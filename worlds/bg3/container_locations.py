"""Containersanity wiring: turn containers.py rows into AP locations.

containers.py is *generated* data (every container instance placed in a level,
with its instance UUID, region and world position). This module is the
hand-written glue that turns those rows into the three shapes the rest of the
world already speaks:

    CONTAINER_LOCATION_ID_REGION      like locationids.LOCATION_NAME_ID_REGION
    CONTAINER_LOCATION_NAME_TO_ID     like locationids.LOCATION_NAME_TO_ID
    CONTAINER_GAME_EVENT_TO_LOCATIONS like bg3_locations.BG3_LOCATION_LIST's map

locations.py merges all three, so the existing per-region location loops and
the client's out-file lookup pick containers up with no further changes.

IDs start at CONTAINER_ID_BASE because locations.isSanityActive() already
reserves everything >= 100000 for containersanity (and only creates them when
the option is set to 2 -- option_i_suppose_if_you_insist).

Game side: the Lua "Opened" listener writes "Container-<instance uuid>" into
ap_out.json, which is the key of CONTAINER_GAME_EVENT_TO_LOCATIONS.

Scope note: NAME_TO_ID and the game-event map carry *every* row, so the client
can always resolve something the game reports even if this seed didn't create
that location. ID_REGION -- the list locations.py actually creates from --
carries only containers.select(), which drops cinematic-only levels (flag "C")
and variant/duplicate levels (flag "V"); those are not reachable in a normal
playthrough, so an item placed there would be lost.
"""
from __future__ import annotations

from .containers import BG3_CONTAINER_LIST, REGION_DISPLAY, location_name, select

CONTAINER_ID_BASE = 100000


def container_location_name(row: list) -> str:
    """AP location name for a container row, e.g. "Emerald Grove: Burlap Sack 2 (195, 471)"."""
    return location_name(row)


def container_location_id(row: list) -> int:
    return CONTAINER_ID_BASE + row[0]


def container_game_event(row: list) -> str:
    """What the mod writes into ap_out.json when this container is opened."""
    return "Container-" + row[1]


CONTAINER_LOCATION_NAME_TO_ID = {
    container_location_name(row): container_location_id(row)
    for row in BG3_CONTAINER_LIST
}

CONTAINER_GAME_EVENT_TO_LOCATIONS = {
    container_game_event(row): [container_location_name(row)]
    for row in BG3_CONTAINER_LIST
}

# Fourth field is the character-tag list create_regular_locations filters on;
# containers are never character-specific, so it is always empty.
CONTAINER_LOCATION_ID_REGION = [
    [container_location_name(row), container_location_id(row), row[5], []]
    for row in select()
]
