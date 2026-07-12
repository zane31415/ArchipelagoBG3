from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range, Toggle, OptionSet, Visibility

class Goal(Choice):
    """
    (Dev note: Progression Balancing is recommended to be 0)
    Determines what location counts as victory.
    These goals also determine how many level ups are placed in the pool-
    Rescue Halsin: Level Cap 5 - goal is to rescue Halsin and return him safely to the Grove.
    Kill Inquisitor Wwargaz: Level Cap 8 - goal is to kill Inquisitor Wwargaz in the Creche.
        The space laser does not count.
    Act 1 user defined fights: Level Cap 8 - goal is to defeat selected bosses (see UserDefinedFights).
    Kill Myrkul: Level Cap 10 - goal is to kill the Avatar of Myrkul at the end of Act 2.
    Act 2 user defined fights: Level Cap 10 - goal is to defeat selected bosses (see UserDefinedFights).
    Kill the Nether Brain: Level Cap 12 - goal is to kill the Nether Brain at the end of Act 3. UNTESTED.
    Act 3 user defined fights: Level Cap 12 - goal is to defeat selected bosses (see UserDefinedFights). UNTESTED.
    """

    display_name = "Goal"

    option_rescue_halsin = 0
    option_kill_inquisitor_wwargaz = 1
    option_act1_user_defined_fights = 2
    option_kill_myrkul = 3
    option_act2_user_defined_fights = 4
    option_kill_nether_brain = 5
    option_act3_user_defined_fights = 6

    default = option_rescue_halsin

class UserDefinedFights(OptionSet):
    """
    If using a User Defined Fights goal, select which fights are required to complete the goal.
    Act 2 fights require the act2_user_defined_fights goal to be selected.
    Act 3 fights require the act3_user_defined_fights goal to be selected.
    Act 1 fights are Auntie Ethel - Ch'r'ai W'wargaz, Act 2 fights are Shambling Mound - Myrkul, Act 3 fights are everything past Myrkul.
    """
    valid_keys = [
        "Auntie Ethel",
        "Spider Queen",
        "Spectator",
        "Bulette",
        "Nere",
        "Grym",
        "Ch'r'ai W'wargaz",
        "Shambling Mound",
        "Cursed Kuo-Toa Chief",
        "Malus Thorm",
        "Gerringothe Thorm",
        "Thisobald Thorm",
        "Ch'r'ai Tska'an",
        "Yurgir",
        "Balthazar",
        "Myrkul"
    ]
    display_name = "User Defined Fights"
    default = {"Auntie Ethel",
        "Spider Queen",
        "Spectator",
        "Bulette",
        "Nere",
        "Grym",
        "Ch'r'ai W'wargaz",
        "Shambling Mound",
        "Cursed Kuo-Toa Chief",
        "Malus Thorm",
        "Gerringothe Thorm",
        "Thisobald Thorm",
        "Ch'r'ai Tska'an",
        "Yurgir",
        "Balthazar",
        "Myrkul"}

class KillSanity(Choice):
    """
    Whether kills of individual creatures should be locations.
    Kills do _not_ count if they are done by falling damage or by being thrown into a chasm.
    
    Currently the only option is "All Nonmissable Hostiles" -  The intent was all monsters that are either default or story-forced hostile,
    and are not likely to be missed by advancing plot. There still do exist some fights that are technically missable (paladins, Nere, etc), but
    only by transitions that have explicit warnings on them.

    Nonmissable Hostiles Location count - Halsin: ~140, Wwargaz: ~250
    """
    display_name = "Killsanity"
    option_off = 0
    option_all_nonmissable_hostiles = 1
    #option_include_missible_bosses = 2
    #option_important_hostiles = 2
    #option_progressive_count = 3
    default = option_off

class QuestSanity(Choice):
    """
    Whether quest updates should be locations.
    Some locations may be buggy or missable- please tell the BG3 channel if any quest doesn't complete that you think should've.
    Due to the nature of the branching of BG3 paths, many quests had to have choices as to what options were viable.
    Currently the only option is "Most Content" - skill checks are not expected to be passed _unless_ future content depends on it.

    Most Content Location count - Halsin: ~200, Wwargaz: ~300
    """
    display_name = "Questsanity"
    option_off = 0
    option_most_content = 1
    #option_important_hostiles = 2
    #option_progressive_count = 3
    default = option_most_content

