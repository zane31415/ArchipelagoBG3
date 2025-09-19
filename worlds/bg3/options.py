from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class Goal(Choice):
    """
    Determines what location counts as victory. Currently only Act 1 goals are supported.
    These goals also determine how many level ups are placed in the pool-
    Rescue Halsin: Level Cap 5 - goal is to rescue Halsin and return him safely to the Grove.
    Kill Inquisitor Wwargaz: Level Cap 8 - goal is to kill Inquisitor Wwargaz in the Creche. The space laser does not count.
    Kill Myrkul: Level Cap 10 - goal is to kill the Avatar of Myrkul at the end of Act 2.
    Kill the Nether Brain: Level Cap 12 - goal is to kill the Nether Brain at the end of Act 3.
    """
    
    display_name = "Goal"

    option_rescue_halsin = 0
    option_kill_inquisitor_wwargaz = 1
    option_kill_myrkul = 2
    option_kill_nether_brain = 3

    default = option_rescue_halsin

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

class ObjectsAsChecks(Toggle):
    """
    Makes all rare+ items into AP items. This adds more locations into the pool. Currently unimplemented.
    """

    display_name = "Objects as Checks"
    default = False


class FeatsAsItems(Toggle):
    """
    If true, no feats will be allowed to be taken on level up, and additional items will be added to the pool
    that grant feats when received. Currently unimplemented.
    """

    display_name = "Feats as Items"
    default = False


class StatsAsItems(Toggle):
    """
    If true, Tav will have base 8 in all stats, and additional items will be added to the pool
    that grant stat improvements when received. Currently unimplemented.
    """

    display_name = "Stats as Items"
    default = False

class ApprovalItems(Toggle):
    """
    If true, additional items will be added to the pool that will randomly increase or decrease random
    companions' approval when received. Currently unimplemented.
    """

    display_name = "Approval Items"
    default = False



# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class BG3Options(PerGameCommonOptions):
    goal: Goal
    trim_treasure_method: TrimTreasureMethod
    add_act1a_treasure: AddAct1ATreasure
    add_act1b_treasure: AddAct1BTreasure
    add_act2_treasure: AddAct2Treasure
    add_act3_treasure: AddAct3Treasure
    objects_as_checks: ObjectsAsChecks
    feats_as_items: FeatsAsItems
    stats_as_items: StatsAsItems
    approval_items: ApprovalItems

