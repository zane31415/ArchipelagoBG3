from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)
#"goal", "objects_as_checks", "feats_as_items", "stats_as_items", "approval_items"

# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
class Goal(Choice):
    """
    Determines what location counts as victory. Currently only "Escape the Nautiloid" is supported.
    """
    # The docstring of an option is used as the description on the website and in the template yaml.

    # You'll also want to set a display name, which will determine what the option is called on the website.
    display_name = "Goal"

    option_escape_nautiloid = 0
    option_kill_nether_brain = 1

    # Choice options must define an explicit default value.
    default = option_escape_nautiloid

class ObjectsAsChecks(Toggle):
    """
    Makes all rare+ items into AP items. This adds more locations into the pool. Currently unimplemented.
    """

    display_name = "Objects as Checks"


class FeatsAsItems(Toggle):
    """
    If true, no feats will be allowed to be taken on level up, and additional items will be added to the pool
    that grant feats when received. Currently unimplemented.
    """

    display_name = "Feats as Items"


class StatsAsItems(Range):
    """
    If true, Tav will have base 8 in all stats, and additional items will be added to the pool
    that grant stat improvements when received. Currently unimplemented.
    """

    display_name = "Stats as Items"

class ApprovalItems(Toggle):
    """
    If true, additional items will be added to the pool that will randomly increase or decrease random
    companions' approval when received. Currently unimplemented.
    """

    display_name = "Approval Items"



# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class BG3Options(PerGameCommonOptions):
    goal: Goal
    objects_as_checks: ObjectsAsChecks
    feats_as_items: FeatsAsItems
    stats_as_items: StatsAsItems
    approval_items: ApprovalItems

