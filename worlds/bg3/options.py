from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, OptionSet

class Goal(Choice):
    """
    Determines what location counts as victory. Currently only Act 1 goals are supported.
    These goals also determine how many level ups are placed in the pool-
    Rescue Halsin: Level Cap 5 - goal is to rescue Halsin and return him safely to the Grove.
    Kill Inquisitor Wwargaz: Level Cap 8 - goal is to kill Inquisitor Wwargaz in the Creche.
        The space laser does not count.
    """
    #Kill Myrkul: Level Cap 10 - goal is to kill the Avatar of Myrkul at the end of Act 2.
    #Kill the Nether Brain: Level Cap 12 - goal is to kill the Nether Brain at the end of Act 3.

    display_name = "Goal"

    option_rescue_halsin = 0
    option_kill_inquisitor_wwargaz = 1
    #option_kill_myrkul = 2
    #option_kill_nether_brain = 3

    default = option_rescue_halsin

class KillSanity(Toggle):
    """
    Whether kills of individual creatures should be locations.
    This has recently been added and may not be complete and/or may have issues with some kills.
    Kills do _not_ count if they are done by falling damage or by being thrown into a chasm.
    Due to the missability of some checks, it is advised to save often.

    Nonmissable Hostiles Location count - Halsin: ~140, Wwargaz: ~250
    """
    display_name = "Killsanity"
    option_off = 0
    option_all_nonmissable_hostiles = 1
    #option_important_hostiles = 2
    #option_progressive_count = 3
    default = option_off

class QuestSanity(Toggle):
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

class AdditionalLevelUps(Range):
    """
    For an easier play through, this adds additional Level Up items into the pool. Level hard caps at 12 regardless of setting. Not recommended.
    """
    display_name = "Additional Level Ups"
    range_start = 0
    range_end = 10
    default = 0

class SyncMethod(Choice):
    """
    Determines how AP items will be delivered into BG3. All options will still have the AP Sync scroll, it just will be a No-op if not needed.
    Scroll_Tav - Items will only be generated when the scroll is cast, and placed in Tav's inventory.
    Any_action_Tav - Items will be generated when ANYBODY takes ANY action that the game considers worth triggering the listener flag for
        (which is most things). Items will be given to the character currently being controlled.
        This may (will likely) cause encumbrance issues, potentially even during combat.
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
    default = option_remove_random_treasure

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
    What percent of filler items should be traps. This is EXPERIMENTAL.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

class EnabledTraps(OptionSet):
    """
    Which kinds of traps should be enabled. This is EXPERIMENTAL. Currently monster spawns do not scale to level.
    Monster traps are currently broken.
    """
    valid_keys = ["Monster", "Bleeding", "Stun"]
    display_name = "Enabled Trap List"
    default = {"Bleeding", "Stun"}



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
    killsanity: KillSanity
    questsanity: QuestSanity
    sync_method: SyncMethod
    add_act1a_treasure: AddAct1ATreasure
    add_act1b_treasure: AddAct1BTreasure
    add_act2_treasure: AddAct2Treasure
    add_act3_treasure: AddAct3Treasure
    trim_treasure_method: TrimTreasureMethod
    additional_level_ups: AdditionalLevelUps
    traps_percentage: TrapsPercentage
    enabled_traps: EnabledTraps
#    objects_as_checks: ObjectsAsChecks
#    feats_as_items: FeatsAsItems
#    stats_as_items: StatsAsItems
#    approval_items: ApprovalItems

