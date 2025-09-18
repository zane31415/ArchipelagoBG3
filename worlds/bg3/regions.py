from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import BG3World

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


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
    iron_throne = Region("Iron Throne", world.player, world.multiworld)
    netherbrain = Region("Netherbrain", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [tutorial, beach, crypt, grove, blighted_village, goblin_camp, waukeen, hag, underdark, grymforge, monastery, creche, \
            east_act2, west_act2, last_light, moonrise, shar_gauntlet, mindflayer, \
            rivington, wyrms_crossing, lower_city, lower_city_sewers, iron_throne, netherbrain]

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: BG3World) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
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
    iron_throne = world.get_region("Iron Throne")
    netherbrain = world.get_region("Netherbrain")

    tutorial.connect(beach, "Tutorial to Beach", lambda state: state.has("Level Up", world.player))
    beach.connect(crypt, "Beach to Crypt")
    beach.connect(grove, "Beach to Grove", lambda state: state.has("Level Up", world.player, 2))
    beach.connect(blighted_village, "Beach to Blighted Village", lambda state: state.has("Level Up", world.player, 2))
    blighted_village.connect(goblin_camp, "Blighted Village to Goblin Camp", lambda state: state.has("Level Up", world.player, 4))
    blighted_village.connect(hag, "Blighted Village to Hag", lambda state: state.has("Level Up", world.player, 4))
    blighted_village.connect(waukeen, "Blighted Village to Waukeen", lambda state: state.has("Level Up", world.player, 3))

    if (world.options.goal != world.options.goal.option_rescue_halsin):
        goblin_camp.connect(underdark, "Goblin Camp to Underdark")
        underdark.connect(grymforge, "Underdark to Grymforge", lambda state: state.has("Level Up", world.player, 5))
        blighted_village.connect(underdark, "Blighted Village to Underdark", lambda state: state.has("Level Up", world.player, 4))
        blighted_village.connect(monastery, "Blighted Village to Monastery", lambda state: state.has("Level Up", world.player, 6))
        monastery.connect(creche, "Monastery to Creche")

        if (world.options.goal != world.options.goal.option_kill_inquisitor_wwargaz):
            monastery.connect(east_act2, "Monastery to East Act 2", lambda state: state.has("Level Up", world.player, 7))
            grymforge.connect(east_act2, "Grymforge to East Act 2", lambda state: state.has("Level Up", world.player, 7))
            east_act2.connect(west_act2, "East Act 2 to West Act 2", lambda state: state.has("Level Up", world.player, 8))
            east_act2.connect(last_light, "East Act 2 to Last Light Inn")
            west_act2.connect(moonrise, "West Act 2 to Moonrise Towers")
            west_act2.connect(shar_gauntlet, "West Act 2 to Gauntlet of Shar")
            moonrise.connect(mindflayer, "Moonrise Towers to Mindflayer Colony", lambda state: state.has("Level Up", world.player, 9))

            if (world.options.goal != world.options.goal.option_kill_myrkul):
                mindflayer.connect(rivington, "Mindflayer Colony to Rivington")
                rivington.connect(wyrms_crossing, "Rivington to Wyrm's Crossing")
                wyrms_crossing.connect(lower_city, "Wyrm's Crossing to Lower City", lambda state: state.has("Level Up", world.player, 10))
                lower_city.connect(lower_city_sewers, "Lower City to Lower City Sewers")
                lower_city.connect(iron_throne, "Lower City to Iron Throne")
                lower_city.connect(netherbrain, "Lower City to Netherbrain", lambda state: state.has("Level Up", world.player, 11))
