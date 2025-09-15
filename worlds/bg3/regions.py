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
    overworld = Region("Overworld", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [tutorial, overworld]

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: BG3World) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    tutorial = world.get_region("Tutorial")
    overworld = world.get_region("Overworld")

    tutorial.connect(overworld, "Tutorial to Overworld", lambda state: state.has("Level Up", world.player))