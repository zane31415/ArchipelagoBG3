from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from ..generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import BG3World


def set_all_rules(world: BG3World) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: BG3World) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    tutorial_to_overworld = world.get_entrance("Tutorial to Overworld")

    # Because the function has to be defined locally, most worlds prefer the lambda syntax.
    set_rule(tutorial_to_overworld, lambda state: state.has("Level Up", world.player))


def set_completion_condition(world: BG3World) -> None:
    # In our case, we went for the Victory event design pattern (see regions.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)