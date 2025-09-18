from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import BG3World

from .equipment import EQUIPMENT

FILLER_EQUIPMENT = [
    ["Lockpick", "6d0d9e73-a922-47e8-88b8-842b977ecb20"],
    ["Supply Pack", "a24a2ca2-a213-424c-833d-47c79934c0ce"],
    ["Is that blood? No, nevermind.", "af808d7c-c8d6-4924-94a9-35bffd450803"],
    ["100 Gold", "Gold-100"],
]

#[game item name, id in BG3, int id in AP, classification, filter level]
# Filter levels: 0 (pre-Halsin), 1 (Act 1), 2 (Act 2), 3 (Act 3)
ITEM_TUPLES = [
    ["Level Up", "LevelUp", 1, ItemClassification.progression, 0],
    ["Boots of Speed", "8b22d15a-85bb-4c8d-90cf-a773fc451eac", 2, ItemClassification.progression, 1],
    ["Shadow Lantern", "c9ebcfae-8c9a-4acc-8a30-da7830b32121", 3, ItemClassification.progression, 2],
    ["Spear of Night", "d590884d-55a2-4136-9777-531ee7d53f7e", 4, ItemClassification.progression, 2],
] + [[item[0], item[1], index + 1000, ItemClassification.useful, item[2]] for index, item in enumerate(EQUIPMENT)] \
  + [[item[0], item[1], index + 5000, ItemClassification.filler, 0] for index, item in enumerate(FILLER_EQUIPMENT)]
# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {item[0]: item[2] for item in ITEM_TUPLES}
ID_TO_ITEM_NAME = {item[2]: item[0] for item in ITEM_TUPLES}
AP_ITEM_TO_BG3_ID = {item[0]: item[1] for item in ITEM_TUPLES}
ID_TO_AP_ITEM = {item[2]: item[1] for item in ITEM_TUPLES}
DEFAULT_ITEM_CLASSIFICATIONS = {item[0]: item[3] for item in ITEM_TUPLES}

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class BG3Item(Item):
    game = "Baldur's Gate 3"


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: BG3World) -> str:
    index = world.random.randint(0, len(FILLER_EQUIPMENT) - 1)
    return FILLER_EQUIPMENT[index][0]


def create_item_with_correct_classification(world: BG3World, name: str) -> BG3Item:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return BG3Item(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: BG3World) -> None:
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = []

    levelups_to_add = 4  # Base number of level ups
    if (world.options.goal == world.options.goal.option_kill_inquisitor_wwargaz):
        levelups_to_add = 7
    elif (world.options.goal == world.options.goal.option_kill_myrkul):
        levelups_to_add = 9
    elif (world.options.goal == world.options.goal.option_kill_nether_brain):
        levelups_to_add = 11

    itempool += [world.create_item("Level Up") for _ in range(levelups_to_add)]
    # Here we would add other progression items as we have them.

    # Add Treasure
    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    space_after_progression = number_of_unfilled_locations - number_of_items

    equipment_available = []
    for item in EQUIPMENT:
        if (item[2] == 0 and world.options.add_act1a_treasure) or (item[2] == 1 and world.options.add_act1b_treasure) or \
           (item[2] == 2 and world.options.add_act2_treasure) or (item[2] == 3 and world.options.add_act3_treasure):
            equipment_available.append(item)

    if space_after_progression < len(equipment_available):
        if (world.options.trim_treasure_method == world.options.trim_treasure_method.option_remove_random_treasure):
            world.random.shuffle(equipment_available)
        elif (world.options.trim_treasure_method == world.options.trim_treasure_method.option_remove_later_treasure_first):
            world.random.shuffle(equipment_available)
            equipment_available.sort(key=lambda x: x[2])
        # filter out treasure items
        itempool+= [world.create_item(equipment_available[i][0]) for i in range(space_after_progression)]
    else:
        itempool+= [world.create_item(item[0]) for item in equipment_available]

    number_of_items = len(itempool)
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