class ContainerSanity(Choice):
    """
    Whether opening containers should be locations. Currently unimplemented and exists only for testing.
    Even if it was, don't do this.
    """
    visibility = Visibility.none
    display_name = "Containersanity"
    option_off = 0
    option_no_really_dont_do_this = 1
    option_i_suppose_if_you_insist = 2
    default = option_off

class StatSanity(Choice):
    """
    Whether stats should be items. Currently unimplemented. If selected, all characters start at all stats at 8 and you must
    get stats from the multiworld. This is currently only in testing.
    Tav only stats: Only Tav's stats are randomized, and the companions' stats are left alone.
    Party slots: Stats are only applied to party slots, and not the characters. Rearranging the party will rearrange stats.
    Universal stats: Stats are not character specific, and all characters get the same stat boosts when a stat item is received.
    Character stats: Stats are character specific, and each character's stats are randomized separately.
    """
    visibility = Visibility.none
    display_name = "Statsanity"
    option_off = 0
    option_tav_only_stats = 1
    option_party_slots = 2
    option_universal_stats = 3
    option_character_stats = 4
    default = option_off

class StatSanityBoostBy(Range):
    """
    If Statsanity is on, determines how much each stat item boosts the stat by.
    Halsin requires stats at 12, Wwargaz requires stats at 16, Myrkul requires stats at 20.
    The number of item slots taken will be characters * 6 * (required_stat - 8) / boost_amount, 
    so for example if boost_amount is 2, goal is Myrkul, and party_slots is chosen,
    the number of items taken will be 4*6*6 = 144 (this is the highest option).
    Even numbers only, please.
    """
    visibility = Visibility.none
    display_name = "Statsanity Boost By"
    range_start = 2
    range_end = 8
    default = 2

class CharactersInLogic(OptionSet):
    """
    Which characters the generator should assume you will recruit.
    A character NOT listed here has their character-specific plot events removed from the
    location pool: locations named "<Character>: ..." and any "Recruit <Character>" location
    (e.g. removing Lae'zel drops "Lae'zel: Deal with Patrol" and "Beach-LZ: Recruit Lae'zel").
    Other locations that merely depend on a character are not yet auto-detected.
    If Statsanity is on, determines which characters' stats are included in logic.
    If Questsanity is on, determines which characters' quest completions are included in logic.
    Currently in testing.
    """
    valid_keys = ["Astarion", "Gale", "Karlach", "Lae'zel", "Shadowheart", "Wyll", "Halsin", "Minthara"]
    display_name = "Characters in Logic"
    default = {"Astarion", "Gale", "Karlach", "Lae'zel", "Shadowheart", "Wyll", "Halsin", "Minthara"}

class Deathlink(Toggle):
    """
    If true, when a player dies, all players receive an item that kills them. Currently in testing.
    """
    display_name = "Deathlink"
    default = False

class AdditionalLevelUps(Range):
    """
    For an easier play through, this adds items to support additional levels into the pool. Not recommended.
    """
    display_name = "Additional Level Ups"
    range_start = 0
    range_end = 10
    default = 0

class SyncMethod(Choice):
    """
    Determines how AP items will be delivered into BG3.
    With a current mod and client, items are delivered automatically within about a second regardless
    of this choice, and the AP Sync scroll remains as a manual "force a sync now" button.
    This option only changes behavior with an OLD mod version (no sync timer):
    Scroll_Tav - Items will only be generated when the scroll is cast, and placed in Tav's inventory.
    Any_action_Tav - Items will be generated when ANYBODY takes ANY action that the game considers worth triggering the listener flag for
        (which is most things).
    """

    display_name = "SyncMethod"

    option_scroll_tav = 0
    option_any_action_tav = 1

    default = option_any_action_tav

