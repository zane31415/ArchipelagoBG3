
from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import BG3World

from .locationids import LOCATION_NAME_TO_ID, LOCATION_NAME_ID_REGION
from .bg3_locations import BG3_LOCATION_LIST

BG3_LOCATION_TO_AP_LOCATIONS = {item[0]: item[1] for item in BG3_LOCATION_LIST}

class BG3Location(Location):
    game = "Baldur's Gate 3"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: BG3World) -> None:
    create_regular_locations(world)


def create_regular_locations(world: BG3World) -> None:
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

    tutorial_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'tutorial'):
            tutorial_location_names.append(loc[0])
    tutorial_locations = get_location_names_with_ids(tutorial_location_names)
    tutorial.add_locations(tutorial_locations, BG3Location)

    beach_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'beach'):
            beach_location_names.append(loc[0])
    beach_locations = get_location_names_with_ids(beach_location_names)
    beach.add_locations(beach_locations, BG3Location)

    crypt_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'crypt'):
            crypt_location_names.append(loc[0])
    crypt_locations = get_location_names_with_ids(crypt_location_names)
    crypt.add_locations(crypt_locations, BG3Location)

    grove_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'grove'):
            grove_location_names.append(loc[0])
    grove_locations = get_location_names_with_ids(grove_location_names)
    grove.add_locations(grove_locations, BG3Location)

    blighted_village_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'blighted_village'):
            blighted_village_location_names.append(loc[0])
    blighted_village_locations = get_location_names_with_ids(blighted_village_location_names)
    blighted_village.add_locations(blighted_village_locations, BG3Location)

    goblin_camp_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'goblin_camp'):
            goblin_camp_location_names.append(loc[0])
    goblin_camp_locations = get_location_names_with_ids(goblin_camp_location_names)
    goblin_camp.add_locations(goblin_camp_locations, BG3Location)

    waukeen_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'waukeen'):
            waukeen_location_names.append(loc[0])
    waukeen_locations = get_location_names_with_ids(waukeen_location_names)
    waukeen.add_locations(waukeen_locations, BG3Location)

    hag_location_names = []
    for loc in LOCATION_NAME_ID_REGION:
        if (loc[2] == 'hag'):
            hag_location_names.append(loc[0])
    hag_locations = get_location_names_with_ids(hag_location_names)
    hag.add_locations(hag_locations, BG3Location)

    # Done with Halsin goal. Following additions are for other goals.
    if (world.options.goal != world.options.goal.option_rescue_halsin):
        underdark_locations = get_location_names_with_ids(
            ["Gale: Fed a Second Item",
            "Gale: Fed a Third Item",
            "Gale: Told Backstory"]
        )
        underdark.add_locations(underdark_locations, BG3Location)
        creche_locations = get_location_names_with_ids(
            ["Gale: Met Elminster"]
        )
        creche.add_locations(creche_locations, BG3Location)

    if (world.options.goal == world.options.goal.option_rescue_halsin):
        goblin_camp.add_event("Victory_Halsin", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_kill_inquisitor_wwargaz):
        creche.add_event("Victory_Wwargaz", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_kill_myrkul):
        mindflayer.add_event("Victory_Myrkul", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    else:
        netherbrain.add_event("Victory_Netherbrain", "Victory", location_type=BG3Location, item_type=items.BG3Item)
