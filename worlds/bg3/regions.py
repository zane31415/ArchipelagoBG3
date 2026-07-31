from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import BG3World

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).

_STATS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]


def _build_rule(
    world: BG3World,
    level_fragments: int = 0,
    block_items: list[str] | None = None,
    stats: int = 0,
) -> Callable | None:
    """Build an entrance access rule callable from level, block-item, and statsanity requirements.

    Args:
        level_fragments: Number of Level Fragment items required.
        block_items: Items required only when the block_entrances option is enabled.
        stats: Raw stat investment required per stat (divided by statsanity_boost_by for item count).
    Returns None when there are no conditions so the caller can skip setting a rule.
    """
    player = world.player
    checks = []

    if level_fragments:
        n = level_fragments
        checks.append(lambda state, _n=n: state.has("Level Fragment", player, _n))

    if block_items and world.options.block_entrances == 1:
        if (block_items[0] == "Blighted Village"):
            if (world.options.goal == world.options.goal.option_rescue_halsin):
                checks.append(lambda state: state.has("Blighted Village Well", player))
            else:
                checks.append(lambda state: state.has("Underdark", player))
        elif (block_items[0] == "Moonlight Towers"):
            checks.append(lambda state: state.has("Progressive Moonlight Towers", player, 4))
        elif (block_items[0] == "Mindflayer"):
            checks.append(lambda state: state.has("Progressive Moonlight Towers", player, 5))
        else:
            for item in block_items:
                checks.append(lambda state, _i=item: state.has(_i, player))

    if stats:
        count = stats / world.options.statsanity_boost_by
        statsanity = world.options.statsanity
        if (statsanity == statsanity.option_tav_only_stats
                or statsanity == statsanity.option_universal_stats):
            for stat in _STATS:
                item_name = f"{stat} Stat Boost"
                checks.append(lambda state, _i=item_name, _c=count: state.has(_i, player, _c))
        elif statsanity == statsanity.option_party_slots:
            for slot in range(1, 5):
                for stat in _STATS:
                    item_name = f"Slot {slot} {stat} Stat Boost"
                    checks.append(lambda state, _i=item_name, _c=count: state.has(_i, player, _c))

    if not checks:
        return None
    return lambda state: all(c(state) for c in checks)


def _connect(source, dest, name, world: BG3World,
             level_fragments: int = 0,
             block_items: list[str] | None = None,
             stats: int = 0) -> None:
    rule = _build_rule(world, level_fragments, block_items, stats)
    if rule is not None:
        source.connect(dest, name, rule)
    else:
        source.connect(dest, name)