class TrimTreasureMethod(Choice):
    """
    The standard method of having 1:1 items:locations does not work for BG3. Each option instead lists how many locations or items they add.
    Locations are filled with progression first, then useful, and if there is room left, filler.
    If there are not enough locations for all of the useful items, they will be trimmed. This option determines how this trimming is done.
    - Remove Later Treasure First: Removes treasure items that are found later in the game first. This is the recommended option for a more balanced playthrough.
    - Remove Random Treasure: Removes treasure items at random.
    """
    display_name = "Trim Treasure Method"
    option_remove_later_treasure_first = 0
    option_remove_random_treasure = 1
    default = option_remove_later_treasure_first

class AddAct1ATreasure(Toggle):
    """
    Adds 26 items into the pool.
    """
    display_name = "Add Act 1 Overworld Treasure"
    default = True

class AddAct1BTreasure(Toggle):
    """
    Adds 62 items into the pool.
    """
    display_name = "Add Act 1 Underdark Treasure"
    default = True

class AddAct2Treasure(Toggle):
    """
    Adds 103 items into the pool.
    """
    display_name = "Add Act 2 Treasure"
    default = False

class AddAct3Treasure(Toggle):
    """
    Adds 191 items into the pool.
    """
    display_name = "Add Act 3 Treasure"
    default = False

class TrapsPercentage(Range):
    """
    What percent of filler items should be traps.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

class EnabledTraps(OptionSet):
    """
    Which kinds of traps should be enabled. Currently monster spawns do not scale to level.
    Only Monster, Bleeding and Stun are implemented by the game mod right now; the others
    are stripped from the pool at generation (with a warning) until the mod supports them.
    """
    valid_keys = ["Monster", "Bleeding", "Stun", "Confusion", "Sussur", "Clown", "Overburdened"]
    display_name = "Enabled Trap List"
    default = {"Monster", "Bleeding", "Stun"}

class BlockEntrances(Toggle):
    """
    If true, there will be barriers placed in the world that block advancement until a required item is received. This is currently in testing and may be buggy.
    """
    display_name = "Block Entrances"
    default = False

class DevDebugOn(Toggle):
    """
    If true, logs debug items in debug.json
    """
    visibility = Visibility.none
    display_name = "DevDebugOn"
    default = False

#class ObjectsAsChecks(Toggle):
#    """
#    Makes all rare+ items into AP items. This adds more locations into the pool. Currently unimplemented.
#    """
#
#    display_name = "Objects as Checks"
#    default = False


#class FeatsAsItems(Toggle):
#    """
#    If true, no feats will be allowed to be taken on level up, and additional items will be added to the pool
#    that grant feats when received. Currently unimplemented.
#    """

#    display_name = "Feats as Items"
#    default = False


#class StatsAsItems(Toggle):
#    """
#    If true, Tav will have base 8 in all stats, and additional items will be added to the pool
#    that grant stat improvements when received. Currently unimplemented.
#    """

#    display_name = "Stats as Items"
#    default = False

#class ApprovalItems(Toggle):
#    """
#    If true, additional items will be added to the pool that will randomly increase or decrease random
#    companions' approval when received. Currently unimplemented.
#    """

#    display_name = "Approval Items"
#    default = False



# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class BG3Options(PerGameCommonOptions):
    goal: Goal
    user_defined_fights: UserDefinedFights
    killsanity: KillSanity
    questsanity: QuestSanity
    containersanity: ContainerSanity
    statsanity: StatSanity
    statsanity_boost_by: StatSanityBoostBy
    characters_in_logic: CharactersInLogic
    deathlink: Deathlink
    sync_method: SyncMethod
    add_act1a_treasure: AddAct1ATreasure
    add_act1b_treasure: AddAct1BTreasure
    add_act2_treasure: AddAct2Treasure
    add_act3_treasure: AddAct3Treasure
    trim_treasure_method: TrimTreasureMethod
    additional_level_ups: AdditionalLevelUps
    traps_percentage: TrapsPercentage
    enabled_traps: EnabledTraps
    block_entrances: BlockEntrances
    dev_debug_on: DevDebugOn
#    objects_as_checks: ObjectsAsChecks
#    feats_as_items: FeatsAsItems
#    stats_as_items: StatsAsItems
#    approval_items: ApprovalItems

