
from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import BG3World

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Tut: Learn about the Helm": 1,
    "Tut: Reach the Helm": 2,
    "Tut: Connect the Transponder": 3,
    "Tut-SH: Find Captive": 4,
    "Tut-SH: Find the Rune": 5,
    "Tut-SH: Open the Pod": 6,
    "Tut-SH: Recruit Captive": 7,
    #"Act1-Over: Woke on Beach": 8,
}

BG3_LOCATION_TO_AP_LOCATIONS = {
    "TUT_NautiloidEscape-Start":[],
    "TUT_NautiloidEscape-LearnedHelm_Laezel":["Tut: Learn about the Helm"],
    "TUT_NautiloidEscape-LearnedHelm_AltGuide":["Tut: Learn about the Helm"],
    "TUT_NautiloidEscape-LearnedHelm_Devourer":["Tut: Learn about the Helm"],
    "TUT_NautiloidEscape-ReachedHelm":["Tut: Reach the Helm"],
    "TUT_NautiloidEscape-EscapedHell":["Tut: Connect the Transponder"],
    "TUT_ShadowheartEscape-FindCaptive":["Tut-SH: Find Captive"],
    "TUT_ShadowheartEscape-UsedRune":["Tut-SH: Open the Pod"],
    "TUT_ShadowheartEscape-UsedForce":["Tut-SH: Find the Rune", "Tut-SH: Open the Pod"],
    "TUT_ShadowheartEscape-FreedAndRecruited":["Tut-SH: Recruit Captive"],
    "TUT_ShadowheartEscape-FreedDidNotRecruit":[],
    "TUT_ShadowheartEscape-FreedLeftBehind":[],
    "TUT_ShadowheartEscape-LeftBehind":[],
    "TUT_ShadowheartEscape-FoundRune":["Tut-SH: Find the Rune"],
    "GLO_Tadpole-WokeAtCrash":["Act1-Over: Woke on Beach"],

}

class BG3Location(Location):
    game = "Baldur's Gate 3"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: BG3World) -> None:
    create_regular_locations(world)


def create_regular_locations(world: BG3World) -> None:
    tutorial = world.get_region("Tutorial")
    overworld = world.get_region("Overworld")

    tutorial_locations = get_location_names_with_ids(
        ["Tut: Learn about the Helm",
        "Tut: Reach the Helm",
        "Tut: Connect the Transponder",
        "Tut-SH: Find Captive",
        "Tut-SH: Find the Rune",
        "Tut-SH: Open the Pod",
        "Tut-SH: Recruit Captive"]
    )
    tutorial.add_locations(tutorial_locations, BG3Location)
    # overworld_locations = get_location_names_with_ids(["Act1-Over: Woke on Beach"])
    overworld.add_event("Act1-Over: Woke on Beach", "Victory", location_type=BG3Location, item_type=items.BG3Item)

