
from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import BG3World

from .locationids import LOCATION_NAME_TO_ID
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

    beach_locations = get_location_names_with_ids(
        ["Beach-LZ: Find Lae'zel",
        "Beach-LZ: Talk to Lae'zel",
        "Beach-LZ: Get the Tieflings Away",
        "Beach-LZ: Free Lae'zel",
        "Beach-LZ: Recruit Lae'zel",
        "Astarion: Recruited",
        "Tadpole: Wake on Beach",
        "Tadpole: Talk to Lae'zel",
        "Gale: Recruited",
        "Gale: Died",
        "Gale: Listened to Projection",
        "Gale: Opened Pouch",
        "Gale: Played Flute",
        "Gale: Told Mephit his Name",
        "Gale: Resurrected",
        "Plot-Art: Notice Artefact",
        "Shart: Recruit Shadowheart",
        "Shart: Resolve Camp Fight (both live)",])
    beach.add_locations(beach_locations, BG3Location)

    crypt_locations = get_location_names_with_ids(
        ["Crypt: Learn about Crypt",
        "Crypt: Enter Crypt",
        "Crypt: Find Sarcophagus",
        "Crypt: Read Plaque",
        "Crypt: Open Sarcophagus",
        "Crypt: Talk to Withers at Camp"]
    )
    crypt.add_locations(crypt_locations, BG3Location)

    grove_locations = get_location_names_with_ids(
        ["Grove-Thief: Discover Pickpocketing",
        "Grove-Thief: Learn About Hideout",
        "Grove-Thief: Enter Hideout",
        "Grove-Thief: Get Your Stuff Back",
        "Tadpole: Learn about Nettie",
        "Tadpole: Learn about Halsin",
        "Tadpole: Learn about Priestess Gut",
        "Tadpole: See True Soul Meld/Tadpole",
        "Tadpole-Nettie: Talk to Nettie",
        "Tadpole-Nettie: Be Poisoned by Nettie",
        "Tadpole-Nettie: Learn about Antidote",
        "Tadpole-Nettie: Cure the Poison",
        "Grove-Harpy: Hear Harpy Song",
        "Grove-Harpy: Find Child",
        "Grove-Harpy: Defeat Harpies",
        "Grove-Harpy: Discover Hideout Password",
        "Grove-Harpy: Tell password to Doni",
        "Grove-Harpy: Meet Mol",
        "Grove-Locket: Recover Locket",
        "Grove-Locket: Return Locket",
        "Grove-Snake: Learn about Arabella",
        "Grove-Snake: Find Arabella",
        "Grove-Snake: Resolve Arabella's Situation",
        "Grove-Snake: Talk to Arabella's Parents",
        "Grove-Kagha: Talk to Zevlor about Kagha",
        "Grove-Kagha: Meet Kagha",
        "Grove-Kagha: Find Note in Grove",
        "Grove-Kagha: Get past Guards",
        "Grove-Kagha: Talk to Rath",
        "Grove-Sazza: Keep Sazza Alive",
        "Grove-Sazza: Free Sazza",
        "Grove-Sazza: Escort Sazza out",
        "Grove-Idol: Get Asked to Steal the Idol",
        "Lae'zel: Find out about Zorru",
        "Lae'zel: Talk to Zorru",
        "Shart: See Wound",
        "Wyll: Recruited",]
    )
    grove.add_locations(grove_locations, BG3Location)

    blighted_village_locations = get_location_names_with_ids([
        "Village-Book: Learn about Lab",
        "Village-Book: Find Lab",
        "Village-Book: Find Tome",
        "Village-Book: Learn about Gem",
        "Village-Book: Find Gem",
        "Village-Book: Unlock Tome",
        "Village-Book: Read Tome",
        "Village-Forge: Find Journal",
        "Village-Forge: Find Plans",
        "Village-Gnome: Find Windmill",
        "Village-Gnome: Talk to Goblins",
        "Village-Gnome: Get Rid of Goblins",
        "Village-Gnome: Stop Windmill",
        "Village-Gnome: Free Gnome",
        "Village-Gnome: Talk to Barcus",
        "Tadpole: Found a Tadpole",
        "Tadpole: Used Illithid Persuasion"]
    )
    blighted_village.add_locations(blighted_village_locations, BG3Location)

    goblin_camp_locations = get_location_names_with_ids(
        ["Gobs: Arrive at Goblin Camp",
        "Gobs: Learn the Priestess' Name",
        "Gobs: Learn the Drow's Name",
        "Gobs: Learn the King's Name",
        "Gobs: Kill Priestess Gut",
        "Gobs: Kill Dror Ragzlin",
        "Gobs: Defeat (Knock Out) Minthara",
        "Gobs: Follow Gut to her Quarters",
        "Gobs-Halsin: Learn Halsin is Missing",
        "Gobs-Halsin: Found Halsin",
        "Gobs-Halsin: Defeated all Goblin Leaders",
        "Gobs-Halsin: Tell Halsin about Victory",
        "Gobs-Halsin: Tell Tieflings about Halsin's Freedom",
        "Gobs-Halsin: Celebrate with Tieflings",
        "Gobs-Halsin: Tieflings left for Baldur's Gate",
        "Gobs-Halsin: Learn Halsin is a Bear",
        "Gobs-Halsin: Get Reward from Rath",
        "Grove-Sazza: Find Sazza at Minthara",
        "Grove-Sazza: Save Sazza Again",
        "Gobs-Volo: Watch Volo get Escorted Away",
        "Gobs-Volo: Find Volo in Cage",
        "Gobs-Volo: Free Volo",
        "Gobs-Volo: Meet Volo in Camp",
        "Gobs-Nightsong: Find Clues to Nightsong",
        "Plot-Art: Hear Minthara talk about Artefact",
        "Plot-Art: Hear Ragzlin talk about Artefact",
        "Tadpole: Told by Guardian to find Tadpoles",
        "Tadpole: Guardian Suggests Consuming Tadpole",
        "Grove-Idol: Steal the Idol",
        "Grove-Idol: Give Idol to Mol",]
    )
    goblin_camp.add_locations(goblin_camp_locations, BG3Location)

    waukeen_locations = get_location_names_with_ids(
        ["Gale: Told about Hunger",
        "Gale: Fed an Item",
        "Waukeen-Zhent: Meet Oskar",
        "Waukeen-Zhent: Agree to Free Oskar",
        "Waukeen-Zhent: Learn Oskar's Price",
        "Waukeen-Zhent: Free Oskar",
        "Waukeen-Fire: Notice Fire",
        "Waukeen-Fire: Enter Inn",
        "Waukeen-Fire: Find Benryn",
        "Waukeen-Fire: Find Florrick",
        "Waukeen-Fire: Rescue Benryn",
        "Waukeen-Fire: Rescue Florrick",
        "Waukeen-Fire: Learn about Duke",
        "Waukeen-Fire: Accept Mission to Rescue Duke",
        "Waukeen-Fire: Learn about Benryn's Wife",
        "Waukeen-Fire: Show Benryn his Wife",
        "Waukeen-Fire: Learn about Dowry",
        "Waukeen-Fire: Recover Dowry",
        "Waukeen-Fire: Return Dowry",
        "Karlach-Tyr: Agree to Help Anders",
        "Karlach-Tyr: Meet Karlach",
        "Karlach-Tyr: Learn Anders Follows Zariel",
        "Karlach-Tyr: Recruit Karlach",
        "Karlach-Tyr: Kill the Paladins",
        "Waukeen-Zhent: Find Caravan",
        "Waukeen-Zhent: Notice Struggle",
        "Waukeen-Zhent: Kill Gnolls",
        "Waukeen-Zhent: Rescue Agents",
        "Waukeen-Zhent: Learn Password",
        "Waukeen-Zhent: Enter Zhentarim Hideout",
        "Waukeen-Zhent: Return Cargo",
        "Karlach-Heart: Recruit Karlach",
        "Karlach-Heart: Learn about Heart Upgrades",
        "Karlach-Heart: Introduce Karlach to Dammon",
        "Karlach-Heart: Find Infernal Metal",
        "Karlach-Heart: Get First Heart Upgrade",
        "Lae'zel: See Dragon Rider",
        "Lae'zel: Deal with Patrol",
        "Lae'zel: Learn Creche Location",
        "Wyll: Resolved Conflict with Karlach",
        "Wyll: Meet Mizora",
        "Wyll: Learn Wyll's Father",
    ])
    waukeen.add_locations(waukeen_locations, BG3Location)

    hag_locations = get_location_names_with_ids([
        "Grove-Kagha: Find Note in Swamp",
        "Grove-Kagha: Confront Kagha",
        "Grove-Kagha: Kill the Shadow Druids",
        "Grove-Kagha: Return to Zevlor",
    ])
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