def create_and_connect_regions(world: BG3World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: BG3World) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    tutorial = Region("Tutorial", world.player, world.multiworld)
    beach = Region("Beach", world.player, world.multiworld)
    crypt = Region("Crypt", world.player, world.multiworld)
    grove = Region("Grove", world.player, world.multiworld)
    blighted_village = Region("Blighted Village", world.player, world.multiworld)
    goblin_camp = Region("Goblin Camp", world.player, world.multiworld)
    waukeen = Region("Waukeen", world.player, world.multiworld)
    hag = Region("Hag", world.player, world.multiworld)
    underdark = Region("Underdark", world.player, world.multiworld)
    grymforge = Region("Grymforge", world.player, world.multiworld)
    monastery = Region("Monastery", world.player, world.multiworld)
    creche = Region("Creche", world.player, world.multiworld)

    east_act2 = Region("East Act 2", world.player, world.multiworld)
    west_act2 = Region("West Act 2", world.player, world.multiworld)
    last_light = Region("Last Light Inn", world.player, world.multiworld)
    moonrise = Region("Moonrise Towers", world.player, world.multiworld)
    shar_gauntlet = Region("Gauntlet of Shar", world.player, world.multiworld)
    mindflayer = Region("Mindflayer Colony", world.player, world.multiworld)

    rivington = Region("Rivington", world.player, world.multiworld)
    wyrms_crossing = Region("Wyrm's Crossing", world.player, world.multiworld)
    lower_city = Region("Lower City", world.player, world.multiworld)
    lower_city_sewers = Region("Lower City Sewers", world.player, world.multiworld)
    # house_of_hope = Region("House of Hope", world.player, world.multiworld)
    # steel watch foundry
    # counting house
    # szarr palace
    # undercity ruins
    # blushing mermaid
    # house of grief
    # upper city
    iron_throne = Region("Iron Throne", world.player, world.multiworld)
    netherbrain = Region("Netherbrain", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [tutorial, beach, crypt, grove, blighted_village, goblin_camp, waukeen, hag, underdark, grymforge, monastery, creche, \
            east_act2, west_act2, last_light, moonrise, shar_gauntlet, mindflayer, \
            rivington, wyrms_crossing, lower_city, lower_city_sewers, iron_throne, netherbrain]

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: BG3World) -> None:
    tutorial = world.get_region("Tutorial")
    beach = world.get_region("Beach")
    crypt = world.get_region("Crypt")
    grove = world.get_region("Grove")
    blighted_village = world.get_region("Blighted Village")
    goblin_camp = world.get_region("Goblin Camp")
    waukeen = world.get_region("Waukeen")
    hag = world.get_region("Hag")
    
    underdark = world.get_region("Underdark")
    grymforge = world.get_region("Grymforge")
    monastery = world.get_region("Monastery")
    creche = world.get_region("Creche")

    east_act2 = world.get_region("East Act 2")
    west_act2 = world.get_region("West Act 2")
    last_light = world.get_region("Last Light Inn")
    moonrise = world.get_region("Moonrise Towers")
    shar_gauntlet = world.get_region("Gauntlet of Shar")
    mindflayer = world.get_region("Mindflayer Colony")

    rivington = world.get_region("Rivington")
    wyrms_crossing = world.get_region("Wyrm's Crossing")
    lower_city = world.get_region("Lower City")
    lower_city_sewers = world.get_region("Lower City Sewers")
    # house_of_hope = world.get_region("House of Hope")
    iron_throne = world.get_region("Iron Throne")
    netherbrain = world.get_region("Netherbrain")

    _connect(tutorial, beach, "Tutorial to Beach", world, level_fragments=1, block_items=["Nautiloid Control Panel"]) # Level 2
    _connect(beach, crypt, "Beach to Crypt", world, block_items=["Wither's Crypt"])
    _connect(beach, grove, "Beach to Grove", world, level_fragments=3) # Level 3
    _connect(beach, blighted_village, "Beach to Blighted Village", world, level_fragments=3, block_items=["Blighted Village"]) # Level 3
    _connect(blighted_village, goblin_camp, "Blighted Village to Goblin Camp", world, level_fragments=8, block_items=["Goblin Camp"]) # Level 4.5
    _connect(blighted_village, hag, "Blighted Village to Hag", world, level_fragments=10, stats=4, block_items=["Hag's Fireplace"]) # Level 5
    _connect(blighted_village, waukeen, "Blighted Village to Waukeen", world, level_fragments=6, block_items=["Zhentarim Basement"]) # Level 4

    if (world.options.goal != world.options.goal.option_rescue_halsin):
        _connect(goblin_camp, underdark, "Goblin Camp to Underdark", world, level_fragments=10, block_items=["Underdark"]) # Level 5
        _connect(underdark, grymforge, "Underdark to Grymforge", world, level_fragments=14, block_items=["Grymforge"]) # Level 6
        _connect(blighted_village, underdark, "Blighted Village to Underdark", world, level_fragments=10, block_items=["Underdark"]) # Level 5
        _connect(blighted_village, monastery, "Blighted Village to Monastery", world, level_fragments=18, block_items=["Goblin Camp", "Mountain Pass"]) # Level 7
        _connect(monastery, creche, "Monastery to Creche", world, block_items=["Creche"])

        if (world.options.goal != world.options.goal.option_kill_inquisitor_wwargaz
            and world.options.goal != world.options.goal.option_act1_user_defined_fights):
            _connect(monastery, east_act2, "Monastery to East Act 2", world, level_fragments=22, block_items=["Act 2"]) # Level 8
            _connect(grymforge, east_act2, "Grymforge to East Act 2", world, level_fragments=22, block_items=["Goblin Camp", "Act 2"]) # Level 8
            _connect(east_act2, west_act2, "East Act 2 to West Act 2", world, level_fragments=26, block_items=["Reithwin's Mason's Guild"]) # Level 9
            _connect(east_act2, last_light, "East Act 2 to Last Light Inn", world, level_fragments=26, block_items=["Last Light Basement"]) # Level 9
            _connect(west_act2, moonrise, "West Act 2 to Moonrise Towers", world, block_items=["Moonlight Towers"])
            _connect(west_act2, shar_gauntlet, "West Act 2 to Gauntlet of Shar", world, block_items=["Underdark", "Grymforge", "Shar Trials"])
            _connect(moonrise, mindflayer, "Moonrise Towers to Mindflayer Colony", world, level_fragments=30, block_items=["Mindflayer"]) # Level 10

            if (world.options.goal != world.options.goal.option_kill_myrkul):
                _connect(mindflayer, rivington, "Mindflayer Colony to Rivington", world, block_items=["Rivington"])
                _connect(rivington, wyrms_crossing, "Rivington to Wyrm's Crossing", world, block_items=["Wyrm's Crossing"])
                _connect(wyrms_crossing, lower_city, "Wyrm's Crossing to Lower City", world, level_fragments=34, block_items=["Lower City"])
                _connect(lower_city, lower_city_sewers, "Lower City to Lower City Sewers", world, block_items=["Lower City Sewers"])
                _connect(lower_city, iron_throne, "Lower City to Iron Throne", world, block_items=["Iron Throne"])
 #               _connect(lower_city, house_of_hope, "Lower City to House of Hope", world, block_items=["House of Hope"])
                _connect(lower_city, netherbrain, "Lower City to Netherbrain", world, level_fragments=38, block_items=["Netherbrain"])