from __future__ import annotations
from itertools import count

import os
import sys
import asyncio
from typing import Tuple, List, Iterable, Dict

from .world import BG3World
from .items import ITEM_NAME_TO_ID, AP_ITEM_TO_BG3_ID
from .locations import BG3_LOCATION_TO_AP_LOCATIONS, LOCATION_NAME_TO_ID

import ModuleUpdate
ModuleUpdate.update()

import Utils
import json
import logging

if __name__ == "__main__":
    Utils.init_logging("BG3Client", exception_logger="Client")

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

wg_logger = logging.getLogger("WG")
bugged_locations = []

class BG3ClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.syncing = True


class BG3Context(CommonContext):
    command_processor = BG3ClientCommandProcessor
    game = "Baldur's Gate 3"
    items_handling = 0b111  # full remote
    has_death_link: bool = False
    se_bg3 = ''
    comm_file_sent_items = "ap_in.json"
    comm_file_locations_checked = "ap_out.json"

    def __init__(self, server_address, password):
        super(BG3Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        game_options = BG3World.settings

        appdata_bg3 = os.path.join("%LOCALAPPDATA%", "Larian Studios", "Baldur's Gate 3")
        #logger.debug(f"Game options: {game_options}")
        #logger.debug(f"Root directory: {game_options['root_directory']}")
        #logger.debug(os.path.expandvars(os.path.join(game_options['root_directory'], "Script Extender")))
        #try:
        #    appdata_bg3 = game_options["root_directory"]
        #except FileNotFoundError:
        #    print_error_and_close("BG3Client couldn't detect a path to the Baldur's Gate 3 folder.\n"
        #                            "Try setting the \"root_directory\" value in your local options file "
        #                            "to the folder BG3 is installed to.")
        self.se_bg3 = os.path.expandvars(os.path.join(appdata_bg3, "Script Extender"))

        if not os.path.isdir(self.se_bg3):
            print_error_and_close(f"BG3Client couldn't find the Script Extender folder in your BG3 install.\n"
                                  f"Please make sure Script Extender has been installed, and BG3 "
                                  f"has been run at least once since.")
        #If the in and out files don't exist, create them
        if not os.path.isfile(os.path.join(self.se_bg3, self.comm_file_sent_items)):
            with open(self.comm_file_sent_items, "w") as file:
                file.write("[]")
        if not os.path.isfile(os.path.join(self.se_bg3, self.comm_file_locations_checked)):
            with open(self.comm_file_locations_checked, "w") as file:
                file.write("[]")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BG3Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(BG3Context, self).connection_closed()
        #self.remove_communication_files()
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
        #self.remove_communication_files()
        self.checked_locations.clear()
        self.server_locations.clear()
        self.finished_game = False

    def remove_communication_files(self):
        for root, dirs, files in os.walk(self.se_bg3):
            for file in files:
                os.remove(root + "/" + file)

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

        if cmd in {"RoomInfo"}:
            self.seed_name = args["seed_name"]

        if cmd in {"ReceivedItems"}:
            received_items = [AP_ITEM_TO_BG3_ID[self.item_names.lookup_in_game(network_item.item)] for network_item in self.items_received]
            counter = count()
            received_items = [f"LevelUp<{next(counter)}>" if item == "LevelUp" else item for item in received_items]
            path = os.path.join(self.se_bg3, self.comm_file_sent_items)
            with open(path, 'w') as f:
                json.dump(received_items, f)

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                path = os.path.join(self.se_bg3, self.comm_file_locations_checked)
                #And then we did nothing with it

async def game_watcher(ctx: BG3Context):
    while not ctx.exit_event.is_set():
        try:
            if ctx.syncing == True:
                sync_msg = [{'cmd': 'Sync'}]
                #if ctx.locations_checked:
                    #sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
                await ctx.send_msgs(sync_msg)
                ctx.syncing = False
            sending = []
            victory = False
            bg3LocationsToSend = []

            path = os.path.join(ctx.se_bg3, ctx.comm_file_locations_checked)
            if (os.path.isfile(path)):
                with open(path, 'r') as f:
                    bg3LocationsToSend = json.load(f)
            else:
                with open(path, 'w') as f:
                    f.write("[]")
            for loc in bg3LocationsToSend:
                if loc in BG3_LOCATION_TO_AP_LOCATIONS:
                    for apLoc in BG3_LOCATION_TO_AP_LOCATIONS[loc]:
                        if apLoc not in ctx.checked_locations and apLoc in LOCATION_NAME_TO_ID:
                            sending = sending + [LOCATION_NAME_TO_ID[apLoc]]
                            ctx.checked_locations.add(LOCATION_NAME_TO_ID[apLoc])
                        if apLoc not in LOCATION_NAME_TO_ID:
                            logger.error(f"BUG: Please tell BG3 channel that {apLoc} is a typo and needs fixing. This location may need a server send_location to fix this run.")
                        if apLoc == "Victory_Halsin":
                            victory = True
                elif loc not in bugged_locations:
                    logger.error(f"Please tell BG3 channel about {loc}- it was not handled. This probably doesn't break anything, but it should be looked at.")
                    bugged_locations.append(loc)
           
            message = [{"cmd": 'LocationChecks', "locations": sending}]
            await ctx.send_msgs(message)
            if not ctx.finished_game and victory:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
            await asyncio.sleep(3)

        except Exception as err:
            logger.warn("Exception in communication thread, a check may not have been sent: " + str(err))


def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)

def launch_bg3_client(*launch_args: str):
    async def main():
        args = parser.parse_args(launch_args)
        ctx = BG3Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="BG3ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="BG3 Client, for text interfacing.")

    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()