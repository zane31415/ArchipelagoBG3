from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import BG3World

from .equipment import EQUIPMENT

FILLER_EQUIPMENT = [
    ["Lockpick", "e32a200c-5b63-414d-ae57-00e7b38f125b"],
    ["Supply Pack", "a24a2ca2-a213-424c-833d-47c79934c0ce"],
    ["Trap Disarm Pack", "22c74b5e-bef2-41b1-b9ed-f4acc766d4ee"],
    ["Is that blood? No, nevermind.", "809f228e-8d2b-46b8-8a33-51181505bc61"],
    # Gold wire format is "Gold-<digits>" (the client appends "-n" to make
    # each copy unique). Historically the mod parsed exactly six zero-padded
    # digits; current mod versions accept any digit count, but keep padding
    # to six so old mods still grant the right amount.
    ["100 Gold", "Gold-000100"],
    ["200 Gold", "Gold-000200"],
    ["Potion of Healing", "d47006e9-8a51-453d-b200-9e0d42e9bbab"],
]

TRAP_OPTIONS = [
    ["Monster Spawn Trap", "Trap-Monster"],
    ["Bleeding Trap", "Trap-Bleeding"],
    ["Stunned Trap", "Trap-Stun"],
    ["Confusion Trap", "Trap-Confusion"],
    ["Sussur Trap", "Trap-Sussur"],
    ["Clown Trap", "Trap-Clown"],
    ["Overburdened Trap", "Trap-Overburdened"]
]

# Traps the game mod actually implements. The others are silently consumed
# with no effect by the mod's Lua, so generation strips them from the pool
# (with a warning) rather than handing out items that do nothing.
IMPLEMENTED_TRAPS = {"Monster", "Bleeding", "Stun"}
TRAP_KEY_TO_ITEM_NAME = {
    "Monster": "Monster Spawn Trap",
    "Bleeding": "Bleeding Trap",
    "Stun": "Stunned Trap",
    "Confusion": "Confusion Trap",
    "Sussur": "Sussur Trap",
    "Clown": "Clown Trap",
    "Overburdened": "Overburdened Trap",
}

