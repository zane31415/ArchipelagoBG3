
from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import BG3World

from .locationids import LOCATION_NAME_TO_ID, LOCATION_NAME_ID_REGION
from .bg3_locations import BG3_LOCATION_LIST
from .container_locations import (
    CONTAINER_GAME_EVENT_TO_LOCATIONS,
    CONTAINER_LOCATION_ID_REGION,
    CONTAINER_LOCATION_NAME_TO_ID,
)

# Containersanity rides on the same three tables as everything else; merging
# here means the per-region loops below and the client's out-file lookup need
# no container-specific code. isSanityActive() is what actually gates creation.
LOCATION_NAME_TO_ID = {**LOCATION_NAME_TO_ID, **CONTAINER_LOCATION_NAME_TO_ID}
LOCATION_NAME_ID_REGION = LOCATION_NAME_ID_REGION + CONTAINER_LOCATION_ID_REGION

BG3_LOCATION_TO_AP_LOCATIONS = {item[0]: item[1] for item in BG3_LOCATION_LIST}
BG3_LOCATION_TO_AP_LOCATIONS.update(CONTAINER_GAME_EVENT_TO_LOCATIONS)

class BG3Location(Location):
    game = "Baldur's Gate 3"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: BG3World) -> None:
    create_regular_locations(world)

def isSanityActive(locId: int, world: BG3World) -> bool:
    if (locId < 10000 and world.options.questsanity == 1):
        return True
    if (locId >= 10000 and locId < 100000 and world.options.killsanity == 1):
         return True
    if (locId >= 100000 and world.options.containersanity == 2):
         return True
    return False

