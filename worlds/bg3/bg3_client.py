from __future__ import annotations
from itertools import count

import os
import sys
import time
import asyncio
import typing
from typing import Tuple, List, Iterable, Dict

from .world import BG3World
from .items import AP_ITEM_TO_BG3_ID, IS_DUPEABLE
from .locations import BG3_LOCATION_TO_AP_LOCATIONS, LOCATION_NAME_TO_ID

import ModuleUpdate
ModuleUpdate.update()

import Utils
import json
import logging

if __name__ == "__main__":
    Utils.init_logging("BG3Client", exception_logger="Client")

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, handle_url_arg, ClientCommandProcessor, \
    CommonContext, server_loop

wg_logger = logging.getLogger("WG")
bugged_locations = ["Victory_Halsin", "Victory_Wwargaz", "Victory_Myrkul", "Victory_Brain", "Bad_State"]
bad_states = []
act1bosses = ["Victory_Halsin", "Hag: Kill Auntie Ethel", "Village: Kill Well Spider Queen", "Underdark: Kill Spectator", "Underdark: Kill Bulette", "Grym: Kill Nere", "Forge: Kill Grym", "Creche: Kill Ch'r'ai W'wargaz"]
act2bosses = ["East Act 2: Kill Shambling Mound", "Reithwin: Kill Cursed Kuo-Toa Chief", "HoH: Kill Malus Thorm", "Tollhouse: Kill Gerringothe Thorm", "Brewery: Kill Thisobald Thorm", "Reithwin: Kill Ch'r'ai Tska'an", "Shar: Kill Yurgir", "Shar: Kill Balthazar", "Colony Showdown: Kill Myrkul"]
act3bosses = []
goalbosses = act1bosses + act2bosses + act3bosses
goal = -1
bossmap = {
    "Auntie Ethel": "Hag: Kill Auntie Ethel",
    "Spider Queen": "Village: Kill Well Spider Queen",
    "Spectator": "Underdark: Kill Spectator",
    "Bulette": "Underdark: Kill Bulette",
    "Nere": "Grym: Kill Nere",
    "Grym": "Forge: Kill Grym",
    "Ch'r'ai W'wargaz": "Creche: Kill Ch'r'ai W'wargaz",

    "Shambling Mound": "East Act 2: Kill Shambling Mound",
    "Cursed Kuo-Toa Chief": "Reithwin: Kill Cursed Kuo-Toa Chief",
    "Malus Thorm": "HoH: Kill Malus Thorm",
    "Gerringothe Thorm": "Tollhouse: Kill Gerringothe Thorm",
    "Thisobald Thorm": "Brewery: Kill Thisobald Thorm",
    "Ch'r'ai Tska'an": "Reithwin: Kill Ch'r'ai Tska'an",
    "Yurgir": "Shar: Kill Yurgir",
    "Balthazar": "Shar: Kill Balthazar",
    "Myrkul": "Colony Showdown: Kill Myrkul"
}

HEARTBEAT_INTERVAL = 5.0        # seconds between heartbeat_client.json writes
GAME_STALE_SECONDS = 15.0       # 3x the mod's 5 s heartbeat cadence
WATCHER_INTERVAL = 1.0          # out-file poll; the mod reacts to us via gen_in


def atomic_write_text(path: str, text: str) -> None:
    """Write-then-rename so the mod's Ext.IO.LoadFile never sees a torn file.

    os.replace is atomic on NTFS when source and destination are on the same
    volume, which they are (both live in the Script Extender folder).
    """
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def atomic_write_json(path: str, obj) -> None:
    atomic_write_text(path, json.dumps(obj))


class BG3ClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True

    def _cmd_deathlink(self):
        """Toggles deathlink On/Off"""
        if isinstance(self.ctx, BG3Context):
            self.ctx.has_death_link = not self.ctx.has_death_link
            Utils.async_start(self.ctx.update_death_link(self.ctx.has_death_link), name="Update Deathlink")
            if self.ctx.has_death_link:
                death_link_send_file = os.path.join(self.ctx.se_bg3, self.ctx.deathlink_out)
                if os.path.exists(death_link_send_file):
                    atomic_write_json(death_link_send_file, [])
                self.output(f"Deathlink enabled.")
            else:
                death_link_receive_file = os.path.join(self.ctx.se_bg3, self.ctx.deathlink_in)
                if os.path.exists(death_link_receive_file):
                    atomic_write_json(death_link_receive_file, [])
                self.output(f"Deathlink disabled.")