#[game item name, id in BG3, int id in AP, classification, filter level]
# Filter levels: 0 (pre-Halsin), 1 (Act 1), 2 (Act 2), 3 (Act 3)
ITEM_TUPLES = [
    ["Level Fragment", "LevelUp", 1, ItemClassification.progression, 0],
    ["Boots of Speed", "8b22d15a-85bb-4c8d-90cf-a773fc451eac", 2, ItemClassification.progression, 1],
    ["Shadow Lantern", "c9ebcfae-8c9a-4acc-8a30-da7830b32121", 3, ItemClassification.progression, 2],
    ["Spear of Night", "d590884d-55a2-4136-9777-531ee7d53f7e", 4, ItemClassification.progression, 2],
    ["Strength Stat Boost", "StrStatBoost", 5, ItemClassification.progression, 0],
    ["Dexterity Stat Boost", "DexStatBoost", 6, ItemClassification.progression, 0],
    ["Constitution Stat Boost", "ConStatBoost", 7, ItemClassification.progression, 0],
    ["Intelligence Stat Boost", "IntStatBoost", 8, ItemClassification.progression, 0],
    ["Wisdom Stat Boost", "WisStatBoost", 9, ItemClassification.progression, 0],
    ["Charisma Stat Boost", "ChaStatBoost", 10, ItemClassification.progression, 0],
    ["Slot 1 Strength Boost", "Slot1StrStatBoost", 11, ItemClassification.progression, 0],
    ["Slot 1 Dexterity Boost", "Slot1DexStatBoost", 12, ItemClassification.progression, 0],
    ["Slot 1 Constitution Boost", "Slot1ConStatBoost", 13, ItemClassification.progression, 0],
    ["Slot 1 Intelligence Boost", "Slot1IntStatBoost", 14, ItemClassification.progression, 0],
    ["Slot 1 Wisdom Boost", "Slot1WisStatBoost", 15, ItemClassification.progression, 0],
    ["Slot 1 Charisma Boost", "Slot1ChaStatBoost", 16, ItemClassification.progression, 0],
    ["Slot 2 Strength Boost", "Slot2StrStatBoost", 17, ItemClassification.progression, 0],
    ["Slot 2 Dexterity Boost", "Slot2DexStatBoost", 18, ItemClassification.progression, 0],
    ["Slot 2 Constitution Boost", "Slot2ConStatBoost", 19, ItemClassification.progression, 0],
    ["Slot 2 Intelligence Boost", "Slot2IntStatBoost", 20, ItemClassification.progression, 0],
    ["Slot 2 Wisdom Boost", "Slot2WisStatBoost", 21, ItemClassification.progression, 0],
    ["Slot 2 Charisma Boost", "Slot2ChaStatBoost", 22, ItemClassification.progression, 0],
    ["Slot 3 Strength Boost", "Slot3StrStatBoost", 23, ItemClassification.progression, 0],
    ["Slot 3 Dexterity Boost", "Slot3DexStatBoost", 24, ItemClassification.progression, 0],
    ["Slot 3 Constitution Boost", "Slot3ConStatBoost", 25, ItemClassification.progression, 0],
    ["Slot 3 Intelligence Boost", "Slot3IntStatBoost", 26, ItemClassification.progression, 0],
    ["Slot 3 Wisdom Boost", "Slot3WisStatBoost", 27, ItemClassification.progression, 0],
    ["Slot 3 Charisma Boost", "Slot3ChaStatBoost", 28, ItemClassification.progression, 0],
    ["Slot 4 Strength Boost", "Slot4StrStatBoost", 29, ItemClassification.progression, 0],
    ["Slot 4 Dexterity Boost", "Slot4DexStatBoost", 30, ItemClassification.progression, 0],
    ["Slot 4 Constitution Boost", "Slot4ConStatBoost", 31, ItemClassification.progression, 0],
    ["Slot 4 Intelligence Boost", "Slot4IntStatBoost", 32, ItemClassification.progression, 0],
    ["Slot 4 Wisdom Boost", "Slot4WisStatBoost", 33, ItemClassification.progression, 0],
    ["Slot 4 Charisma Boost", "Slot4ChaStatBoost", 34, ItemClassification.progression, 0],
    ["Nautiloid Control Panel", "Gate-ExitNautiloid", 100, ItemClassification.progression, 0],
    ["Wither's Crypt", "Gate-WithersCrypt", 101, ItemClassification.progression, 0],
    ["Blighted Village Well", "Gate-RuinedVillageWell", 102, ItemClassification.progression, 0],
    ["Goblin Camp", "Gate-GoblinCamp", 103, ItemClassification.progression, 0],
    ["Underdark", "Gate-Underdark", 104, ItemClassification.progression, 1],
    ["Hag's Fireplace", "Gate-HagsFireplace", 105, ItemClassification.progression, 1],
    ["Zhentarim Basement", "Gate-ZhentarimBasement", 106, ItemClassification.progression, 1],
    ["Grymforge", "Gate-Grymforge", 107, ItemClassification.progression, 1],
    ["Mountain Pass", "Gate-MountainPass", 108, ItemClassification.progression, 1],
    ["Creche", "Gate-Creche", 109, ItemClassification.progression, 1],
    ["Act 2", "Gate-Act2", 110, ItemClassification.progression, 2],
    ["Last Light Basement", "Gate-LastLightBasement", 111, ItemClassification.progression, 2],
    ["Reithwin's Mason's Guild", "Gate-ReithwinsMasonsGuild", 112, ItemClassification.progression, 2],
    ["Shar Trials", "Gate-SharTrials", 113, ItemClassification.progression, 2],
    ["Progressive Moonlight Towers", "Gate-ProgressiveMoonlightTowers", 114, ItemClassification.progression, 2],
    ["Act 3", "Gate-Act3", 115, ItemClassification.progression, 3],
    
] + [[item[0], item[1], index + 1000, ItemClassification.useful, item[2]] for index, item in enumerate(EQUIPMENT)] \
  + [[item[0], item[1], index + 5000, ItemClassification.filler, 0] for index, item in enumerate(FILLER_EQUIPMENT)] \
  + [[item[0], item[1], index + 7000, ItemClassification.trap, 0] for index, item in enumerate(TRAP_OPTIONS)] 
# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {item[0]: item[2] for item in ITEM_TUPLES}
ID_TO_ITEM_NAME = {item[2]: item[0] for item in ITEM_TUPLES}
AP_ITEM_TO_BG3_ID = {item[0]: item[1] for item in ITEM_TUPLES}
ID_TO_AP_ITEM = {item[2]: item[1] for item in ITEM_TUPLES}
DEFAULT_ITEM_CLASSIFICATIONS = {item[0]: item[3] for item in ITEM_TUPLES}
IS_DUPEABLE = {item[1]: True for item in FILLER_EQUIPMENT}

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class BG3Item(Item):
    game = "Baldur's Gate 3"


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: BG3World) -> str:
    if (world.random.randint(0, 100) < world.options.traps_percentage):
        traps = sorted(trap for trap in world.options.enabled_traps if trap in IMPLEMENTED_TRAPS)
        if traps:
            trap = traps[world.random.randint(0, len(traps) - 1)]
            return TRAP_KEY_TO_ITEM_NAME[trap]
        # All enabled traps are unimplemented: fall through to normal filler.
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

    if world.options.traps_percentage > 0:
        unimplemented = sorted(t for t in world.options.enabled_traps if t not in IMPLEMENTED_TRAPS)
        if unimplemented:
            logging.warning(
                f"BG3 ({world.player_name}): enabled traps {unimplemented} are not implemented "
                f"by the game mod yet and will not be added to the pool.")

    itempool: list[Item] = []

    levelups_to_add = 10  # Base number of level ups - enough to reach level 5
    if (world.options.goal == world.options.goal.option_kill_inquisitor_wwargaz or world.options.goal == world.options.goal.option_act1_user_defined_fights):
        levelups_to_add = 22 # To reach level 8
    elif (world.options.goal == world.options.goal.option_kill_myrkul or world.options.goal == world.options.goal.option_act2_user_defined_fights):
        levelups_to_add = 30 # To reach level 10
    elif (world.options.goal == world.options.goal.option_kill_nether_brain or world.options.goal == world.options.goal.option_act3_user_defined_fights):
        levelups_to_add = 38 # To reach level 12

    levelups_to_add = levelups_to_add + world.options.additional_level_ups
    itempool += [world.create_item("Level Fragment") for _ in range(levelups_to_add)]
    # Here we would add other progression items as we have them.
    if (world.options.block_entrances == 1):
        itempool += [world.create_item("Nautiloid Control Panel")]
        itempool += [world.create_item("Wither's Crypt")]
        itempool += [world.create_item("Goblin Camp")]
        itempool += [world.create_item("Hag's Fireplace")]
        itempool += [world.create_item("Zhentarim Basement")]
        if (world.options.goal == world.options.goal.option_rescue_halsin):
            itempool += [world.create_item("Blighted Village Well")]
        else:
            itempool += [world.create_item("Underdark")]
            itempool += [world.create_item("Grymforge")]
            itempool += [world.create_item("Mountain Pass")]
            itempool += [world.create_item("Creche")]
            if (world.options.goal != world.options.goal.option_kill_inquisitor_wwargaz and world.options.goal != world.options.goal.option_act1_user_defined_fights):
                itempool += [world.create_item("Act 2")]
                itempool += [world.create_item("Last Light Basement")]
                itempool += [world.create_item("Reithwin's Mason's Guild")]
                itempool += [world.create_item("Shar Trials")]
                itempool += [world.create_item("Progressive Moonlight Towers")]
                itempool += [world.create_item("Progressive Moonlight Towers")]
                itempool += [world.create_item("Progressive Moonlight Towers")]
                itempool += [world.create_item("Progressive Moonlight Towers")]
                itempool += [world.create_item("Progressive Moonlight Towers")]
                if (world.options.goal != world.options.goal.option_kill_myrkul and world.options.goal != world.options.goal.option_act2_user_defined_fights):
                    itempool += [world.create_item("Act 3")]
           
            
    if (world.options.statsanity != world.options.statsanity.option_off):
        required_stat = 20
        if (world.options.goal == world.options.goal.option_rescue_halsin):
            required_stat = 12
        elif (world.options.goal == world.options.goal.option_kill_inquisitor_wwargaz or world.options.goal == world.options.goal.option_act1_user_defined_fights):
            required_stat = 16
        elif (world.options.goal == world.options.goal.option_kill_myrkul or world.options.goal == world.options.goal.option_act2_user_defined_fights):
            required_stat = 20
        elif (world.options.goal == world.options.goal.option_kill_nether_brain or world.options.goal == world.options.goal.option_act3_user_defined_fights):
            required_stat = 24
        stats_per_slot = (required_stat - 8) // world.options.statsanity_boost_by
        if (world.options.statsanity == world.options.statsanity.option_universal_stats or world.options.statsanity == world.options.statsanity.option_tav_only_stats):
            itempool += [world.create_item("Strength Stat Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Dexterity Stat Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Constitution Stat Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Intelligence Stat Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Wisdom Stat Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Charisma Stat Boost") for _ in range(stats_per_slot)]
        else: # party slots
            itempool += [world.create_item("Slot 1 Strength Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 1 Dexterity Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 1 Constitution Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 1 Intelligence Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 1 Wisdom Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 1 Charisma Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 2 Strength Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 2 Dexterity Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 2 Constitution Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 2 Intelligence Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 2 Wisdom Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 2 Charisma Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 3 Strength Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 3 Dexterity Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 3 Constitution Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 3 Intelligence Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 3 Wisdom Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 3 Charisma Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 4 Strength Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 4 Dexterity Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 4 Constitution Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 4 Intelligence Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 4 Wisdom Boost") for _ in range(stats_per_slot)]
            itempool += [world.create_item("Slot 4 Charisma Boost") for _ in range(stats_per_slot)]

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
