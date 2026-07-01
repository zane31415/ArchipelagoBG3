from collections.abc import Mapping
from typing import Any, ClassVar

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, options, regions, rules, web_world, settings


# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# it is common to split up world functionality into multiple files.
# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class BG3World(World):
    """
    Baldur's Gate 3 is a large adventure game modeled after Dungeons and Dragons 5th edition.
    """
    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    game = "Baldur's Gate 3"

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.BG3WebWorld()

    # This is how we associate the options defined in our options.py with our world.
    options_dataclass = options.BG3Options
    options: options.BG3Options  # Common mistake: This has to be a colon (:), not an equals sign (=).

    settings: ClassVar[settings.BG3Settings]

    # Universal Tracker integration. UT reads this dict to wire up its map
    # tab. We use an external-pack layout (the actual pack zip lives on
    # disk outside the apworld, path supplied via the ut_pack_path
    # setting). Section names in the pack match AP location names
    # exactly, so no `poptracker_name_mapping` is needed.
    tracker_world: ClassVar = {
        "external_pack_key": "ut_pack_path",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": "locations/locations.json",
    }

    # Tell UT this world can re-generate from slot_data alone, without the
    # player's YAML on disk. Requires fill_slot_data to carry every
    # generation-affecting option (see _UT_GEN_OPTION_KEYS below),
    # interpret_slot_data to signal the re-gen path, and generate_early
    # to read the passthrough back into self.options before the rest of
    # generation runs.
    ut_can_gen_without_yaml = True

    # Names of options that affect generation (location creation, item
    # pool composition, rule fan-out). Sent in slot_data so UT can
    # rebuild the world from the server without needing the original
    # YAML, and re-applied in generate_early during the UT re-gen pass.
    # Keep in sync with the option reads in items.py / locations.py.
    _UT_GEN_OPTION_KEYS: ClassVar = (
        "goal", "sync_method", "user_defined_fights", "deathlink",
        "killsanity", "questsanity", "containersanity",
        "statsanity", "statsanity_boost_by",
        "add_act1a_treasure", "add_act1b_treasure",
        "add_act2_treasure", "add_act3_treasure",
        "trim_treasure_method", "additional_level_ups",
        "traps_percentage", "enabled_traps", "block_entrances",
    )

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Tutorial"

    def generate_early(self) -> None:
        # UT re-gen passthrough: restore options recorded in slot_data.
        re_gen = getattr(self.multiworld, "re_gen_passthrough", None)
        if re_gen and self.game in re_gen:
            slot_data = re_gen[self.game]
            for key in self._UT_GEN_OPTION_KEYS:
                if key not in slot_data:
                    continue
                opt = getattr(self.options, key, None)
                if opt is None:
                    continue
                setattr(self.options, key, opt.from_any(slot_data[key]))
            if "death_link" in slot_data:
                self.options.deathlink = self.options.deathlink.from_any(
                    slot_data["death_link"]
                )

        if self.options.block_entrances == 1:
            self.multiworld.early_items[self.player]["Nautiloid Control Panel"] = 1

    @staticmethod
    def interpret_slot_data(slot_data: Mapping[str, Any]) -> Mapping[str, Any]:
        # Returning the dict (rather than mutating `self`) tells UT to
        # do a re-generation pass with `re_gen_passthrough` populated.
        # `generate_early` then loads the recorded options. See
        # UniversalTracker/worlds/tracker/docs/apworld-integration.md
        # "Generating without a YAML".
        return slot_data

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, create_items.
    # For better structure and readability, we put each of these in their own file.
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, the same one that create_items is in.
    def create_item(self, name: str) -> items.BG3Item:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        slot_data = self.options.as_dict(*self._UT_GEN_OPTION_KEYS)
        slot_data["death_link"] = slot_data.pop("deathlink")
        slot_data["seed_name"] = str(self.multiworld.seed_name)
        return slot_data