class BG3Context(CommonContext):
    command_processor = BG3ClientCommandProcessor
    game = "Baldur's Gate 3"
    items_handling = 0b111  # full remote
    has_death_link: bool = False
    se_bg3 = ''
    comm_file_sent_items = "ap_in.json"
    comm_file_locations_checked = "ap_out.json"
    comm_file_item_names = "ap_names.json"
    comm_file_gen = "gen_in.txt"
    comm_file_command = "ap_command.json"
    sync_option = "ap_options.json"
    deathlink_in = "deathLinkReceive.json"
    deathlink_out = "deathLinkSend.json"
    heartbeat_out = "heartbeat_client.json"
    heartbeat_game = "heartbeat_game.json"
    seed_name = ""

    def __init__(self, server_address, password):
        super(BG3Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.gen_counter: int = 0
        self.last_command_seq: typing.Optional[int] = None
        self.game_present: typing.Optional[bool] = None  # None = unknown yet
        self._game_beat_content: typing.Optional[str] = None
        self._game_beat_changed_at: float = 0.0
        self._warned_unknown_items: typing.Set[str] = set()
        self._watcher_errors_seen: typing.Set[str] = set()
        self._instance_lock = None
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        game_options = BG3World.settings

        appdata_bg3 = ""
        if "localappdata" in os.environ:
            appdata_bg3 = os.path.join(os.environ['localappdata'], "Larian Studios", "Baldur's Gate 3")
        else:
            try:
                appdata_bg3 = game_options.root_directory
            except FileNotFoundError:
                print_error_and_close("BG3Client couldn't detect a path to the Baldur's Gate 3 folder.\n"
                                        "Try setting the \"root_directory\" value in your local options file "
                                        "to the folder BG3 is installed to.\n"
                                        "On Steam Deck / Linux (Proton), this is inside the game's prefix, e.g.\n"
                                        "steamapps/compatdata/1086940/pfx/drive_c/users/steamuser/AppData/Local/"
                                        "Larian Studios/Baldur's Gate 3")
        self.se_bg3 = os.path.expandvars(os.path.join(appdata_bg3, "Script Extender"))

        if not os.path.isdir(self.se_bg3):
            print_error_and_close(f"BG3Client couldn't find the Script Extender folder in your BG3 install.\n"
                                  f"Please make sure Script Extender has been installed, and BG3 "
                                  f"has been run at least once since.")

        # A stale client instance (window closed, process alive) keeps
        # rewriting the comm files and fights any newly launched instance;
        # historically this "broke items until reboot".
        self._instance_lock = acquire_single_instance_lock(self.se_bg3)
        if self._instance_lock is None:
            print_error_and_close("Another Archipelago BG3 Client is already running.\n"
                                  "Close it first (check Task Manager for a stuck BG3Client "
                                  "if you can't find its window).")

        #If the in and out files don't exist, create them (in the SE folder -
        # these unprefixed files are what a pre-options-load game session uses)
        if not os.path.isfile(os.path.join(self.se_bg3, self.comm_file_sent_items)):
            atomic_write_text(os.path.join(self.se_bg3, self.comm_file_sent_items), "[]")
        if not os.path.isfile(os.path.join(self.se_bg3, self.comm_file_locations_checked)):
            atomic_write_text(os.path.join(self.se_bg3, self.comm_file_locations_checked), "[]")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        # The mod clears this file at session load, so a deathlink received
        # while the game is closed won't fire on the next session.
        atomic_write_json(os.path.join(self.se_bg3, self.deathlink_in), ["DeathLink"])
        super(BG3Context, self).on_deathlink(data)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BG3Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(BG3Context, self).connection_closed()
        self.checked_locations.clear()
        self.server_locations.clear()
        self.finished_game = False

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(BG3Context, self).shutdown()
        self.checked_locations.clear()
        self.server_locations.clear()
        self.finished_game = False
        release_single_instance_lock(self._instance_lock)
        self._instance_lock = None

    def remove_communication_files(self):
        # Not called from anywhere right now; kept as a safe (allowlisted)
        # helper. The SE folder is shared with every other SE mod's storage,
        # so this must never walk the directory indiscriminately.
        our_files = [
            self.comm_file_sent_items, self.comm_file_locations_checked,
            self.comm_file_item_names, self.comm_file_gen, self.comm_file_command,
            self.sync_option, self.deathlink_in, self.deathlink_out,
            self.heartbeat_out, self.heartbeat_game, "debug.json", "items_to_remove.json",
        ]
        prefixes = [""] if not self.seed_name else ["", self.seed_name]
        for prefix in prefixes:
            for name in our_files:
                path = os.path.join(self.se_bg3, prefix + name)
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

    @staticmethod
    def apply_item_suffixes(received_items: List[str]) -> List[str]:
        levelcounter = count()
        goldcounter = count()
        trapcounter = count()
        fillercounter = count()
        progressivemoonlightcounter = count()
        return [f"LevelUp<{next(levelcounter)}>" if item == "LevelUp"
                else f"{item}-{next(goldcounter)}" if item[:4] == "Gold"
                else f"{item}-2e51b930-c9fd-41f2-8013-02c92e990de2-{next(trapcounter)}" if item[:12] == "Trap-Monster"
                else f"{item}-{next(trapcounter)}" if item[:4] == "Trap"
                else f"{item}-{next(progressivemoonlightcounter)}" if item == "Gate-ProgressiveMoonlightTowers"
                else f"Dupe-{next(fillercounter):04}-{item}" if IS_DUPEABLE.get(item, False)
                else item for item in received_items]

    def write_items_files(self) -> None:
        """Rewrite {seed}ap_in.json + {seed}ap_names.json, then bump the gen
        file. Payload first (atomic replace), gen bump second, so the mod
        never parses a half-written payload."""
        if self.seed_name == "":
            # RoomInfo hasn't arrived yet; writing unprefixed files here would
            # just litter the folder with data the game will never read.
            return
        ap_names: List[str] = []
        bg3_ids: List[str] = []
        unknown: List[str] = []
        for network_item in self.items_received:
            name = self.item_names.lookup_in_game(network_item.item)
            bg3_id = AP_ITEM_TO_BG3_ID.get(name)
            if bg3_id is None:
                # Server generated with a newer apworld than ours; deliver
                # what we can instead of dying on the KeyError.
                if name not in self._warned_unknown_items:
                    unknown.append(name)
                    self._warned_unknown_items.add(name)
                continue
            ap_names.append(name)
            bg3_ids.append(bg3_id)
        if unknown:
            logger.error(f"Received items this apworld version doesn't know: {unknown}. "
                         f"Your installed bg3 apworld is older than the one this seed was "
                         f"generated with - update it. Everything else will still be delivered.")
        wire_items = self.apply_item_suffixes(bg3_ids)
        names_map = {wire: ap_name for wire, ap_name in zip(wire_items, ap_names)}
        atomic_write_json(os.path.join(self.se_bg3, self.seed_name + self.comm_file_sent_items), wire_items)
        atomic_write_json(os.path.join(self.se_bg3, self.seed_name + self.comm_file_item_names), names_map)
        self.bump_gen_file()
        if self.game_present is False:
            logger.warning("Items are arriving from the server, but no game heartbeat is "
                           "present - is BG3 running with the Archipelago mod enabled?")

    def bump_gen_file(self) -> None:
        # Content only has to *change*; time_ns also stays unique across
        # client restarts (a plain counter would restart at 1 and could
        # collide with the previous instance's value).
        self.gen_counter += 1
        with open(os.path.join(self.se_bg3, self.seed_name + self.comm_file_gen), "w") as f:
            f.write(str(time.time_ns()))

    def run_gui(self):
        from kvui import GameManager

        class BG3Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Baldur's Gate 3 Client"

        self.ui = BG3Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            slot_data = args["slot_data"]
            if "seed_name" in args and args["seed_name"]:
                self.seed_name = args["seed_name"]
            self.has_death_link = slot_data.get("death_link", False)
            Utils.async_start(self.update_death_link(self.has_death_link), name="Update Deathlink")
            global goal
            goal = slot_data["goal"]
            if (goal == 2 or goal == 4):
                global user_defined_fights
                global goalbosses
                user_defined_fights = slot_data["user_defined_fights"]
                user_selected_fight_values = set()
                for key in user_defined_fights:
                    if key in bossmap:
                        user_selected_fight_values.add(bossmap[key])
                goalbosses = [boss for boss in goalbosses if boss in user_selected_fight_values]
                logger.error(f"Expected bosses to defeat for goal: {goalbosses}")
            atomic_write_json(os.path.join(self.se_bg3, self.sync_option), slot_data)
            self.write_items_files()

        if cmd in {"RoomInfo"}:
            if "seed_name" in args and args["seed_name"]:
                self.seed_name = args["seed_name"]

        if cmd in {"ReceivedItems"}:
            self.write_items_files()


async def process_command_file(ctx: BG3Context):
    """Consume ap_command.json (written by the mod when the player pushes a
    button in the in-game window). Single writer (the mod); we only remember
    the last seq we acted on - anything present when the client starts is
    treated as already consumed."""
    path = os.path.join(ctx.se_bg3, ctx.comm_file_command)
    if not os.path.isfile(path):
        return
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except (ValueError, OSError):
        return
    if not isinstance(data, dict):
        return
    seq = data.get("seq")
    if not isinstance(seq, int):
        return
    if ctx.last_command_seq is None:
        ctx.last_command_seq = seq
        return
    if seq <= ctx.last_command_seq:
        return
    ctx.last_command_seq = seq
    command = data.get("command")
    if command == "resync":
        logger.info("Resync requested from the in-game window.")
        ctx.syncing = True
        ctx.write_items_files()
    else:
        logger.info(f"Ignoring unknown in-game command: {command!r}")


async def game_watcher(ctx: BG3Context):
    while not ctx.exit_event.is_set():
        try:
            if ctx.syncing == True:
                sync_msg = [{'cmd': 'Sync'}]
                await ctx.send_msgs(sync_msg)
                ctx.syncing = False
            sending = []
            newly_checked = set()
            victory = False
            bg3LocationsToSend = []

            await process_command_file(ctx)

            if ctx.seed_name != "":
                path = os.path.join(ctx.se_bg3, ctx.seed_name + ctx.comm_file_locations_checked)
                if (os.path.isfile(path)):
                    with open(path, 'r') as f:
                        bg3LocationsToSend = json.load(f)
                else:
                    atomic_write_text(path, "[]")
                if goal != -1:
                    global goalbosses
                    if goal not in [0,1,2,3,4]:
                        logger.error(f"Your version of the apworld is not compatible with server's version. Please update your apworld and try again.")
                        logger.error(goal)
                    for loc in bg3LocationsToSend:
                        if loc in BG3_LOCATION_TO_AP_LOCATIONS:
                            for apLoc in BG3_LOCATION_TO_AP_LOCATIONS[loc]:
                                if apLoc in LOCATION_NAME_TO_ID:
                                    apLocId = LOCATION_NAME_TO_ID[apLoc]
                                    if apLocId not in ctx.checked_locations and apLocId not in newly_checked:
                                        sending.append(apLocId)
                                        newly_checked.add(apLocId)
                                if apLoc not in LOCATION_NAME_TO_ID and apLoc not in bugged_locations:
                                    logger.error(f"BUG: Please tell BG3 channel that {apLoc} is a typo and needs fixing. This location (if it exists) may need a server send_location to fix this run.")
                                    bugged_locations.append(apLoc)
                                if apLoc == "Victory_Halsin" and goal == 0:
                                    victory = True
                                elif apLoc == "Victory_Wwargaz" and goal == 1:
                                    victory = True
                                elif apLoc == "Victory_Myrkul" and goal == 3:
                                    victory = True
                                elif (apLoc in goalbosses) and (goal == 2 or goal == 4):
                                    remaining_bosses = [
                                        boss for boss in goalbosses
                                        if LOCATION_NAME_TO_ID[boss] not in ctx.checked_locations
                                        and LOCATION_NAME_TO_ID[boss] not in newly_checked
                                    ]
                                    if not remaining_bosses:
                                        victory = True
                                    else:
                                        goalbosses = remaining_bosses
                                        logger.error(f"Remaining bosses to defeat for goal: {goalbosses}")
                                elif apLoc == "Bad_State" and loc not in bad_states:
                                    logger.error(f"Something has happened in the game that may make some locations unreachable. Consider loading an earlier save.")
                                    bad_states.append(loc)
                        elif loc[:5] == "Kill-":
                            pass # A kill that we don't track for this setting, ignore it.
                        elif loc not in bugged_locations:
                            # logger.error(f"Please tell BG3 channel about {loc}- it was not handled. This probably doesn't break anything, but it should be looked at.")
                            bugged_locations.append(loc)
                    if goal == 2 or goal == 4:
                        remaining_bosses = [
                            boss for boss in goalbosses
                            if LOCATION_NAME_TO_ID[boss] not in ctx.checked_locations
                            and LOCATION_NAME_TO_ID[boss] not in newly_checked
                        ]
                        if not remaining_bosses:
                            victory = True
                        goalbosses = remaining_bosses

                    # Send first, mark as checked only after the send didn't
                    # raise - otherwise an exception here would eat these
                    # checks for the rest of the session.
                    if sending:
                        message = [{"cmd": 'LocationChecks', "locations": sending}]
                        await ctx.send_msgs(message)
                    ctx.checked_locations.update(newly_checked)
                    if not ctx.finished_game and victory:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                path = os.path.join(ctx.se_bg3, ctx.deathlink_out)
                if (os.path.isfile(path) and ctx.has_death_link):
                    with open(path, 'r') as file:
                        deaths = json.load(file)
                    if deaths and ctx.slot is not None:
                        for death in deaths:
                            await ctx.send_death(f"{ctx.player_names[ctx.slot]} had {death} hang out with Jergal for a bit.")
                        # Rewrite minus what we processed instead of blind
                        # truncation; the mod appends, so a death landing in
                        # this window survives. (A tiny read-modify-write race
                        # remains and is accepted - worst case one duplicate
                        # or dropped deathlink.)
                        try:
                            with open(path, 'r') as file:
                                current = json.load(file)
                        except (ValueError, OSError):
                            current = []
                        remaining = list(current) if isinstance(current, list) else []
                        for death in deaths:
                            if death in remaining:
                                remaining.remove(death)
                        atomic_write_json(path, remaining)

            await asyncio.sleep(WATCHER_INTERVAL)

        except Exception as err:
            # Log the traceback once per distinct error so field reports
            # contain something actionable, without spamming every poll.
            msg = f"{type(err).__name__}: {err}"
            if msg not in ctx._watcher_errors_seen:
                ctx._watcher_errors_seen.add(msg)
                logger.exception("Exception in communication thread, a check may not have been sent")
            else:
                logger.error("Exception in communication thread, a check may not have been sent: " + msg)
            await asyncio.sleep(WATCHER_INTERVAL)


async def heartbeat_task(ctx: BG3Context):
    """Write our presence heartbeat and watch the game's.

    Deliberately its own task (not part of game_watcher) so the beat keeps
    going even when a watcher iteration fails. Heartbeats are plain
    overwrites, not atomic replaces: a torn read is harmless and skipping
    temp+rename halves the metadata churn (design doc section 13.2.1).
    """
    n = 0
    while not ctx.exit_event.is_set():
        try:
            n += 1
            beat = {
                "n": n,
                "server_connected": bool(ctx.server and ctx.slot is not None),
                "slot": ctx.auth or "",
                "seed": ctx.seed_name,
            }
            with open(os.path.join(ctx.se_bg3, ctx.heartbeat_out), "w") as f:
                json.dump(beat, f)

            # Game presence, by content change (never wall clock comparison).
            game_beat = None
            try:
                with open(os.path.join(ctx.se_bg3, ctx.heartbeat_game), "r") as f:
                    game_beat = f.read()
            except OSError:
                pass
            now = time.monotonic()
            if game_beat is not None and game_beat != ctx._game_beat_content:
                ctx._game_beat_content = game_beat
                ctx._game_beat_changed_at = now
                if ctx.game_present is not True:
                    ctx.game_present = True
                    logger.info("Game: connected (BG3 heartbeat detected).")
            elif ctx.game_present is True and now - ctx._game_beat_changed_at > GAME_STALE_SECONDS:
                ctx.game_present = False
                logger.warning("Game: not detected (BG3 heartbeat went stale). "
                               "Checks and items will catch up when it's back.")
        except Exception:
            logger.exception("Exception in heartbeat task")
        await asyncio.sleep(HEARTBEAT_INTERVAL)


def _acquire_lock_windows():
    """Named-mutex guard. Returns a token, or None if another client holds it."""
    import ctypes
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    handle = kernel32.CreateMutexW(None, True, "ArchipelagoBG3ClientSingleInstance")
    if not handle:
        return ("win_mutex", None)  # couldn't even create one; don't block startup
    ERROR_ALREADY_EXISTS = 183
    if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
        kernel32.CloseHandle(handle)
        return None
    return ("win_mutex", handle)


def _acquire_lock_posix(se_dir: str):
    """pid-lockfile guard with a liveness check, for Linux/Mac (Steam Deck).

    NB: only ever call this off Windows - os.kill(pid, 0) is a liveness probe
    on POSIX, but on Windows it calls TerminateProcess and would kill the pid.
    """
    lock_path = os.path.join(se_dir, "bg3client.lock")
    for _ in range(2):
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return ("lockfile", lock_path)
        except FileExistsError:
            pass
        # Someone holds it. Are they still alive?
        try:
            with open(lock_path) as f:
                pid = int(f.read().strip())
        except (ValueError, OSError):
            pid = None                   # empty/garbage/vanished -> stale
        if pid is not None:
            try:
                os.kill(pid, 0)
                return None              # signalled fine -> holder is alive
            except PermissionError:
                return None              # exists but owned by another user -> alive
            except OSError:
                pass                     # ProcessLookupError -> stale
        try:
            os.remove(lock_path)         # stale; drop it and retry once
        except OSError:
            return None
    return None


def acquire_single_instance_lock(se_dir: str):
    """Returns an opaque lock token, or None if another live client holds it.

    The per-platform implementations live in their own functions on purpose: a
    type checker resolves sys.platform statically, so an inline non-Windows
    branch sitting after an always-returning Windows branch gets flagged
    unreachable and is then skipped by analysis entirely.
    """
    if sys.platform == "win32":
        return _acquire_lock_windows()
    return _acquire_lock_posix(se_dir)


def release_single_instance_lock(token) -> None:
    if not token:
        return
    kind, value = token
    if kind == "win_mutex" and value:
        import ctypes
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.ReleaseMutex(value)
        kernel32.CloseHandle(value)
    elif kind == "lockfile":
        try:
            os.remove(value)
        except OSError:
            pass


def read_apbg3_file(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        logger.error(f"Couldn't read connect file {path}")
        return {}


def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)

def launch_bg3_client(*launch_args: str):
    async def main():
        args = parser.parse_args(launch_args)
        connect_info = {}
        if args.url and args.url.endswith(".apbg3"):
            # Double-clicked connect file from the seed's generation output.
            connect_info = read_apbg3_file(args.url)
            args.url = None
        args = handle_url_arg(args, parser=parser)  # archipelago:// room links
        server = args.connect or connect_info.get("server")
        slot = args.name or connect_info.get("player")
        ctx = BG3Context(server, args.password)
        if slot:
            # Pre-fill the slot name so connecting is one click.
            ctx.auth = slot
            if connect_info:
                logger.info(f"Loaded connect file for slot '{slot}'"
                            + (f", server {server}" if server else "; enter the server address to connect."))
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="BG3ProgressionWatcher")
        heartbeat = asyncio.create_task(
            heartbeat_task(ctx), name="BG3Heartbeat")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher
        await heartbeat

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="BG3 Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", default=None,
                        help="archipelago:// connection url, or a .apbg3 connect file "
                             "from the seed's generation output")

    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
