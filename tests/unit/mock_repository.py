"""Mock repository for unit testing - provides minimal test data for fast tests."""

from typing import Any

class MockRepository:
    """Test double with minimal, predictable data for unit testing."""

    def __init__(self):
        pass

    def get_pokemon_index(self) -> dict[str, dict[str, Any]]:
        """Returns Pokemon info for test Pokemon."""
        return {
            # Normal Pokemon
            "bulbasaur": {"display_name": "Bulbasaur", "number": 1, "height": 0.7, "weight": 6.9, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png", "description": "A strange seed was planted on its back at birth.", "genus": "Seed Pokémon", "type_display": "grass/poison", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "charmander": {"display_name": "Charmander", "number": 4, "height": 0.6, "weight": 8.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "description": "Obviously prefers hot places.", "genus": "Lizard Pokémon", "type_display": "fire", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "charizard": {"display_name": "Charizard", "number": 6, "height": 1.7, "weight": 90.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png", "description": "Spits fire that is hot enough to melt boulders.", "genus": "Flame Pokémon", "type_display": "fire/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "pikachu": {"display_name": "Pikachu", "number": 25, "height": 0.4, "weight": 6.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png", "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.", "genus": "Mouse Pokémon", "type_display": "electric", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gastly": {"display_name": "Gastly", "number": 92, "height": 1.3, "weight": 0.1, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/92.png", "description": "Almost invisible, this gaseous POKéMON cloaks the target and puts it to sleep without notice.", "genus": "Gas Pokémon", "type_display": "ghost/poison", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "haunter": {"display_name": "Haunter", "number": 93, "height": 1.6, "weight": 0.1, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/93.png", "description": "Because of its ability to slip through block walls, it is said to be from another dimension.", "genus": "Gas Pokémon", "type_display": "ghost/poison", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gengar": {"display_name": "Gengar", "number": 94, "height": 1.5, "weight": 40.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png", "description": "Under a full moon, this POKéMON likes to mimic the shadows of people and laugh at their fright.", "genus": "Shadow Pokémon", "type_display": "ghost/poison", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "vulpix": {"display_name": "Vulpix", "number": 37, "height": 0.6, "weight": 9.9, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/37.png", "description": "At the time of birth, it has just one tail.", "genus": "Fox Pokémon", "type_display": "fire", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "zubat": {"display_name": "Zubat", "number": 41, "height": 0.8, "weight": 7.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/41.png", "description": "Forms colonies in perpetually dark places.", "genus": "Bat Pokémon", "type_display": "poison/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "meowth": {"display_name": "Meowth", "number": 52, "height": 0.4, "weight": 4.2, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/52.png", "description": "Adores circular objects.", "genus": "Scratch Cat Pokémon", "type_display": "normal", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "psyduck": {"display_name": "Psyduck", "number": 54, "height": 0.8, "weight": 19.6, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/54.png", "description": "While lulling its enemies with its vacant look, this wily POKéMON will use psychokinetic powers.", "genus": "Duck Pokémon", "type_display": "water", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "poliwag": {"display_name": "Poliwag", "number": 60, "height": 0.6, "weight": 12.4, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/60.png", "description": "Its newly grown legs prevent it from running.", "genus": "Tadpole Pokémon", "type_display": "water", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "poliwhirl": {"display_name": "Poliwhirl", "number": 61, "height": 1.0, "weight": 20.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/61.png", "description": "Capable of living in or out of water.", "genus": "Tadpole Pokémon", "type_display": "water", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "poliwrath": {"display_name": "Poliwrath", "number": 62, "height": 1.3, "weight": 54.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/62.png", "description": "An adept swimmer at both the front crawl and breast stroke.", "genus": "Tadpole Pokémon", "type_display": "water/fighting", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "ponyta": {"display_name": "Ponyta", "number": 77, "height": 1.0, "weight": 30.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/77.png", "description": "Its hooves are 10 times harder than diamonds.", "genus": "Fire Horse Pokémon", "type_display": "fire", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "exeggcute": {"display_name": "Exeggcute", "number": 102, "height": 0.4, "weight": 2.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/102.png", "description": "Often mistaken for eggs.", "genus": "Egg Pokémon", "type_display": "grass/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "exeggutor": {"display_name": "Exeggutor", "number": 103, "height": 2.0, "weight": 120.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/103.png", "description": "Legend has it that on rare occasions, one of its heads will drop off and continue on as an EXEGGCUTE.", "genus": "Coconut Pokémon", "type_display": "grass/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "mr-mime": {"display_name": "Mr. Mime", "number": 122, "height": 1.3, "weight": 54.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/122.png", "description": "If interrupted while it is miming, it will slap around the offender with its broad hands.", "genus": "Barrier Pokémon", "type_display": "psychic/fairy", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "hoothoot": {"display_name": "Hoothoot", "number": 163, "height": 0.7, "weight": 21.2, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/163.png", "description": "It always stands on one foot.", "genus": "Owl Pokémon", "type_display": "normal/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "noctowl": {"display_name": "Noctowl", "number": 164, "height": 1.6, "weight": 40.8, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/164.png", "description": "Its eyes are specially adapted.", "genus": "Owl Pokémon", "type_display": "normal/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "politoed": {"display_name": "Politoed", "number": 186, "height": 1.1, "weight": 33.9, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/186.png", "description": "The curled hair on POLITOED's head is proof of its status as a king.", "genus": "Frog Pokémon", "type_display": "water", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "ralts": {"display_name": "Ralts", "number": 280, "height": 0.4, "weight": 6.6, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/280.png", "description": "It is highly attuned to the emotions of people and POKéMON.", "genus": "Feeling Pokémon", "type_display": "psychic/fairy", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "kirlia": {"display_name": "Kirlia", "number": 281, "height": 0.8, "weight": 20.2, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/281.png", "description": "It is said that a KIRLIA that is exposed to the positive emotions of its TRAINER grows beautiful.", "genus": "Emotion Pokémon", "type_display": "psychic/fairy", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gardevoir": {"display_name": "Gardevoir", "number": 282, "height": 1.6, "weight": 48.4, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/282.png", "description": "GARDEVOIR has the ability to read the future.", "genus": "Embrace Pokémon", "type_display": "psychic/fairy", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "lunatone": {"display_name": "Lunatone", "number": 337, "height": 1.0, "weight": 168.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/337.png", "description": "It becomes very active on the night of a full moon.", "genus": "Meteorite Pokémon", "type_display": "rock/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "solrock": {"display_name": "Solrock", "number": 338, "height": 1.2, "weight": 154.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/338.png", "description": "Solar energy is the source of this POKéMON's power.", "genus": "Meteorite Pokémon", "type_display": "rock/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "feebas": {"display_name": "Feebas", "number": 349, "height": 0.6, "weight": 7.4, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/349.png", "description": "FEEBAS's fins are ragged and tattered from the start of its life.", "genus": "Fish Pokémon", "type_display": "water", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "drifloon": {"display_name": "Drifloon", "number": 425, "height": 0.4, "weight": 1.2, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/425.png", "description": "A Pokémon formed by the spirits of people and Pokémon.", "genus": "Balloon Pokémon", "type_display": "ghost/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "bronzor": {"display_name": "Bronzor", "number": 436, "height": 0.5, "weight": 60.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/436.png", "description": "Implements shaped like ancient POKéMON have been discovered.", "genus": "Bronze Pokémon", "type_display": "steel/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "bronzong": {"display_name": "Bronzong", "number": 437, "height": 1.3, "weight": 187.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/437.png", "description": "One caused a news sensation when it was dug up at a construction site after a 2,000-year sleep.", "genus": "Bronze Bell Pokémon", "type_display": "steel/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "mime-jr": {"display_name": "Mime Jr.", "number": 439, "height": 0.6, "weight": 13.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/439.png", "description": "It habitually mimics foes.", "genus": "Mime Pokémon", "type_display": "psychic/fairy", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "spiritomb": {"display_name": "Spiritomb", "number": 442, "height": 1.0, "weight": 108.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/442.png", "description": "A Pokémon that was formed by 108 spirits.", "genus": "Forbidden Pokémon", "type_display": "ghost/dark", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gallade": {"display_name": "Gallade", "number": 475, "height": 1.6, "weight": 52.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/475.png", "description": "A master of courtesy and swordsmanship.", "genus": "Blade Pokémon", "type_display": "psychic/fighting", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "munna": {"display_name": "Munna", "number": 517, "height": 0.6, "weight": 23.3, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/517.png", "description": "Munna always float in the air.", "genus": "Dream Eater Pokémon", "type_display": "psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "musharna": {"display_name": "Musharna", "number": 518, "height": 1.1, "weight": 60.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/518.png", "description": "The mist emanating from their foreheads is packed with the dreams of people and Pokémon.", "genus": "Drowsing Pokémon", "type_display": "psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "pidove": {"display_name": "Pidove", "number": 519, "height": 0.3, "weight": 2.1, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/519.png", "description": "These Pokémon live in cities.", "genus": "Tiny Pigeon Pokémon", "type_display": "normal/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "sigilyph": {"display_name": "Sigilyph", "number": 561, "height": 1.4, "weight": 14.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/561.png", "description": "The guardians of an ancient city, they use their psychic power to attack enemies that invade their territory.", "genus": "Avianoid Pokémon", "type_display": "psychic/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gothita": {"display_name": "Gothita", "number": 574, "height": 0.4, "weight": 5.8, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/574.png", "description": "Their ribbons change shape depending on their feelings.", "genus": "Fixation Pokémon", "type_display": "psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gothorita": {"display_name": "Gothorita", "number": 575, "height": 0.7, "weight": 18.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/575.png", "description": "Starlight is the source of their power.", "genus": "Manipulate Pokémon", "type_display": "psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gothitelle": {"display_name": "Gothitelle", "number": 576, "height": 1.5, "weight": 44.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/576.png", "description": "Starry skies thousands of light-years away are visible in the space distorted by their intense psychic power.", "genus": "Astral Body Pokémon", "type_display": "psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "inkay": {"display_name": "Inkay", "number": 686, "height": 0.4, "weight": 3.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/686.png", "description": "Opponents who stare at the flashing of the light-emitting spots on its body become dazed and lose their will to fight.", "genus": "Revolving Pokémon", "type_display": "dark/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "malamar": {"display_name": "Malamar", "number": 687, "height": 1.5, "weight": 47.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/687.png", "description": "It lures its prey close with hypnotic motions, then wraps its tentacles around it before finishing it off with digestive fluids.", "genus": "Overturning Pokémon", "type_display": "dark/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "sandygast": {"display_name": "Sandygast", "number": 769, "height": 0.5, "weight": 70.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/769.png", "description": "Born from a sand mound playfully built by a child, this Pokémon embodies the grudges of the departed.", "genus": "Sand Heap Pokémon", "type_display": "ghost/ground", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "palossand": {"display_name": "Palossand", "number": 770, "height": 1.3, "weight": 250.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/770.png", "description": "Possessed people controlled by this Pokémon transformed its sand mound into a castle.", "genus": "Sand Castle Pokémon", "type_display": "ghost/ground", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},

            # Psychic type Pokemon for "psychic" move tests
            "alakazam": {"display_name": "Alakazam", "number": 65, "height": 1.5, "weight": 48.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/65.png", "description": "Its brain can outperform a supercomputer.", "genus": "Psi Pokémon", "type_display": "psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},

            # Legendary Pokemon
            "mewtwo": {"display_name": "Mewtwo", "number": 150, "height": 2.0, "weight": 122.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png", "description": "It was created by a scientist after years of horrific gene splicing and DNA engineering experiments.", "genus": "Genetic Pokémon", "type_display": "psychic", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "latias": {"display_name": "Latias", "number": 380, "height": 1.4, "weight": 40.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/380.png", "description": "They make a small herd of only several members.", "genus": "Eon Pokémon", "type_display": "dragon/psychic", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "latios": {"display_name": "Latios", "number": 381, "height": 2.0, "weight": 60.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/381.png", "description": "Even in hiding, it can detect the locations of others and sense their emotions.", "genus": "Eon Pokémon", "type_display": "dragon/psychic", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "cresselia": {"display_name": "Cresselia", "number": 488, "height": 1.5, "weight": 85.6, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/488.png", "description": "Shining particles are released from its wings like a veil.", "genus": "Lunar Pokémon", "type_display": "psychic", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},

            # Mythical Pokemon
            "celebi": {"display_name": "Celebi", "number": 251, "height": 0.6, "weight": 5.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/251.png", "description": "This POKéMON wanders across time.", "genus": "Time Travel Pokémon", "type_display": "psychic/grass", "is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "jirachi": {"display_name": "Jirachi", "number": 385, "height": 0.3, "weight": 1.1, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/385.png", "description": "A legend states that JIRACHI will make true any wish that is written on notes attached to its head when it awakens.", "genus": "Wish Pokémon", "type_display": "steel/psychic", "is_legendary": False, "is_mythical": True, "is_ultra_beast": False},

            # Ultra Beasts
            "nihilego": {"display_name": "Nihilego", "number": 793, "height": 1.2, "weight": 55.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/793.png", "description": "One of the Ultra Beasts.", "genus": "Parasite Pokémon", "type_display": "rock/poison", "is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "blacephalon": {"display_name": "Blacephalon", "number": 806, "height": 1.8, "weight": 13.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/806.png", "description": "A UB that appeared from an Ultra Wormhole.", "genus": "Fireworks Pokémon", "type_display": "fire/ghost", "is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "kartana": {"display_name": "Kartana", "number": 798, "height": 0.3, "weight": 0.1, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/798.png", "description": "This Ultra Beast came from the Ultra Wormhole.", "genus": "Drawn Sword Pokémon", "type_display": "grass/steel", "is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "pheromosa": {"display_name": "Pheromosa", "number": 795, "height": 1.8, "weight": 25.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/795.png", "description": "A life-form that lives in another world.", "genus": "Lissome Pokémon", "type_display": "bug/fighting", "is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "celesteela": {"display_name": "Celesteela", "number": 797, "height": 9.2, "weight": 999.9, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/797.png", "description": "One of the dangerous UBs.", "genus": "Launch Pokémon", "type_display": "steel/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": True},

            # Pokemon from type_index
            "arcanine": {"display_name": "Arcanine", "number": 59, "height": 1.9, "weight": 155.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/59.png", "description": "A POKéMON that has been admired since the past for its beauty.", "genus": "Legendary Pokémon", "type_display": "fire", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "moltres": {"display_name": "Moltres", "number": 146, "height": 2.0, "weight": 60.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/146.png", "description": "Known as the legendary bird of fire.", "genus": "Flame Pokémon", "type_display": "fire/flying", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "entei": {"display_name": "Entei", "number": 244, "height": 2.1, "weight": 198.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/244.png", "description": "Volcanoes erupt when it barks.", "genus": "Volcano Pokémon", "type_display": "fire", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "ho-oh": {"display_name": "Ho-Oh", "number": 250, "height": 3.8, "weight": 199.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/250.png", "description": "Legends claim this POKéMON flies the world's skies continuously on its magnificent seven-colored wings.", "genus": "Rainbow Pokémon", "type_display": "fire/flying", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "victini": {"display_name": "Victini", "number": 494, "height": 0.4, "weight": 4.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/494.png", "description": "This Pokémon brings victory.", "genus": "Victory Pokémon", "type_display": "psychic/fire", "is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "volcanion": {"display_name": "Volcanion", "number": 721, "height": 1.7, "weight": 195.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/721.png", "description": "It lets out billows of steam and disappears into the dense fog.", "genus": "Steam Pokémon", "type_display": "fire/water", "is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "fletchinder": {"display_name": "Fletchinder", "number": 662, "height": 0.7, "weight": 16.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/662.png", "description": "From its beak, it fires embers at its prey.", "genus": "Ember Pokémon", "type_display": "fire/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "talonflame": {"display_name": "Talonflame", "number": 663, "height": 1.2, "weight": 24.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/663.png", "description": "In the fever of an exciting battle, it showers embers from the gaps between its feathers and takes to the air.", "genus": "Scorching Pokémon", "type_display": "fire/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "typhlosion": {"display_name": "Typhlosion", "number": 157, "height": 1.7, "weight": 79.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/157.png", "description": "If its rage peaks, it becomes so hot that anything that touches it will instantly go up in flames.", "genus": "Volcano Pokémon", "type_display": "fire", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "blastoise": {"display_name": "Blastoise", "number": 9, "height": 1.6, "weight": 85.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png", "description": "A brutal POKéMON with pressurized water jets on its shell.", "genus": "Shellfish Pokémon", "type_display": "water", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gyarados": {"display_name": "Gyarados", "number": 130, "height": 6.5, "weight": 235.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/130.png", "description": "Rarely seen in the wild. Huge and vicious, it is capable of destroying entire cities in a rage.", "genus": "Atrocious Pokémon", "type_display": "water/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "slaking": {"display_name": "Slaking", "number": 289, "height": 2.0, "weight": 130.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/289.png", "description": "Wherever SLAKING live, rings of over a yard in diameter appear in grassy fields.", "genus": "Lazy Pokémon", "type_display": "normal", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "snorlax": {"display_name": "Snorlax", "number": 143, "height": 2.1, "weight": 460.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png", "description": "Very lazy. Just eats and sleeps.", "genus": "Sleeping Pokémon", "type_display": "normal", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "glaceon": {"display_name": "Glaceon", "number": 471, "height": 0.8, "weight": 25.9, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/471.png", "description": "As a protective technique, it can completely freeze its fur to make its hairs stand like needles.", "genus": "Fresh Snow Pokémon", "type_display": "ice", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "avalugg": {"display_name": "Avalugg", "number": 713, "height": 2.0, "weight": 505.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/713.png", "description": "The way several Bergmite huddle on its back makes it look like an aircraft carrier made of ice.", "genus": "Iceberg Pokémon", "type_display": "ice", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "steelix": {"display_name": "Steelix", "number": 208, "height": 9.2, "weight": 400.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/208.png", "description": "Its body has been compressed deep under the ground.", "genus": "Iron Snake Pokémon", "type_display": "steel/ground", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "metagross": {"display_name": "Metagross", "number": 376, "height": 1.6, "weight": 550.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/376.png", "description": "METAGROSS has four brains in total.", "genus": "Iron Leg Pokémon", "type_display": "steel/psychic", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "registeel": {"display_name": "Registeel", "number": 379, "height": 1.9, "weight": 205.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/379.png", "description": "REGISTEEL has a body that is harder than any kind of metal.", "genus": "Iron Pokémon", "type_display": "steel", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "magearna": {"display_name": "Magearna", "number": 801, "height": 1.0, "weight": 80.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/801.png", "description": "This artificial Pokémon, constructed more than 500 years ago, can understand human speech but cannot itself speak.", "genus": "Artificial Pokémon", "type_display": "steel/fairy", "is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "pidgeot": {"display_name": "Pidgeot", "number": 18, "height": 1.5, "weight": 39.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/18.png", "description": "When hunting, it skims the surface of water at high speed to pick off unwary prey such as MAGIKARP.", "genus": "Bird Pokémon", "type_display": "normal/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},

            # Pokemon from stat_index
            "garchomp": {"display_name": "Garchomp", "number": 445, "height": 1.9, "weight": 95.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/445.png", "description": "When it folds up its body and extends its wings, it looks like a jet plane.", "genus": "Mach Pokémon", "type_display": "dragon/ground", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "salamence": {"display_name": "Salamence", "number": 373, "height": 1.5, "weight": 102.6, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/373.png", "description": "As a result of its long-held dream of flying, its cellular structure changed, and wings grew out.", "genus": "Dragon Pokémon", "type_display": "dragon/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "blaziken": {"display_name": "Blaziken", "number": 257, "height": 1.9, "weight": 52.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/257.png", "description": "In battle, BLAZIKEN blows out intense flames from its wrists and attacks foes courageously.", "genus": "Blaze Pokémon", "type_display": "fire/fighting", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "regigigas": {"display_name": "Regigigas", "number": 486, "height": 3.7, "weight": 420.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/486.png", "description": "There is an enduring legend that states this Pokémon towed continents with ropes.", "genus": "Colossal Pokémon", "type_display": "normal", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "groudon": {"display_name": "Groudon", "number": 383, "height": 3.5, "weight": 950.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/383.png", "description": "GROUDON has long been described in mythology as the POKéMON that raised lands and expanded continents.", "genus": "Continent Pokémon", "type_display": "ground", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "rayquaza": {"display_name": "Rayquaza", "number": 384, "height": 7.0, "weight": 206.5, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/384.png", "description": "RAYQUAZA lived for hundreds of millions of years in the earth's ozone layer.", "genus": "Sky High Pokémon", "type_display": "dragon/flying", "is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "aggron": {"display_name": "Aggron", "number": 306, "height": 2.1, "weight": 360.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/306.png", "description": "AGGRON claims an entire mountain as its own territory.", "genus": "Iron Armor Pokémon", "type_display": "steel/rock", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "rhyperior": {"display_name": "Rhyperior", "number": 464, "height": 2.4, "weight": 282.8, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/464.png", "description": "It puts rocks in holes in its palms and uses its muscles to shoot them.", "genus": "Drill Pokémon", "type_display": "ground/rock", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "dragonite": {"display_name": "Dragonite", "number": 149, "height": 2.2, "weight": 210.0, "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/149.png", "description": "An extremely rarely seen marine POKéMON.", "genus": "Dragon Pokémon", "type_display": "dragon/flying", "is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
        }

    def get_type_index(self) -> dict[str, frozenset[str]]:
        """Returns minimal type index for testing."""
        return {
            "fire": frozenset({
                "charizard", "arcanine", "moltres", "entei", "ho-oh",
                "victini", "volcanion", "fletchinder", "talonflame", "typhlosion"
            }),
            "flying": frozenset({
                "charizard", "moltres", "ho-oh", "fletchinder",
                "talonflame", "celesteela"
            }),
            "ghost": frozenset({
                'phantump', 'golurk', 'shuppet', 'sandygast',
                'trevenant', 'golett', 'froslass', 'honedge', 'haunter', 'misdreavus',
                'cofagrigus', 'dhelmise', 'gastly', 'sableye', 'mismagius', 'litwick',
                'chandelure', 'shedinja', 'lampent', 'palossand', 'banette',
                'doublade', 'yamask', 'rotom', 'spiritomb', 'decidueye', 'gengar',
                'duskull', 'drifblim', 'dusclops', 'drifloon', 'dusknoir',
                'jellicent'
            }),
            "steel": frozenset({
                "steelix", "metagross", "kartana", "celesteela",
                "registeel", "magearna"
            }),
            "water": frozenset({
                "blastoise", "gyarados"
            }),
            "normal": frozenset({
                "slaking", "snorlax"
            }),
            "ice": frozenset({
                "glaceon", "avalugg"
            }),
            "psychic": frozenset({
                "mewtwo", "latias", "celebi", "alakazam"
            }),
        }

    def get_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Returns minimal move index for testing."""
        return {
            "hypnosis": {
                'vulpix': {'egg': True}, 'zubat': {'egg': True},
                'meowth': {'egg': True}, 'psyduck': {'egg': True},
                'poliwag': {'level-up': 1}, 'poliwhirl': {'level-up': 1},
                'poliwrath': {'level-up': 1}, 'ponyta': {'egg': True},
                'gastly': {'level-up': 4}, 'haunter': {'level-up': 1},
                'gengar': {'level-up': 1}, 'exeggcute': {'level-up': 1},
                'exeggutor': {'level-up': 1}, 'mr-mime': {'egg': True},
                'hoothoot': {'level-up': 36}, 'noctowl': {'level-up': 48},
                'politoed': {'level-up': 1}, 'ralts': {'level-up': 9},
                'kirlia': {'level-up': 9}, 'gardevoir': {'level-up': 9},
                'lunatone': {'level-up': 5}, 'solrock': {'level-up': 5},
                'feebas': {'egg': True}, 'drifloon': {'egg': True},
                'bronzor': {'level-up': 20}, 'bronzong': {'level-up': 20},
                'mime-jr': {'egg': True}, 'spiritomb': {'level-up': 55},
                'gallade': {'level-up': 1}, 'munna': {'level-up': 4},
                'musharna': {'level-up': 1}, 'pidove': {'egg': True},
                'sigilyph': {'level-up': 10}, 'gothita': {'level-up': 24},
                'gothorita': {'level-up': 24}, 'gothitelle': {'level-up': 24},
                'inkay': {'level-up': 3}, 'malamar': {'level-up': 1},
                'sandygast': {'level-up': 30}, 'palossand': {'level-up': 30}
            },
            "psychic": {
                "alakazam": {'machine': True},
                "latias": {'machine': True},
                "latios": {'machine': True},
                "cresselia": {'machine': True},
                "celebi": {'machine': True},
                "jirachi": {'machine': True},
                "nihilego": {'machine': True},
                "blacephalon": {'machine': True},
            }
        }

    def get_stat_index(self) -> dict[str, dict[str, int]]:
        """Returns base stats for test Pokemon."""
        return {
            "garchomp": {"hp": 108, "attack": 130, "defense": 95, "special_attack": 80, "special_defense": 85, "speed": 102},
            "salamence": {"hp": 95, "attack": 135, "defense": 80, "special_attack": 110, "special_defense": 80, "speed": 100},
            "slaking": {"hp": 150, "attack": 160, "defense": 100, "special_attack": 95, "special_defense": 65, "speed": 100},
            "blaziken": {"hp": 80, "attack": 120, "defense": 70, "special_attack": 110, "special_defense": 70, "speed": 80},
            "regigigas": {"hp": 110, "attack": 160, "defense": 110, "special_attack": 80, "special_defense": 110, "speed": 100},
            "groudon": {"hp": 100, "attack": 150, "defense": 140, "special_attack": 100, "special_defense": 90, "speed": 90},
            "rayquaza": {"hp": 105, "attack": 150, "defense": 90, "special_attack": 150, "special_defense": 90, "speed": 95},
            "kartana": {"hp": 59, "attack": 181, "defense": 131, "special_attack": 59, "special_defense": 31, "speed": 109},
            "pheromosa": {"hp": 71, "attack": 137, "defense": 37, "special_attack": 137, "special_defense": 37, "speed": 151},
            "aggron": {"hp": 70, "attack": 110, "defense": 180, "special_attack": 60, "special_defense": 60, "speed": 50},
            "rhyperior": {"hp": 115, "attack": 140, "defense": 130, "special_attack": 55, "special_defense": 55, "speed": 40},
            # Add one more Pokemon to get 5+ results for test
            "dragonite": {"hp": 91, "attack": 134, "defense": 95, "special_attack": 100, "special_defense": 100, "speed": 80},
        }

    def get_stat_spread_index(self) -> dict[str, Any]:
        """Returns stat spread quintiles for testing."""
        return {
            "STAT_MEDIANS": {
                "hp": 65,
                "attack": 75,
                "defense": 70,
                "special_attack": 72,
                "special_defense": 70,
                "speed": 65
            },
            "QUINTILES": {
                "D": {"hp": 50, "attack": 55, "defense": 50, "special_attack": 50, "special_defense": 50, "speed": 45},
                "C": {"hp": 65, "attack": 75, "defense": 70, "special_attack": 72, "special_defense": 70, "speed": 65},
                "B": {"hp": 80, "attack": 95, "defense": 85, "special_attack": 90, "special_defense": 85, "speed": 85},
                "A": {"hp": 95, "attack": 110, "defense": 100, "special_attack": 105, "special_defense": 100, "speed": 100},
                "S": {"hp": 255, "attack": 255, "defense": 255, "special_attack": 255, "special_defense": 255, "speed": 255}
            }
        }

    def get_type_matchup_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """Returns type effectiveness matchups for testing - complete type chart."""
        return {
            "normal": {"double_damage_from": frozenset({"fighting"}), "half_damage_from": frozenset(), "no_damage_from": frozenset({"ghost"})},
            "fire": {"double_damage_from": frozenset({"water", "ground", "rock"}), "half_damage_from": frozenset({"fire", "grass", "ice", "bug", "steel", "fairy"}), "no_damage_from": frozenset()},
            "water": {"double_damage_from": frozenset({"electric", "grass"}), "half_damage_from": frozenset({"fire", "water", "ice", "steel"}), "no_damage_from": frozenset()},
            "electric": {"double_damage_from": frozenset({"ground"}), "half_damage_from": frozenset({"electric", "flying", "steel"}), "no_damage_from": frozenset()},
            "grass": {"double_damage_from": frozenset({"fire", "ice", "poison", "flying", "bug"}), "half_damage_from": frozenset({"water", "electric", "grass", "ground"}), "no_damage_from": frozenset()},
            "ice": {"double_damage_from": frozenset({"fire", "fighting", "rock", "steel"}), "half_damage_from": frozenset({"ice"}), "no_damage_from": frozenset()},
            "fighting": {"double_damage_from": frozenset({"flying", "psychic", "fairy"}), "half_damage_from": frozenset({"bug", "rock", "dark"}), "no_damage_from": frozenset()},
            "poison": {"double_damage_from": frozenset({"ground", "psychic"}), "half_damage_from": frozenset({"grass", "fighting", "poison", "bug", "fairy"}), "no_damage_from": frozenset()},
            "ground": {"double_damage_from": frozenset({"water", "grass", "ice"}), "half_damage_from": frozenset({"poison", "rock"}), "no_damage_from": frozenset({"electric"})},
            "flying": {"double_damage_from": frozenset({"electric", "ice", "rock"}), "half_damage_from": frozenset({"grass", "fighting", "bug"}), "no_damage_from": frozenset({"ground"})},
            "psychic": {"double_damage_from": frozenset({"bug", "ghost", "dark"}), "half_damage_from": frozenset({"fighting", "psychic"}), "no_damage_from": frozenset()},
            "bug": {"double_damage_from": frozenset({"fire", "flying", "rock"}), "half_damage_from": frozenset({"grass", "fighting", "ground"}), "no_damage_from": frozenset()},
            "rock": {"double_damage_from": frozenset({"water", "grass", "fighting", "ground", "steel"}), "half_damage_from": frozenset({"normal", "fire", "poison", "flying"}), "no_damage_from": frozenset()},
            "ghost": {"double_damage_from": frozenset({"ghost", "dark"}), "half_damage_from": frozenset({"bug", "poison"}), "no_damage_from": frozenset({"fighting", "normal"})},
            "dragon": {"double_damage_from": frozenset({"ice", "dragon", "fairy"}), "half_damage_from": frozenset({"fire", "water", "electric", "grass"}), "no_damage_from": frozenset()},
            "dark": {"double_damage_from": frozenset({"fighting", "bug", "fairy"}), "half_damage_from": frozenset({"ghost", "dark"}), "no_damage_from": frozenset({"psychic"})},
            "steel": {"double_damage_from": frozenset({"fire", "fighting", "ground"}), "half_damage_from": frozenset({"normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"}), "no_damage_from": frozenset({"poison"})},
            "fairy": {"double_damage_from": frozenset({"poison", "steel"}), "half_damage_from": frozenset({"fighting", "bug", "dark"}), "no_damage_from": frozenset({"dragon"})},
        }