def create_regular_locations(world: BG3World) -> None:
    # Character-gating: each locationids row carries a 4th field, a list of
    # character tags. A location tagged with a character the player left out of
    # CharactersInLogic is not created here. Untagged locations (empty list)
    # are always kept. Note LOCATION_NAME_TO_ID stays the FULL set on purpose,
    # so the client can still map a game event to a location it simply doesn't
    # have this game and move on -- no error.
    in_logic = set(world.options.characters_in_logic.value)
    allowed_locs = [
        loc for loc in LOCATION_NAME_ID_REGION
        if all(tag in in_logic for tag in (loc[3] if len(loc) > 3 else []))
    ]

    tutorial = world.get_region("Tutorial")
    beach = world.get_region("Beach")
    crypt = world.get_region("Crypt")
    grove = world.get_region("Grove")
    blighted_village = world.get_region("Blighted Village")
    underwell = world.get_region("Underwell")
    goblin_camp = world.get_region("Goblin Camp")
    inside_goblin_camp = world.get_region("Inside Goblin Camp")
    waukeen = world.get_region("Waukeen")
    zhentarim_basement = world.get_region("Zhentarim Basement")
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

    astral = world.get_region("Astral Plane")
    rivington = world.get_region("Rivington")
    wyrms_crossing = world.get_region("Wyrm's Crossing")
    lower_city = world.get_region("Lower City")
    lower_city_sewers = world.get_region("Lower City Sewers")
    ancient_lair = world.get_region("Ancient Lair")
    undercity_ruins = world.get_region("Undercity Ruins")
    elfsong_basement = world.get_region("Elfsong Basement")
    murder_tribunal = world.get_region("Murder Tribunal")
    endgame = world.get_region("Endgame")
    # house_of_hope = world.get_region("House of Hope")
    iron_throne = world.get_region("Iron Throne")

    tutorial_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'tutorial' and isSanityActive(loc[1], world)):
            tutorial_location_names.append(loc[0])
    tutorial_locations = get_location_names_with_ids(tutorial_location_names)
    tutorial.add_locations(tutorial_locations, BG3Location)

    beach_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'beach' and isSanityActive(loc[1], world)):
            beach_location_names.append(loc[0])
    beach_locations = get_location_names_with_ids(beach_location_names)
    beach.add_locations(beach_locations, BG3Location)

    crypt_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'crypt' and isSanityActive(loc[1], world)):
            crypt_location_names.append(loc[0])
    crypt_locations = get_location_names_with_ids(crypt_location_names)
    crypt.add_locations(crypt_locations, BG3Location)

    grove_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'grove' and isSanityActive(loc[1], world)):
            grove_location_names.append(loc[0])
    grove_locations = get_location_names_with_ids(grove_location_names)
    grove.add_locations(grove_locations, BG3Location)

    blighted_village_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'blighted_village' and isSanityActive(loc[1], world)):
            blighted_village_location_names.append(loc[0])
    blighted_village_locations = get_location_names_with_ids(blighted_village_location_names)
    blighted_village.add_locations(blighted_village_locations, BG3Location)

    underwell_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'underwell' and isSanityActive(loc[1], world)):
            underwell_location_names.append(loc[0])
    underwell_locations = get_location_names_with_ids(underwell_location_names)
    underwell.add_locations(underwell_locations, BG3Location)

    goblin_camp_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'goblin_camp' and isSanityActive(loc[1], world)):
            goblin_camp_location_names.append(loc[0])
    goblin_camp_locations = get_location_names_with_ids(goblin_camp_location_names)
    goblin_camp.add_locations(goblin_camp_locations, BG3Location)

    inside_goblin_camp_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'inside_goblin_camp' and isSanityActive(loc[1], world)):
            inside_goblin_camp_location_names.append(loc[0])
    inside_goblin_camp_locations = get_location_names_with_ids(inside_goblin_camp_location_names)
    inside_goblin_camp.add_locations(inside_goblin_camp_locations, BG3Location)

    waukeen_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'waukeen' and isSanityActive(loc[1], world)):
            waukeen_location_names.append(loc[0])
    waukeen_locations = get_location_names_with_ids(waukeen_location_names)
    waukeen.add_locations(waukeen_locations, BG3Location)

    zhentarim_basement_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'zhentarim_basement' and isSanityActive(loc[1], world)):
            zhentarim_basement_location_names.append(loc[0])
    zhentarim_basement_locations = get_location_names_with_ids(zhentarim_basement_location_names)
    zhentarim_basement.add_locations(zhentarim_basement_locations, BG3Location)

    hag_location_names = []
    for loc in allowed_locs:
        if (loc[2] == 'hag' and isSanityActive(loc[1], world)):
            hag_location_names.append(loc[0])
    hag_locations = get_location_names_with_ids(hag_location_names)
    hag.add_locations(hag_locations, BG3Location)

    # Done with Halsin goal. Following additions are for other goals.
    if (world.options.goal != world.options.goal.option_rescue_halsin):
        underdark_location_names = []
        for loc in allowed_locs:
            if (loc[2] == 'underdark' and isSanityActive(loc[1], world)):
                underdark_location_names.append(loc[0])
        underdark_locations = get_location_names_with_ids(underdark_location_names)
        underdark.add_locations(underdark_locations, BG3Location)

        grymforge_location_names = []
        for loc in allowed_locs:
            if (loc[2] == 'grymforge' and isSanityActive(loc[1], world)):
                grymforge_location_names.append(loc[0])
        grymforge_locations = get_location_names_with_ids(grymforge_location_names)
        grymforge.add_locations(grymforge_locations, BG3Location)

        monastery_location_names = []
        for loc in allowed_locs:
            if (loc[2] == 'monastery' and isSanityActive(loc[1], world)):
                monastery_location_names.append(loc[0])
        monastery_locations = get_location_names_with_ids(monastery_location_names)
        monastery.add_locations(monastery_locations, BG3Location)

        creche_location_names = []
        for loc in allowed_locs:
            if (loc[2] == 'creche' and isSanityActive(loc[1], world)):
                creche_location_names.append(loc[0])
        creche_locations = get_location_names_with_ids(creche_location_names)
        creche.add_locations(creche_locations, BG3Location)

        # Done with Wwargaz goal. Following additions are for other goals.
        if (world.options.goal != world.options.goal.option_kill_inquisitor_wwargaz 
            and world.options.goal != world.options.goal.option_act1_user_defined_fights):
            east_act2_location_names = []
            for loc in allowed_locs:
                if (loc[2] == 'east_act2' and isSanityActive(loc[1], world)):
                    east_act2_location_names.append(loc[0])
            east_act2_location = get_location_names_with_ids(east_act2_location_names)
            east_act2.add_locations(east_act2_location, BG3Location)

            west_act2_location_names = []
            for loc in allowed_locs:
                if (loc[2] == 'west_act2' and isSanityActive(loc[1], world)):
                    west_act2_location_names.append(loc[0])
            west_act2_location = get_location_names_with_ids(west_act2_location_names)
            west_act2.add_locations(west_act2_location, BG3Location)

            last_light_location_names = []
            for loc in allowed_locs:
                if (loc[2] == 'last_light' and isSanityActive(loc[1], world)):
                    last_light_location_names.append(loc[0])
            last_light_locations = get_location_names_with_ids(last_light_location_names)
            last_light.add_locations(last_light_locations, BG3Location)

            shar_gauntlet_location_names = []
            for loc in allowed_locs:
                if (loc[2] == 'shar_gauntlet' and isSanityActive(loc[1], world)):
                    shar_gauntlet_location_names.append(loc[0])
            shar_gauntlet_locations = get_location_names_with_ids(shar_gauntlet_location_names)
            shar_gauntlet.add_locations(shar_gauntlet_locations, BG3Location)

            moonrise_location_names = []
            for loc in allowed_locs:
                if (loc[2] == 'moonrise' and isSanityActive(loc[1], world)):
                    moonrise_location_names.append(loc[0])
            moonrise_locations = get_location_names_with_ids(moonrise_location_names)
            moonrise.add_locations(moonrise_locations, BG3Location)

            mindflayer_location_names = []
            for loc in allowed_locs:
                if (loc[2] == 'mindflayer' and isSanityActive(loc[1], world)):
                    mindflayer_location_names.append(loc[0])
            mindflayer_locations = get_location_names_with_ids(mindflayer_location_names)
            mindflayer.add_locations(mindflayer_locations, BG3Location)
            
            if (world.options.goal != world.options.goal.option_kill_myrkul 
            and world.options.goal != world.options.goal.option_act2_user_defined_fights):
                astral_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'astral' and isSanityActive(loc[1], world)):
                        astral_location_names.append(loc[0])
                astral_location = get_location_names_with_ids(astral_location_names)
                astral.add_locations(astral_location, BG3Location)
                
                rivington_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'rivington' and isSanityActive(loc[1], world)):
                        rivington_location_names.append(loc[0])
                rivington_location = get_location_names_with_ids(rivington_location_names)
                rivington.add_locations(rivington_location, BG3Location)

                wyrms_crossing_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'wyrms_crossing' and isSanityActive(loc[1], world)):
                        wyrms_crossing_location_names.append(loc[0])
                wyrms_crossing_location = get_location_names_with_ids(wyrms_crossing_location_names)
                wyrms_crossing.add_locations(wyrms_crossing_location, BG3Location)

                lower_city_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'lower_city' and isSanityActive(loc[1], world)):
                        lower_city_location_names.append(loc[0])
                lower_city_location = get_location_names_with_ids(lower_city_location_names)
                lower_city.add_locations(lower_city_location, BG3Location)

                lower_city_sewers_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'lower_city_sewers' and isSanityActive(loc[1], world)):
                        lower_city_sewers_location_names.append(loc[0])
                lower_city_sewers_location = get_location_names_with_ids(lower_city_sewers_location_names)
                lower_city_sewers.add_locations(lower_city_sewers_location, BG3Location)

                ancient_lair_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'ancient_lair' and isSanityActive(loc[1], world)):
                        ancient_lair_location_names.append(loc[0])
                ancient_lair_location = get_location_names_with_ids(ancient_lair_location_names)
                ancient_lair.add_locations(ancient_lair_location, BG3Location)

                undercity_ruins_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'undercity_ruins' and isSanityActive(loc[1], world)):
                        undercity_ruins_location_names.append(loc[0])
                undercity_ruins_location = get_location_names_with_ids(undercity_ruins_location_names)
                undercity_ruins.add_locations(undercity_ruins_location, BG3Location)

                elfsong_basement_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'elfsong_basement' and isSanityActive(loc[1], world)):
                        elfsong_basement_location_names.append(loc[0])
                elfsong_basement_location = get_location_names_with_ids(elfsong_basement_location_names)
                elfsong_basement.add_locations(elfsong_basement_location, BG3Location)

                murder_tribunal_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'murder_tribunal' and isSanityActive(loc[1], world)):
                        murder_tribunal_location_names.append(loc[0])
                murder_tribunal_location = get_location_names_with_ids(murder_tribunal_location_names)
                murder_tribunal.add_locations(murder_tribunal_location, BG3Location)

                iron_throne_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'iron_throne' and isSanityActive(loc[1], world)):
                        iron_throne_location_names.append(loc[0])
                iron_throne_location = get_location_names_with_ids(iron_throne_location_names)
                iron_throne.add_locations(iron_throne_location, BG3Location)

                endgame_location_names = []
                for loc in allowed_locs:
                    if (loc[2] == 'endgame' and isSanityActive(loc[1], world)):
                        endgame_location_names.append(loc[0])
                endgame_location = get_location_names_with_ids(endgame_location_names)
                endgame.add_locations(endgame_location, BG3Location)


    if (world.options.goal == world.options.goal.option_rescue_halsin):
        goblin_camp.add_event("Victory_Halsin", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_kill_inquisitor_wwargaz):
        creche.add_event("Victory_Wwargaz", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_act1_user_defined_fights):
        creche.add_event("Victory_All_Bosses", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_act2_user_defined_fights):
        mindflayer.add_event("Victory_All_Bosses", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_act3_user_defined_fights):
        endgame.add_event("Victory_All_Bosses", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_kill_myrkul):
        mindflayer.add_event("Victory_Myrkul", "Victory", location_type=BG3Location, item_type=items.BG3Item)
    elif (world.options.goal == world.options.goal.option_kill_nether_brain):
        endgame.add_event("Victory_Netherbrain", "Victory", location_type=BG3Location, item_type=items.BG3Item)
