"""Option Library for AI Kids Studio Pro.

This module provides professional-grade option libraries for all variable types.
Separated from registry logic for clean separation of concerns and scalability.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Option:
    """A single selectable option with metadata."""
    value: str
    label: str
    description: str = ""
    icon: str = ""
    group: str = ""
    sort_order: int = 0
    searchable: bool = True


@dataclass(frozen=True)
class OptionGroup:
    """A group of related options."""
    name: str
    label: str
    description: str = ""
    icon: str = ""
    options: List[Option] = field(default_factory=list)
    sort_order: int = 0


class OptionLibrary:
    """Centralized library of all professional option datasets.
    
    This class provides curated, professional-grade option lists for all
    variable types used across AI Kids Studio Pro modules.
    """
    
    # ============================================================
    # LANGUAGES (20+)
    # ============================================================
    LANGUAGES = OptionGroup(
        name="languages",
        label="Languages",
        description="World languages for content generation",
        icon="🌍",
        sort_order=1,
        options=[
            Option("english", "English", "English (US/UK)", "🇺🇸", sort_order=1),
            Option("spanish", "Spanish", "Español", "🇪🇸", sort_order=2),
            Option("french", "French", "Français", "🇫🇷", sort_order=3),
            Option("german", "German", "Deutsch", "🇩🇪", sort_order=4),
            Option("chinese", "Chinese (Mandarin)", "中文", "🇨🇳", sort_order=5),
            Option("japanese", "Japanese", "日本語", "🇯🇵", sort_order=6),
            Option("korean", "Korean", "한국어", "🇰🇷", sort_order=7),
            Option("arabic", "Arabic", "العربية", "🇸🇦", sort_order=8),
            Option("hindi", "Hindi", "हिन्दी", "🇮🇳", sort_order=9),
            Option("portuguese", "Portuguese", "Português", "🇧🇷", sort_order=10),
            Option("russian", "Russian", "Русский", "🇷🇺", sort_order=11),
            Option("italian", "Italian", "Italiano", "🇮🇹", sort_order=12),
            Option("turkish", "Turkish", "Türkçe", "🇹🇷", sort_order=13),
            Option("dutch", "Dutch", "Nederlands", "🇳🇱", sort_order=14),
            Option("polish", "Polish", "Polski", "🇵🇱", sort_order=15),
            Option("swedish", "Swedish", "Svenska", "🇸🇪", sort_order=16),
            Option("norwegian", "Norwegian", "Norsk", "🇳🇴", sort_order=17),
            Option("danish", "Danish", "Dansk", "🇩🇰", sort_order=18),
            Option("finnish", "Finnish", "Suomi", "🇫🇮", sort_order=19),
            Option("hebrew", "Hebrew", "עברית", "🇮🇱", sort_order=20),
            Option("thai", "Thai", "ไทย", "🇹🇭", sort_order=21),
            Option("vietnamese", "Vietnamese", "Tiếng Việt", "🇻🇳", sort_order=22),
            Option("indonesian", "Indonesian", "Bahasa Indonesia", "🇮🇩", sort_order=23),
            Option("urdu", "Urdu", "اردو", "🇵🇰", sort_order=24),
        ]
    )
    
    # ============================================================
    # VOICES (20+)
    # ============================================================
    VOICES = OptionGroup(
        name="voices",
        label="Voice Presets",
        description="Professional voice presets for TTS generation",
        icon="🎙️",
        sort_order=2,
        options=[
            Option("female_adult", "Female Adult", "Warm, clear adult female voice", "👩", sort_order=1),
            Option("male_adult", "Male Adult", "Deep, confident adult male voice", "👨", sort_order=2),
            Option("female_child", "Female Child", "Cheerful young girl voice", "👧", sort_order=3),
            Option("male_child", "Male Child", "Energetic young boy voice", "👦", sort_order=4),
            Option("female_teen", "Female Teen", "Relatable teenage girl voice", "👩‍🦰", sort_order=5),
            Option("male_teen", "Male Teen", "Cool teenage boy voice", "👨‍🦰", sort_order=6),
            Option("female_senior", "Female Senior", "Wise, gentle grandmother voice", "👵", sort_order=7),
            Option("male_senior", "Male Senior", "Warm, storytelling grandfather voice", "👴", sort_order=8),
            Option("narrator_pro", "Professional Narrator", "Broadcast-quality narrator", "🎙️", sort_order=9),
            Option("storyteller", "Storyteller", "Expressive, dramatic storyteller", "📖", sort_order=10),
            Option("teacher_female", "Female Teacher", "Clear, encouraging teacher voice", "👩‍🏫", sort_order=11),
            Option("teacher_male", "Male Teacher", "Authoritative yet friendly teacher", "👨‍🏫", sort_order=12),
            Option("cartoon_character", "Cartoon Character", "Animated, exaggerated character voice", "🎭", sort_order=13),
            Option("robot", "Robot/AI", "Futuristic synthetic voice", "🤖", sort_order=14),
            Option("monster_friendly", "Friendly Monster", "Playful monster voice for kids", "👾", sort_order=15),
            Option("fairy", "Fairy/Magical", "Ethereal, magical creature voice", "🧚", sort_order=16),
            Option("pirate", "Pirate", "Arrr! Swashbuckling pirate voice", "🏴‍☠️", sort_order=17),
            Option("superhero", "Superhero", "Bold, heroic announcer voice", "🦸", sort_order=18),
            Option("whisper", "Whisper", "Intimate, close-mic whisper", "🤫", sort_order=19),
            Option("announcer", "Announcer", "Big event announcer voice", "📢", sort_order=20),
            Option("meditation", "Meditation Guide", "Calm, soothing meditation voice", "🧘", sort_order=21),
            Option("news_anchor", "News Anchor", "Professional broadcast journalist", "📺", sort_order=22),
        ]
    )
    
    # ============================================================
    # ACCENTS (15+)
    # ============================================================
    ACCENTS = OptionGroup(
        name="accents",
        label="Accents",
        description="Regional accents for voice generation",
        icon="🗣️",
        sort_order=3,
        options=[
            Option("american", "American (General)", "Standard US accent", "🇺🇸", sort_order=1),
            Option("british", "British (RP)", "Received Pronunciation UK", "🇬🇧", sort_order=2),
            Option("australian", "Australian", "General Australian accent", "🇦🇺", sort_order=3),
            Option("canadian", "Canadian", "Standard Canadian accent", "🇨🇦", sort_order=4),
            Option("indian", "Indian English", "Indian English accent", "🇮🇳", sort_order=5),
            Option("irish", "Irish", "Irish accent", "🇮🇪", sort_order=6),
            Option("scottish", "Scottish", "Scottish accent", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", sort_order=7),
            Option("south_african", "South African", "South African English", "🇿🇦", sort_order=8),
            Option("new_zealand", "New Zealand", "Kiwi accent", "🇳🇿", sort_order=9),
            Option("southern_us", "Southern US", "Southern American drawl", "🤠", sort_order=10),
            Option("new_york", "New York", "Classic NYC accent", "🗽", sort_order=11),
            Option("british_cockney", "Cockney", "London working-class accent", "🇬🇧", sort_order=12),
            Option("caribbean", "Caribbean", "Caribbean English accent", "🏝️", sort_order=13),
            Option("nigerian", "Nigerian", "Nigerian English accent", "🇳🇬", sort_order=14),
            Option("singaporean", "Singaporean", "Singlish accent", "🇸🇬", sort_order=15),
        ]
    )
    
    # ============================================================
    # ANIMALS (30+)
    # ============================================================
    ANIMALS = OptionGroup(
        name="animals",
        label="Animals",
        description="Animals for educational content",
        icon="🦁",
        sort_order=4,
        options=[
            Option("lion", "Lion", "King of the jungle", "🦁", sort_order=1),
            Option("elephant", "Elephant", "Gentle giant with trunk", "🐘", sort_order=2),
            Option("giraffe", "Giraffe", "Tallest animal with long neck", "🦒", sort_order=3),
            Option("zebra", "Zebra", "Striped African equid", "🦓", sort_order=4),
            Option("monkey", "Monkey", "Playful primate", "🐒", sort_order=5),
            Option("tiger", "Tiger", "Striped big cat", "🐅", sort_order=6),
            Option("bear", "Bear", "Large furry mammal", "🐻", sort_order=7),
            Option("panda", "Panda", "Black and white bamboo eater", "🐼", sort_order=8),
            Option("koala", "Koala", "Australian eucalyptus eater", "🐨", sort_order=9),
            Option("kangaroo", "Kangaroo", "Australian hopping marsupial", "🦘", sort_order=10),
            Option("fox", "Fox", "Clever red-furred canine", "🦊", sort_order=11),
            Option("wolf", "Wolf", "Pack-hunting canine", "🐺", sort_order=12),
            Option("deer", "Deer", "Graceful antlered herbivore", "🦌", sort_order=13),
            Option("rabbit", "Rabbit", "Hopping long-eared mammal", "🐰", sort_order=14),
            Option("squirrel", "Squirrel", "Bushy-tailed nut gatherer", "🐿️", sort_order=15),
            Option("hedgehog", "Hedgehog", "Spiny insectivore", "🦔", sort_order=16),
            Option("raccoon", "Raccoon", "Masked bandit of the forest", "🦝", sort_order=17),
            Option("otter", "Otter", "Playful aquatic mammal", "🦦", sort_order=18),
            Option("beaver", "Beaver", "Dam-building rodent", "🦫", sort_order=19),
            Option("moose", "Moose", "Large antlered deer", "🫎", sort_order=20),
            Option("horse", "Horse", "Majestic domesticated equine", "🐴", sort_order=21),
            Option("cow", "Cow", "Gentle dairy farm animal", "🐄", sort_order=22),
            Option("pig", "Pig", "Intelligent pink farm animal", "🐷", sort_order=23),
            Option("sheep", "Sheep", "Woolly flock animal", "🐑", sort_order=24),
            Option("goat", "Goat", "Curious climbing herbivore", "🐐", sort_order=25),
            Option("chicken", "Chicken", "Feathered farm bird", "🐔", sort_order=26),
            Option("duck", "Duck", "Quacking waterfowl", "🦆", sort_order=27),
            Option("frog", "Frog", "Jumping amphibian", "🐸", sort_order=28),
            Option("turtle", "Turtle", "Slow-moving shelled reptile", "🐢", sort_order=29),
            Option("snake", "Snake", "Slithering reptile", "🐍", sort_order=30),
            Option("crocodile", "Crocodile", "Ancient armored predator", "🐊", sort_order=31),
            Option("hippo", "Hippo", "Massive river mammal", "🦛", sort_order=32),
            Option("rhino", "Rhino", "Horned heavyweight", "🦏", sort_order=33),
        ]
    )
    
    # ============================================================
    # BIRDS (25+)
    # ============================================================
    BIRDS = OptionGroup(
        name="birds",
        label="Birds",
        description="Birds for educational content",
        icon="🐦",
        sort_order=5,
        options=[
            Option("eagle", "Eagle", "Majestic bird of prey", "🦅", sort_order=1),
            Option("owl", "Owl", "Wise nocturnal hunter", "🦉", sort_order=2),
            Option("parrot", "Parrot", "Colorful talking bird", "🦜", sort_order=3),
            Option("penguin", "Penguin", "Tuxedoed Antarctic bird", "🐧", sort_order=4),
            Option("flamingo", "Flamingo", "Pink long-legged wader", "🦩", sort_order=5),
            Option("peacock", "Peacock", "Iridescent feathered beauty", "🦚", sort_order=6),
            Option("swan", "Swan", "Graceful white waterbird", "🦢", sort_order=7),
            Option("hummingbird", "Hummingbird", "Tiny hovering nectar feeder", "🐦", sort_order=8),
            Option("woodpecker", "Woodpecker", "Tree-tapping drummer", "🐦", sort_order=9),
            Option("robin", "Robin", "Red-breasted songbird", "🐦", sort_order=10),
            Option("blue_jay", "Blue Jay", "Bold blue corvid", "🐦", sort_order=11),
            Option("cardinal", "Cardinal", "Bright red songbird", "🐦", sort_order=12),
            Option("sparrow", "Sparrow", "Common small brown bird", "🐦", sort_order=13),
            Option("crow", "Crow", "Intelligent black corvid", "🐦", sort_order=14),
            Option("raven", "Raven", "Large mysterious corvid", "🐦", sort_order=15),
            Option("hawk", "Hawk", "Sharp-eyed raptor", "🦅", sort_order=16),
            Option("falcon", "Falcon", "Fastest diving bird", "🦅", sort_order=17),
            Option("vulture", "Vulture", "Scavenging soarer", "🦅", sort_order=18),
            Option("ostrich", "Ostrich", "Largest flightless bird", "🦤", sort_order=19),
            Option("emu", "Emu", "Australian flightless bird", "🦤", sort_order=20),
            Option("pelican", "Pelican", "Throat-pouched fisher", "🐦", sort_order=21),
            Option("seagull", "Seagull", "Coastal scavenger", "🐦", sort_order=22),
            Option("pigeon", "Pigeon", "City-dwelling dove", "🕊️", sort_order=23),
            Option("dove", "Dove", "Symbol of peace", "🕊️", sort_order=24),
            Option("swallow", "Swallow", "Aerial insect catcher", "🐦", sort_order=25),
            Option("kingfisher", "Kingfisher", "Colorful fish hunter", "🐦", sort_order=26),
            Option("toucan", "Toucan", "Large-billed tropical bird", "🐦", sort_order=27),
        ]
    )
    
    # ============================================================
    # FRUITS (30+)
    # ============================================================
    FRUITS = OptionGroup(
        name="fruits",
        label="Fruits",
        description="Fruits for educational content",
        icon="🍎",
        sort_order=6,
        options=[
            Option("apple", "Apple", "Crisp red or green fruit", "🍎", sort_order=1),
            Option("banana", "Banana", "Curved yellow potassium-rich fruit", "🍌", sort_order=2),
            Option("orange", "Orange", "Citrus vitamin C powerhouse", "🍊", sort_order=3),
            Option("strawberry", "Strawberry", "Sweet red berry with seeds", "🍓", sort_order=4),
            Option("grape", "Grape", "Small round vine fruit", "🍇", sort_order=5),
            Option("watermelon", "Watermelon", "Large juicy summer melon", "🍉", sort_order=6),
            Option("pineapple", "Pineapple", "Tropical spiky sweet fruit", "🍍", sort_order=7),
            Option("mango", "Mango", "King of tropical fruits", "🥭", sort_order=8),
            Option("peach", "Peach", "Fuzzy stone fruit", "🍑", sort_order=9),
            Option("pear", "Pear", "Teardrop-shaped sweet fruit", "🍐", sort_order=10),
            Option("cherry", "Cherry", "Small red stone fruit", "🍒", sort_order=11),
            Option("blueberry", "Blueberry", "Tiny antioxidant berry", "🫐", sort_order=12),
            Option("raspberry", "Raspberry", "Delicate hollow berry", "🫐", sort_order=13),
            Option("blackberry", "Blackberry", "Dark aggregate fruit", "🫐", sort_order=14),
            Option("kiwi", "Kiwi", "Fuzzy brown, green inside", "🥝", sort_order=15),
            Option("lemon", "Lemon", "Sour yellow citrus", "🍋", sort_order=16),
            Option("lime", "Lime", "Green tart citrus", "🍋", sort_order=17),
            Option("coconut", "Coconut", "Tropical water-filled nut", "🥥", sort_order=18),
            Option("pomegranate", "Pomegranate", "Jewel-seeded superfruit", "🫐", sort_order=19),
            Option("dragon_fruit", "Dragon Fruit", "Vibrant pink cactus fruit", "🐉", sort_order=20),
            Option("papaya", "Papaya", "Orange tropical melon", "🍈", sort_order=21),
            Option("guava", "Guava", "Fragrant tropical fruit", "🍈", sort_order=22),
            Option("lychee", "Lychee", "Floral translucent fruit", "🍈", sort_order=23),
            Option("passion_fruit", "Passion Fruit", "Wrinkly aromatic fruit", "🍈", sort_order=24),
            Option("fig", "Fig", "Sweet ancient fruit", "🍈", sort_order=25),
            Option("date", "Date", "Caramel-like desert fruit", "🌴", sort_order=26),
            Option("apricot", "Apricot", "Small orange stone fruit", "🍑", sort_order=27),
            Option("plum", "Plum", "Purple juicy stone fruit", "🍑", sort_order=28),
            Option("nectarine", "Nectarine", "Smooth-skinned peach", "🍑", sort_order=29),
            Option("cantaloupe", "Cantaloupe", "Orange netted melon", "🍈", sort_order=30),
            Option("honeydew", "Honeydew", "Green sweet melon", "🍈", sort_order=31),
        ]
    )
    
    # ============================================================
    # VEGETABLES (30+)
    # ============================================================
    VEGETABLES = OptionGroup(
        name="vegetables",
        label="Vegetables",
        description="Vegetables for educational content",
        icon="🥕",
        sort_order=7,
        options=[
            Option("carrot", "Carrot", "Orange crunchy root vegetable", "🥕", sort_order=1),
            Option("broccoli", "Broccoli", "Green tree-like florets", "🥦", sort_order=2),
            Option("spinach", "Spinach", "Iron-rich leafy green", "🥬", sort_order=3),
            Option("tomato", "Tomato", "Red juicy fruit-vegetable", "🍅", sort_order=4),
            Option("cucumber", "Cucumber", "Cool crisp green vegetable", "🥒", sort_order=5),
            Option("potato", "Potato", "Versatile starchy tuber", "🥔", sort_order=6),
            Option("sweet_potato", "Sweet Potato", "Orange nutrient-dense root", "🍠", sort_order=7),
            Option("corn", "Corn", "Sweet yellow kernels", "🌽", sort_order=8),
            Option("peas", "Peas", "Green round legumes", "🫛", sort_order=9),
            Option("green_beans", "Green Beans", "Long crisp pods", "🫛", sort_order=10),
            Option("bell_pepper", "Bell Pepper", "Colorful sweet pepper", "🫑", sort_order=11),
            Option("onion", "Onion", "Layered aromatic bulb", "🧅", sort_order=12),
            Option("garlic", "Garlic", "Pungent flavor bulb", "🧄", sort_order=13),
            Option("lettuce", "Lettuce", "Crisp salad green", "🥬", sort_order=14),
            Option("cabbage", "Cabbage", "Dense leafy head", "🥬", sort_order=15),
            Option("cauliflower", "Cauliflower", "White curd vegetable", "🥦", sort_order=16),
            Option("zucchini", "Zucchini", "Green summer squash", "🥒", sort_order=17),
            Option("eggplant", "Eggplant", "Purple glossy vegetable", "🍆", sort_order=18),
            Option("pumpkin", "Pumpkin", "Orange autumn squash", "🎃", sort_order=19),
            Option("radish", "Radish", "Spicy red root", "🌰", sort_order=20),
            Option("beetroot", "Beetroot", "Deep red earthy root", "🌰", sort_order=21),
            Option("celery", "Celery", "Crunchy stalk vegetable", "🌿", sort_order=22),
            Option("asparagus", "Asparagus", "Spring spear vegetable", "🌿", sort_order=23),
            Option("artichoke", "Artichoke", "Thistle flower bud", "🌿", sort_order=24),
            Option("brussels_sprouts", "Brussels Sprouts", "Mini cabbage heads", "🥬", sort_order=25),
            Option("kale", "Kale", "Curly superfood green", "🥬", sort_order=26),
            Option("arugula", "Arugula", "Peppery salad green", "🥬", sort_order=27),
            Option("mushroom", "Mushroom", "Umami fungi", "🍄", sort_order=28),
            Option("avocado", "Avocado", "Creamy healthy fat fruit", "🥑", sort_order=29),
            Option("olive", "Olive", "Mediterranean fruit", "🫒", sort_order=30),
        ]
    )
    
    # ============================================================
    # COUNTRIES (50+)
    # ============================================================
    COUNTRIES = OptionGroup(
        name="countries",
        label="Countries",
        description="Countries of the world",
        icon="🌍",
        sort_order=8,
        options=[
            Option("united_states", "United States", "USA", "🇺🇸", sort_order=1),
            Option("canada", "Canada", "Maple leaf country", "🇨🇦", sort_order=2),
            Option("mexico", "Mexico", "Land of Aztecs", "🇲🇽", sort_order=3),
            Option("brazil", "Brazil", "Amazon rainforest", "🇧🇷", sort_order=4),
            Option("argentina", "Argentina", "Tango and pampas", "🇦🇷", sort_order=5),
            Option("united_kingdom", "United Kingdom", "Britain", "🇬🇧", sort_order=6),
            Option("france", "France", "Eiffel Tower", "🇫🇷", sort_order=7),
            Option("germany", "Germany", "Bavaria and Berlin", "🇩🇪", sort_order=8),
            Option("italy", "Italy", "Pizza and Colosseum", "🇮🇹", sort_order=9),
            Option("spain", "Spain", "Flamenco and paella", "🇪🇸", sort_order=10),
            Option("china", "China", "Great Wall", "🇨🇳", sort_order=11),
            Option("japan", "Japan", "Land of rising sun", "🇯🇵", sort_order=12),
            Option("south_korea", "South Korea", "K-pop and kimchi", "🇰🇷", sort_order=13),
            Option("india", "India", "Taj Mahal", "🇮🇳", sort_order=14),
            Option("australia", "Australia", "Kangaroos and opera house", "🇦🇺", sort_order=15),
            Option("new_zealand", "New Zealand", "Kiwis and hobbits", "🇳🇿", sort_order=16),
            Option("south_africa", "South Africa", "Safari and Table Mountain", "🇿🇦", sort_order=17),
            Option("egypt", "Egypt", "Pyramids and Nile", "🇪🇬", sort_order=18),
            Option("nigeria", "Nigeria", "Giant of Africa", "🇳🇬", sort_order=19),
            Option("kenya", "Kenya", "Maasai Mara", "🇰🇪", sort_order=20),
            Option("russia", "Russia", "Red Square", "🇷🇺", sort_order=21),
            Option("turkey", "Turkey", "Istanbul bridges", "🇹🇷", sort_order=22),
            Option("saudi_arabia", "Saudi Arabia", "Mecca and oil", "🇸🇦", sort_order=23),
            Option("united_arab_emirates", "UAE", "Burj Khalifa", "🇦🇪", sort_order=24),
            Option("israel", "Israel", "Holy Land", "🇮🇱", sort_order=25),
            Option("iran", "Iran", "Persian heritage", "🇮🇷", sort_order=26),
            Option("pakistan", "Pakistan", "K2 mountain", "🇵🇰", sort_order=27),
            Option("bangladesh", "Bangladesh", "Bengal tigers", "🇧🇩", sort_order=28),
            Option("indonesia", "Indonesia", "17,000 islands", "🇮🇩", sort_order=29),
            Option("thailand", "Thailand", "Temples and beaches", "🇹🇭", sort_order=30),
            Option("vietnam", "Vietnam", "Ha Long Bay", "🇻🇳", sort_order=31),
            Option("philippines", "Philippines", "7,641 islands", "🇵🇭", sort_order=32),
            Option("malaysia", "Malaysia", "Petronas Towers", "🇲🇾", sort_order=33),
            Option("singapore", "Singapore", "Garden city", "🇸🇬", sort_order=34),
            Option("sweden", "Sweden", "Northern lights", "🇸🇪", sort_order=35),
            Option("norway", "Norway", "Fjords", "🇳🇴", sort_order=36),
            Option("denmark", "Denmark", "Hygge and Lego", "🇩🇰", sort_order=37),
            Option("finland", "Finland", "Santa's home", "🇫🇮", sort_order=38),
            Option("poland", "Poland", "Pierogi and history", "🇵🇱", sort_order=39),
            Option("netherlands", "Netherlands", "Tulips and canals", "🇳🇱", sort_order=40),
            Option("belgium", "Belgium", "Chocolate and waffles", "🇧🇪", sort_order=41),
            Option("switzerland", "Switzerland", "Alps and chocolate", "🇨🇭", sort_order=42),
            Option("austria", "Austria", "Mozart and Alps", "🇦🇹", sort_order=43),
            Option("greece", "Greece", "Acropolis", "🇬🇷", sort_order=44),
            Option("portugal", "Portugal", "Port wine", "🇵🇹", sort_order=45),
            Option("ireland", "Ireland", "Emerald Isle", "🇮🇪", sort_order=46),
            Option("colombia", "Colombia", "Coffee and emeralds", "🇨🇴", sort_order=47),
            Option("chile", "Chile", "Longest country", "🇨🇱", sort_order=48),
            Option("peru", "Peru", "Machu Picchu", "🇵🇪", sort_order=49),
            Option("argentina", "Argentina", "Tango and pampas", "🇦🇷", sort_order=50),
        ]
    )
    
    # ============================================================
    # COLORS (30+)
    # ============================================================
    COLORS = OptionGroup(
        name="colors",
        label="Colors",
        description="Colors for educational and creative content",
        icon="🎨",
        sort_order=9,
        options=[
            Option("red", "Red", "Passion and energy", "🔴", sort_order=1),
            Option("blue", "Blue", "Calm and trust", "🔵", sort_order=2),
            Option("yellow", "Yellow", "Happiness and sunshine", "🟡", sort_order=3),
            Option("green", "Green", "Nature and growth", "🟢", sort_order=4),
            Option("orange", "Orange", "Creativity and warmth", "🟠", sort_order=5),
            Option("purple", "Purple", "Royalty and magic", "🟣", sort_order=6),
            Option("pink", "Pink", "Love and sweetness", "🩷", sort_order=7),
            Option("brown", "Brown", "Earth and stability", "🟤", sort_order=8),
            Option("black", "Black", "Elegance and mystery", "⚫", sort_order=9),
            Option("white", "White", "Purity and peace", "⚪", sort_order=10),
            Option("gray", "Gray", "Balance and neutrality", "⚪", sort_order=11),
            Option("cyan", "Cyan", "Fresh and modern", "💎", sort_order=12),
            Option("magenta", "Magenta", "Vibrant and bold", "💖", sort_order=13),
            Option("lime", "Lime", "Zesty and energetic", "💚", sort_order=14),
            Option("teal", "Teal", "Sophisticated blue-green", "🦚", sort_order=15),
            Option("indigo", "Indigo", "Deep mystical blue", "🔮", sort_order=16),
            Option("violet", "Violet", "Spiritual purple", "💜", sort_order=17),
            Option("gold", "Gold", "Wealth and success", "🥇", sort_order=18),
            Option("silver", "Silver", "Modern and sleek", "🥈", sort_order=19),
            Option("bronze", "Bronze", "Warm metallic", "🥉", sort_order=20),
            Option("coral", "Coral", "Warm pink-orange", "🪸", sort_order=21),
            Option("turquoise", "Turquoise", "Tropical ocean", "🏝️", sort_order=22),
            Option("lavender", "Lavender", "Calming purple", "🪻", sort_order=23),
            Option("maroon", "Maroon", "Deep rich red", "🍷", sort_order=24),
            Option("navy", "Navy", "Professional dark blue", "🌊", sort_order=25),
            Option("olive", "Olive", "Military green", "🫒", sort_order=26),
            Option("peach", "Peach", "Soft warm orange", "🍑", sort_order=27),
            Option("mint", "Mint", "Fresh pale green", "🌿", sort_order=28),
            Option("salmon", "Salmon", "Pink-orange fish tone", "🐟", sort_order=29),
            Option("tan", "Tan", "Warm sandy beige", "🏖️", sort_order=30),
        ]
    )
    
    # ============================================================
    # OCCUPATIONS (40+)
    # ============================================================
    OCCUPATIONS = OptionGroup(
        name="occupations",
        label="Occupations",
        description="Professions and jobs for educational content",
        icon="💼",
        sort_order=10,
        options=[
            Option("teacher", "Teacher", "Educator shaping young minds", "👩‍🏫", sort_order=1),
            Option("doctor", "Doctor", "Healer and physician", "👨‍⚕️", sort_order=2),
            Option("nurse", "Nurse", "Compassionate caregiver", "👩‍⚕️", sort_order=3),
            Option("firefighter", "Firefighter", "Brave rescue hero", "👨‍🚒", sort_order=4),
            Option("police_officer", "Police Officer", "Community protector", "👮", sort_order=5),
            Option("astronaut", "Astronaut", "Space explorer", "👨‍🚀", sort_order=6),
            Option("engineer", "Engineer", "Problem solver", "👨‍💻", sort_order=7),
            Option("scientist", "Scientist", "Discovery researcher", "👩‍🔬", sort_order=8),
            Option("artist", "Artist", "Creative visionary", "🎨", sort_order=9),
            Option("musician", "Musician", "Melody maker", "🎵", sort_order=10),
            Option("chef", "Chef", "Culinary artist", "👨‍🍳", sort_order=11),
            Option("baker", "Baker", "Bread and pastry maker", "🍞", sort_order=12),
            Option("farmer", "Farmer", "Food producer", "👨‍🌾", sort_order=13),
            Option("veterinarian", "Veterinarian", "Animal doctor", "👩‍⚕️", sort_order=14),
            Option("dentist", "Dentist", "Tooth doctor", "🦷", sort_order=15),
            Option("pilot", "Pilot", "Sky navigator", "✈️", sort_order=16),
            Option("captain", "Ship Captain", "Ocean commander", "⚓", sort_order=17),
            Option("architect", "Architect", "Building designer", "🏗️", sort_order=18),
            Option("construction_worker", "Construction Worker", "Builder", "👷", sort_order=19),
            Option("electrician", "Electrician", "Power specialist", "⚡", sort_order=20),
            Option("plumber", "Plumber", "Pipe expert", "🔧", sort_order=21),
            Option("mechanic", "Mechanic", "Vehicle fixer", "🔧", sort_order=22),
            Option("librarian", "Librarian", "Knowledge keeper", "📚", sort_order=23),
            Option("journalist", "Journalist", "Truth seeker", "📰", sort_order=24),
            Option("writer", "Writer", "Story creator", "✍️", sort_order=25),
            Option("actor", "Actor", "Character performer", "🎭", sort_order=26),
            Option("dancer", "Dancer", "Movement artist", "💃", sort_order=27),
            Option("singer", "Singer", "Voice artist", "🎤", sort_order=28),
            Option("photographer", "Photographer", "Moment capturer", "📸", sort_order=29),
            Option("designer", "Designer", "Visual problem solver", "🎨", sort_order=30),
            Option("programmer", "Programmer", "Code creator", "💻", sort_order=31),
            Option("data_scientist", "Data Scientist", "Insight finder", "📊", sort_order=32),
            Option("lawyer", "Lawyer", "Justice advocate", "⚖️", sort_order=33),
            Option("judge", "Judge", "Fair arbiter", "⚖️", sort_order=34),
            Option("accountant", "Accountant", "Number expert", "🧮", sort_order=35),
            Option("banker", "Banker", "Finance manager", "🏦", sort_order=36),
            Option("entrepreneur", "Entrepreneur", "Business creator", "🚀", sort_order=37),
            Option("manager", "Manager", "Team leader", "👔", sort_order=38),
            Option("receptionist", "Receptionist", "Front desk coordinator", "📞", sort_order=39),
            Option("driver", "Driver", "Transport operator", "🚗", sort_order=40),
        ]
    )
    
    # ============================================================
    # SPORTS (40+)
    # ============================================================
    SPORTS = OptionGroup(
        name="sports",
        label="Sports",
        description="Sports and physical activities",
        icon="⚽",
        sort_order=11,
        options=[
            Option("soccer", "Soccer/Football", "World's most popular sport", "⚽", sort_order=1),
            Option("basketball", "Basketball", "Hoops and dunks", "🏀", sort_order=2),
            Option("tennis", "Tennis", "Racket sport", "🎾", sort_order=3),
            Option("baseball", "Baseball", "America's pastime", "⚾", sort_order=4),
            Option("football_american", "American Football", "Gridiron", "🏈", sort_order=5),
            Option("swimming", "Swimming", "Water sport", "🏊", sort_order=6),
            Option("running", "Running", "Track and field", "🏃", sort_order=7),
            Option("cycling", "Cycling", "Two-wheel speed", "🚴", sort_order=8),
            Option("gymnastics", "Gymnastics", "Flexibility and strength", "🤸", sort_order=9),
            Option("dance", "Dance", "Artistic movement", "💃", sort_order=10),
            Option("martial_arts", "Martial Arts", "Discipline and defense", "🥋", sort_order=11),
            Option("karate", "Karate", "Striking art", "🥋", sort_order=12),
            Option("judo", "Judo", "Gentle way", "🥋", sort_order=13),
            Option("taekwondo", "Taekwondo", "Korean kicking art", "🥋", sort_order=14),
            Option("boxing", "Boxing", "Sweet science", "🥊", sort_order=15),
            Option("wrestling", "Wrestling", "Grappling sport", "🤼", sort_order=16),
            Option("volleyball", "Volleyball", "Net sport", "🏐", sort_order=17),
            Option("badminton", "Badminton", "Shuttlecock sport", "🏸", sort_order=18),
            Option("table_tennis", "Table Tennis", "Ping pong", "🏓", sort_order=19),
            Option("golf", "Golf", "Precision club sport", "⛳", sort_order=20),
            Option("skiing", "Skiing", "Snow slopes", "⛷️", sort_order=21),
            Option("snowboarding", "Snowboarding", "Sideways snow", "🏂", sort_order=22),
            Option("ice_skating", "Ice Skating", "Frozen grace", "⛸️", sort_order=23),
            Option("hockey", "Hockey", "Ice/field stick sport", "🏒", sort_order=24),
            Option("rugby", "Rugby", "Oval ball contact", "🏉", sort_order=25),
            Option("cricket", "Cricket", "Bat and ball", "🏏", sort_order=26),
            Option("surfing", "Surfing", "Wave riding", "🏄", sort_order=27),
            Option("skateboarding", "Skateboarding", "Board tricks", "🛹", sort_order=28),
            Option("climbing", "Rock Climbing", "Vertical ascent", "🧗", sort_order=29),
            Option("hiking", "Hiking", "Nature walking", "🥾", sort_order=30),
            Option("yoga", "Yoga", "Mind-body practice", "🧘", sort_order=31),
            Option("pilates", "Pilates", "Core strength", "🧘", sort_order=32),
            Option("weightlifting", "Weightlifting", "Strength training", "🏋️", sort_order=33),
            Option("rowing", "Rowing", "Water power", "🚣", sort_order=34),
            Option("kayaking", "Kayaking", "Paddle sport", "🛶", sort_order=35),
            Option("sailing", "Sailing", "Wind power", "⛵", sort_order=36),
            Option("fencing", "Fencing", "Sword sport", "🤺", sort_order=37),
            Option("archery", "Archery", "Bow and arrow", "🏹", sort_order=38),
            Option("equestrian", "Equestrian", "Horse riding", "🏇", sort_order=39),
            Option("diving", "Diving", "Acrobatic water entry", "🤿", sort_order=40),
        ]
    )
    
    # ============================================================
    # FLOWERS (30+)
    # ============================================================
    FLOWERS = OptionGroup(
        name="flowers",
        label="Flowers",
        description="Flowers for educational content",
        icon="🌸",
        sort_order=12,
        options=[
            Option("rose", "Rose", "Classic symbol of love", "🌹", sort_order=1),
            Option("tulip", "Tulip", "Spring bulb flower", "🌷", sort_order=2),
            Option("sunflower", "Sunflower", "Sun-following giant", "🌻", sort_order=3),
            Option("daisy", "Daisy", "Innocent white petals", "🌼", sort_order=4),
            Option("orchid", "Orchid", "Exotic elegant bloom", "🌸", sort_order=5),
            Option("lily", "Lily", "Fragrant trumpet flower", "🌸", sort_order=6),
            Option("lotus", "Lotus", "Sacred water flower", "🪷", sort_order=7),
            Option("cherry_blossom", "Cherry Blossom", "Japanese sakura", "🌸", sort_order=8),
            Option("lavender", "Lavender", "Purple fragrant herb", "🪻", sort_order=9),
            Option("peony", "Peony", "Lush romantic bloom", "🌸", sort_order=10),
            Option("hydrangea", "Hydrangea", "Color-changing clusters", "🌸", sort_order=11),
            Option("iris", "Iris", "Rainbow goddess flower", "🌸", sort_order=12),
            Option("daffodil", "Daffodil", "Spring trumpet", "🌼", sort_order=13),
            Option("marigold", "Marigold", "Golden festival flower", "🌼", sort_order=14),
            Option("poppy", "Poppy", "Delicate red petals", "🌺", sort_order=15),
            Option("hibiscus", "Hibiscus", "Tropical showy bloom", "🌺", sort_order=16),
            Option("bougainvillea", "Bougainvillea", "Vibrant paper bracts", "🌺", sort_order=17),
            Option("magnolia", "Magnolia", "Ancient fragrant tree flower", "🌸", sort_order=18),
            Option("camellia", "Camellia", "Winter rose", "🌸", sort_order=19),
            Option("azalea", "Azalea", "Spring shrub bloom", "🌸", sort_order=20),
            Option("rhododendron", "Rhododendron", "Mountain bell flower", "🌸", sort_order=21),
            Option("gardenia", "Gardenia", "Intense fragrance", "🌸", sort_order=22),
            Option("jasmine", "Jasmine", "Night-blooming scent", "🌸", sort_order=23),
            Option("violet", "Violet", "Tiny purple charm", "🌸", sort_order=24),
            Option("pansy", "Pansy", "Face-like petals", "🌸", sort_order=25),
            Option("snapdragon", "Snapdragon", "Dragon-mouth flower", "🌸", sort_order=26),
            Option("foxglove", "Foxglove", "Tall bell spires", "🌸", sort_order=27),
            Option("delphinium", "Delphinium", "Tall blue spikes", "🌸", sort_order=28),
            Option("lupine", "Lupine", "Pea-family spires", "🌸", sort_order=29),
            Option("wisteria", "Wisteria", "Cascading purple chains", "🌸", sort_order=30),
        ]
    )
    
    # ============================================================
    # VEHICLES (40+)
    # ============================================================
    VEHICLES = OptionGroup(
        name="vehicles",
        label="Vehicles",
        description="Transportation vehicles for educational content",
        icon="🚗",
        sort_order=13,
        options=[
            Option("car", "Car", "Personal automobile", "🚗", sort_order=1),
            Option("bus", "Bus", "Public transport", "🚌", sort_order=2),
            Option("truck", "Truck", "Heavy cargo hauler", "🚛", sort_order=3),
            Option("motorcycle", "Motorcycle", "Two-wheel speed", "🏍️", sort_order=4),
            Option("bicycle", "Bicycle", "Pedal power", "🚲", sort_order=5),
            Option("train", "Train", "Rail transport", "🚂", sort_order=6),
            Option("subway", "Subway", "Underground metro", "🚇", sort_order=7),
            Option("tram", "Tram", "Streetcar", "🚋", sort_order=8),
            Option("airplane", "Airplane", "Sky travel", "✈️", sort_order=9),
            Option("helicopter", "Helicopter", "Vertical flight", "🚁", sort_order=10),
            Option("rocket", "Rocket", "Space launch", "🚀", sort_order=11),
            Option("boat", "Boat", "Water vessel", "⛵", sort_order=12),
            Option("ship", "Ship", "Ocean liner", "🚢", sort_order=13),
            Option("submarine", "Submarine", "Underwater vessel", "🛥️", sort_order=14),
            Option("ferry", "Ferry", "Car-carrying boat", "⛴️", sort_order=15),
            Option("yacht", "Yacht", "Luxury boat", "🛥️", sort_order=16),
            Option("canoe", "Canoe", "Paddle boat", "🛶", sort_order=17),
            Option("kayak", "Kayak", "Solo paddle craft", "🛶", sort_order=18),
            Option("scooter", "Scooter", "Stand-up ride", "🛴", sort_order=19),
            Option("skateboard", "Skateboard", "Four-wheel board", "🛹", sort_order=20),
            Option("rollerblades", "Rollerblades", "Inline skates", "🛼", sort_order=21),
            Option("tractor", "Tractor", "Farm workhorse", "🚜", sort_order=22),
            Option("excavator", "Excavator", "Digging machine", "🏗️", sort_order=23),
            Option("bulldozer", "Bulldozer", "Earth pusher", "🚜", sort_order=24),
            Option("crane", "Crane", "Heavy lifter", "🏗️", sort_order=25),
            Option("dump_truck", "Dump Truck", "Dirt hauler", "🚛", sort_order=26),
            Option("fire_truck", "Fire Truck", "Emergency responder", "🚒", sort_order=27),
            Option("ambulance", "Ambulance", "Medical emergency", "🚑", sort_order=28),
            Option("police_car", "Police Car", "Law enforcement", "🚓", sort_order=29),
            Option("taxi", "Taxi", "Hired ride", "🚕", sort_order=30),
            Option("limousine", "Limousine", "Luxury stretch", "🚗", sort_order=31),
            Option("van", "Van", "Cargo/passenger box", "🚐", sort_order=32),
            Option("rv", "RV", "Home on wheels", "🚐", sort_order=33),
            Option("pickup_truck", "Pickup Truck", "Open bed utility", "🛻", sort_order=34),
            Option("suv", "SUV", "Sport utility vehicle", "🚙", sort_order=35),
            Option("convertible", "Convertible", "Top-down fun", "🚗", sort_order=36),
            Option("electric_car", "Electric Car", "Zero emissions", "🔌", sort_order=37),
            Option("hovercraft", "Hovercraft", "Air cushion vehicle", "🛸", sort_order=38),
            Option("hot_air_balloon", "Hot Air Balloon", "Gentle sky drift", "🎈", sort_order=39),
            Option("blimp", "Blimp", "Airship", "🎈", sort_order=40),
        ]
    )
    
    # ============================================================
    # CAMERA ANGLES (20+)
    # ============================================================
    CAMERA_ANGLES = OptionGroup(
        name="camera_angles",
        label="Camera Angles",
        description="Cinematic camera angles for image/video generation",
        icon="📷",
        sort_order=14,
        options=[
            Option("eye_level", "Eye Level", "Natural human perspective", "👁️", sort_order=1),
            Option("low_angle", "Low Angle", "Looking up - powerful/heroic", "📷", sort_order=2),
            Option("high_angle", "High Angle", "Looking down - vulnerable/small", "📷", sort_order=3),
            Option("birds_eye", "Bird's Eye View", "Directly overhead", "🦅", sort_order=4),
            Option("worms_eye", "Worm's Eye View", "Extreme low angle", "🪱", sort_order=5),
            Option("dutch_angle", "Dutch Angle", "Tilted - tension/unease", "📐", sort_order=6),
            Option("over_shoulder", "Over Shoulder", "POV from behind subject", "👤", sort_order=7),
            Option("pov", "POV (Point of View)", "First-person perspective", "👁️", sort_order=8),
            Option("close_up", "Close Up", "Face/detail focus", "🔍", sort_order=9),
            Option("extreme_close_up", "Extreme Close Up", "Eye/mouth detail", "🔬", sort_order=10),
            Option("medium_shot", "Medium Shot", "Waist up", "📷", sort_order=11),
            Option("full_shot", "Full Shot", "Head to toe", "📷", sort_order=12),
            Option("wide_shot", "Wide Shot", "Subject in environment", "🌄", sort_order=13),
            Option("establishing_shot", "Establishing Shot", "Location context", "🏙️", sort_order=14),
            Option("two_shot", "Two Shot", "Two people in frame", "👥", sort_order=15),
            Option("group_shot", "Group Shot", "Multiple people", "👨‍👩‍👧‍👦", sort_order=16),
            Option("detail_shot", "Detail Shot", "Specific object focus", "🔍", sort_order=17),
            Option("reaction_shot", "Reaction Shot", "Emotional response", "😮", sort_order=18),
            Option("insert_shot", "Insert Shot", "Important detail cutaway", "✂️", sort_order=19),
            Option("aerial", "Aerial/Drone", "High altitude view", "🚁", sort_order=20),
        ]
    )
    
    # ============================================================
    # LIGHTING STYLES (20+)
    # ============================================================
    LIGHTING_STYLES = OptionGroup(
        name="lighting_styles",
        label="Lighting Styles",
        description="Professional lighting setups for image/video generation",
        icon="💡",
        sort_order=15,
        options=[
            Option("natural", "Natural Light", "Sunlight/daylight", "☀️", sort_order=1),
            Option("golden_hour", "Golden Hour", "Warm sunset/sunrise glow", "🌅", sort_order=2),
            Option("blue_hour", "Blue Hour", "Twilight cool tones", "🌃", sort_order=3),
            Option("studio", "Studio Lighting", "Controlled professional setup", "🎬", sort_order=4),
            Option("three_point", "Three-Point Lighting", "Key, fill, backlight classic", "💡", sort_order=5),
            Option("key_light", "Key Light Only", "Dramatic single source", "🔦", sort_order=6),
            Option("rim_light", "Rim/Backlight", "Silhouette outline", "✨", sort_order=7),
            Option("softbox", "Softbox", "Diffused soft shadows", "☁️", sort_order=8),
            Option("ring_light", "Ring Light", "Even circular catchlights", "💍", sort_order=9),
            Option("neon", "Neon Lighting", "Cyberpunk colorful glow", "🌈", sort_order=10),
            Option("candlelight", "Candlelight", "Warm intimate flicker", "🕯️", sort_order=11),
            Option("firelight", "Firelight", "Dancing warm shadows", "🔥", sort_order=12),
            Option("moonlight", "Moonlight", "Cool silver night", "🌙", sort_order=13),
            Option("chiaroscuro", "Chiaroscuro", "High contrast drama", "🎭", sort_order=14),
            Option("high_key", "High Key", "Bright minimal shadows", "☀️", sort_order=15),
            Option("low_key", "Low Key", "Dark moody atmosphere", "🌑", sort_order=16),
            Option("volumetric", "Volumetric/God Rays", "Light beams in atmosphere", "⛅", sort_order=17),
            Option("bioluminescent", "Bioluminescent", "Glowing organisms", "✨", sort_order=18),
            Option("iridescent", "Iridescent", "Color-shifting shimmer", "🌈", sort_order=19),
            Option("holographic", "Holographic", "Futuristic projection", "🤖", sort_order=20),
        ]
    )
    
    # ============================================================
    # ART STYLES (40+)
    # ============================================================
    ART_STYLES = OptionGroup(
        name="art_styles",
        label="Art Styles",
        description="Artistic styles for image generation",
        icon="🎨",
        sort_order=16,
        options=[
            Option("photorealistic", "Photorealistic", "Indistinguishable from photo", "📸", sort_order=1),
            Option("hyperrealistic", "Hyperrealistic", "Beyond photo detail", "🔬", sort_order=2),
            Option("cinematic", "Cinematic", "Movie still aesthetic", "🎬", sort_order=3),
            Option("disney", "Disney Animation", "Classic Disney style", "🏰", sort_order=4),
            Option("pixar", "Pixar 3D", "Pixar render style", "🎮", sort_order=5),
            Option("dreamworks", "DreamWorks", "DreamWorks animation", "🎮", sort_order=6),
            Option("anime", "Anime", "Japanese animation", "🇯🇵", sort_order=7),
            Option("manga", "Manga", "Japanese comic style", "📖", sort_order=8),
            Option("studio_ghibli", "Studio Ghibli", "Miyazaki whimsical", "🏞️", sort_order=9),
            Option("webtoon", "Webtoon", "Korean vertical comic", "📱", sort_order=10),
            Option("comic_book", "Comic Book", "Western comic panels", "🦸", sort_order=11),
            Option("graphic_novel", "Graphic Novel", "Mature comic style", "📚", sort_order=12),
            Option("watercolor", "Watercolor", "Transparent washes", "🎨", sort_order=13),
            Option("oil_painting", "Oil Painting", "Thick textured brushstrokes", "🖼️", sort_order=14),
            Option("acrylic", "Acrylic", "Modern fast-dry paint", "🎨", sort_order=15),
            Option("pastel", "Pastel", "Soft chalky colors", "🎨", sort_order=16),
            Option("charcoal", "Charcoal", "Dramatic black & white", "⚫", sort_order=17),
            Option("pencil_sketch", "Pencil Sketch", "Graphite drawing", "✏️", sort_order=18),
            Option("ink_drawing", "Ink Drawing", "Line art with brush/pen", "🖋️", sort_order=19),
            Option("digital_art", "Digital Painting", "Tablet painted", "💻", sort_order=20),
            Option("concept_art", "Concept Art", "Game/film pre-production", "🎮", sort_order=21),
            Option("matte_painting", "Matte Painting", "VFX background art", "🎬", sort_order=22),
            Option("pixel_art", "Pixel Art", "Retro game aesthetic", "👾", sort_order=23),
            Option("voxel", "Voxel Art", "3D pixel blocks", "🧱", sort_order=24),
            Option("low_poly", "Low Poly", "Geometric 3D style", "🔺", sort_order=25),
            Option("isometric", "Isometric", "2.5D game view", "📐", sort_order=26),
            Option("vector", "Vector Art", "Clean scalable lines", "📐", sort_order=27),
            Option("flat_design", "Flat Design", "Minimal 2D", "📱", sort_order=28),
            Option("material_design", "Material Design", "Google design language", "📱", sort_order=29),
            Option("neumorphism", "Neumorphism", "Soft UI extrusion", "📱", sort_order=30),
            Option("glassmorphism", "Glassmorphism", "Frosted glass UI", "🔮", sort_order=31),
            Option("brutalism", "Brutalism", "Raw concrete aesthetic", "🏢", sort_order=32),
            Option("cyberpunk", "Cyberpunk", "High tech low life", "🌃", sort_order=33),
            Option("steampunk", "Steampunk", "Victorian sci-fi", "⚙️", sort_order=34),
            Option("dieselpunk", "Dieselpunk", "1940s retro-future", "⚙️", sort_order=35),
            Option("solarpunk", "Solarpunk", "Green utopian future", "🌿", sort_order=36),
            Option("fantasy", "Fantasy Art", "Magic and dragons", "🏰", sort_order=37),
            Option("sci_fi", "Sci-Fi", "Futuristic technology", "🚀", sort_order=38),
            Option("horror", "Horror", "Dark scary aesthetic", "👻", sort_order=39),
            Option("noir", "Film Noir", "Black white crime drama", "🕵️", sort_order=40),
        ]
    )
    
    # ============================================================
    # ANIMATION STYLES (25+)
    # ============================================================
    ANIMATION_STYLES = OptionGroup(
        name="animation_styles",
        label="Animation Styles",
        description="Animation styles for video generation",
        icon="🎬",
        sort_order=17,
        options=[
            Option("2d_traditional", "2D Traditional", "Hand-drawn frame by frame", "🎨", sort_order=1),
            Option("2d_digital", "2D Digital", "Toon Boom/TVPaint style", "💻", sort_order=2),
            Option("3d_cgi", "3D CGI", "Maya/Blender/C4D render", "🎮", sort_order=3),
            Option("stop_motion", "Stop Motion", "Physical object animation", "📸", sort_order=4),
            Option("claymation", "Claymation", "Clay figure animation", "🧱", sort_order=5),
            Option("cutout", "Cutout Animation", "Paper/digital puppets", "✂️", sort_order=6),
            Option("motion_graphics", "Motion Graphics", "Design-driven animation", "📊", sort_order=7),
            Option("whiteboard", "Whiteboard Animation", "Hand-drawn explanation", "📝", sort_order=8),
            Option("kinetic_typography", "Kinetic Typography", "Animated text", "🔤", sort_order=9),
            Option("rotoscope", "Rotoscoping", "Traced over footage", "🎞️", sort_order=10),
            Option("anime", "Anime", "Japanese limited animation", "🇯🇵", sort_order=11),
            Option("western_tv", "Western TV Animation", "Simpsons/Family Guy style", "📺", sort_order=12),
            Option("disney_feature", "Disney Feature", "Full theatrical quality", "🏰", sort_order=13),
            Option("pixar_feature", "Pixar Feature", "High-end 3D feature", "🎮", sort_order=14),
            Option("spider_verse", "Spider-Verse Style", "Comic book 3D hybrid", "🕷️", sort_order=15),
            Option("arcane", "Arcane Style", "2D/3D painted hybrid", "🎨", sort_order=16),
            Option("pixel_animation", "Pixel Animation", "Frame-by-frame pixel art", "👾", sort_order=17),
            Option("vector_animation", "Vector Animation", "Scalable clean motion", "📐", sort_order=18),
            Option("procedural", "Procedural Animation", "Code-driven motion", "💻", sort_order=19),
            Option("physics_based", "Physics-Based", "Simulation driven", "⚛️", sort_order=20),
            Option("motion_capture", "Motion Capture", "Actor-driven 3D", "🎭", sort_order=21),
            Option("ai_generated", "AI Generated", "Neural network frames", "🤖", sort_order=22),
            Option("interpolated", "Frame Interpolation", "AI smooth motion", "✨", sort_order=23),
            Option("time_lapse", "Time-lapse", "Accelerated time", "⏱️", sort_order=24),
            Option("stop_motion_lego", "LEGO Stop Motion", "Brick animation", "🧱", sort_order=25),
        ]
    )
    
    # ============================================================
    # ASPECT RATIOS (All common)
    # ============================================================
    ASPECT_RATIOS = OptionGroup(
        name="aspect_ratios",
        label="Aspect Ratios",
        description="Standard aspect ratios for media",
        icon="📐",
        sort_order=18,
        options=[
            Option("16:9", "16:9 (Widescreen)", "Standard HD video", "📺", sort_order=1),
            Option("9:16", "9:16 (Vertical)", "TikTok/Reels/Shorts", "📱", sort_order=2),
            Option("4:3", "4:3 (Standard)", "Classic TV/Monitor", "📺", sort_order=3),
            Option("1:1", "1:1 (Square)", "Instagram post", "📱", sort_order=4),
            Option("4:5", "4:5 (Portrait)", "Instagram portrait", "📱", sort_order=5),
            Option("3:2", "3:2 (Photo)", "35mm photography", "📸", sort_order=6),
            Option("2:3", "2:3 (Vertical Photo)", "Portrait photography", "📸", sort_order=7),
            Option("21:9", "21:9 (Ultrawide)", "Cinematic anamorphic", "🎬", sort_order=8),
            Option("2.39:1", "2.39:1 (CinemaScope)", "Hollywood cinema", "🎬", sort_order=9),
            Option("1.85:1", "1.85:1 (Flat)", "Standard cinema", "🎬", sort_order=10),
            Option("3:4", "3:4 (Tall)", "Pinterest/portrait", "📱", sort_order=11),
            Option("5:4", "5:4 (Large Format)", "Large format photo", "📸", sort_order=12),
        ]
    )
    
    # ============================================================
    # QUALITY PRESETS
    # ============================================================
    QUALITY_PRESETS = OptionGroup(
        name="quality_presets",
        label="Quality Presets",
        description="Output quality levels",
        icon="⭐",
        sort_order=19,
        options=[
            Option("draft", "Draft", "Fast, low quality for testing", "⚡", sort_order=1),
            Option("standard", "Standard", "Balanced quality/speed", "✅", sort_order=2),
            Option("high", "High", "Production quality", "⭐", sort_order=3),
            Option("ultra", "Ultra", "Maximum detail", "⭐⭐", sort_order=4),
            Option("4k", "4K", "3840x2160 resolution", "🖥️", sort_order=5),
            Option("8k", "8K", "7680x4320 resolution", "🖥️🖥️", sort_order=6),
            Option("print_ready", "Print Ready", "300 DPI output", "🖨️", sort_order=7),
            Option("web_optimized", "Web Optimized", "Fast loading, good quality", "🌐", sort_order=8),
        ]
    )
    
    # ============================================================
    # RESOLUTIONS
    # ============================================================
    RESOLUTIONS = OptionGroup(
        name="resolutions",
        label="Resolutions",
        description="Output resolutions",
        icon="🖥️",
        sort_order=20,
        options=[
            Option("640x360", "360p (640×360)", "Low bandwidth", "📱", sort_order=1),
            Option("854x480", "480p (854×480)", "SD quality", "📺", sort_order=2),
            Option("1280x720", "720p HD (1280×720)", "HD ready", "📺", sort_order=3),
            Option("1920x1080", "1080p Full HD (1920×1080)", "Standard HD", "🖥️", sort_order=4),
            Option("2560x1440", "1440p QHD (2560×1440)", "2K quality", "🖥️", sort_order=5),
            Option("3840x2160", "2160p 4K UHD (3840×2160)", "4K Ultra HD", "🖥️", sort_order=6),
            Option("7680x4320", "4320p 8K UHD (7680×4320)", "8K Ultra HD", "🖥️🖥️", sort_order=7),
            Option("512x512", "512×512 (Square)", "AI model standard", "🤖", sort_order=8),
            Option("1024x1024", "1024×1024 (Square)", "High-res square", "🤖", sort_order=9),
            Option("2048x2048", "2048×2048 (Square)", "Ultra square", "🤖", sort_order=10),
        ]
    )
    
    # ============================================================
    # EMOTIONS
    # ============================================================
    EMOTIONS = OptionGroup(
        name="emotions",
        label="Emotions",
        description="Emotional states for characters and voices",
        icon="😊",
        sort_order=21,
        options=[
            Option("happy", "Happy", "Joyful and cheerful", "😄", sort_order=1),
            Option("sad", "Sad", "Melancholy and down", "😢", sort_order=2),
            Option("angry", "Angry", "Furious and mad", "😠", sort_order=3),
            Option("excited", "Excited", "Thrilled and energetic", "🤩", sort_order=4),
            Option("calm", "Calm", "Peaceful and relaxed", "😌", sort_order=5),
            Option("surprised", "Surprised", "Shocked and amazed", "😲", sort_order=6),
            Option("fearful", "Fearful", "Scared and anxious", "😨", sort_order=7),
            Option("disgusted", "Disgusted", "Repulsed and grossed out", "🤢", sort_order=8),
            Option("curious", "Curious", "Inquisitive and wondering", "🤔", sort_order=9),
            Option("confused", "Confused", "Puzzled and uncertain", "😕", sort_order=10),
            Option("proud", "Proud", "Accomplished and confident", "😤", sort_order=11),
            Option("embarrassed", "Embarrassed", "Shy and self-conscious", "😳", sort_order=12),
            Option("grateful", "Grateful", "Thankful and appreciative", "🙏", sort_order=13),
            Option("hopeful", "Hopeful", "Optimistic and expecting", "🌈", sort_order=14),
            Option("lonely", "Lonely", "Isolated and alone", "😔", sort_order=15),
            Option("loving", "Loving", "Affectionate and warm", "❤️", sort_order=16),
            Option("playful", "Playful", "Fun and mischievous", "😜", sort_order=17),
            Option("serious", "Serious", "Focused and grave", "😐", sort_order=18),
            Option("determined", "Determined", "Resolute and driven", "💪", sort_order=19),
            Option("relaxed", "Relaxed", "Chill and easygoing", "😎", sort_order=20),
        ]
    )
    
    # ============================================================
    # AGES / AGE GROUPS
    # ============================================================
    AGE_GROUPS = OptionGroup(
        name="age_groups",
        label="Age Groups",
        description="Target age groups for content",
        icon="👶",
        sort_order=22,
        options=[
            Option("infant", "Infant (0-1)", "Babies", "👶", sort_order=1),
            Option("toddler", "Toddler (1-3)", "Early walkers", "🚼", sort_order=2),
            Option("preschool", "Preschool (3-5)", "Pre-kindergarten", "🏫", sort_order=3),
            Option("early_childhood", "Early Childhood (5-7)", "Kindergarten-1st grade", "🎒", sort_order=4),
            Option("middle_childhood", "Middle Childhood (7-11)", "Elementary school", "🏫", sort_order=5),
            Option("preteens", "Preteens (11-13)", "Middle school", "📚", sort_order=6),
            Option("teens", "Teens (13-18)", "High school", "🎓", sort_order=7),
            Option("young_adults", "Young Adults (18-25)", "College/early career", "🎓", sort_order=8),
            Option("adults", "Adults (25-65)", "Working age", "💼", sort_order=9),
            Option("seniors", "Seniors (65+)", "Retirement age", "👴", sort_order=10),
            Option("all_ages", "All Ages", "Family friendly", "👨‍👩‍👧‍👦", sort_order=11),
        ]
    )
    
    # ============================================================
    # STORY GENRES
    # ============================================================
    STORY_GENRES = OptionGroup(
        name="story_genres",
        label="Story Genres",
        description="Literary genres for story generation",
        icon="📚",
        sort_order=23,
        options=[
            Option("adventure", "Adventure", "Journey and discovery", "🗺️", sort_order=1),
            Option("fantasy", "Fantasy", "Magic and mythical worlds", "🏰", sort_order=2),
            Option("fairy_tale", "Fairy Tale", "Classic folk stories", "🧚", sort_order=3),
            Option("fable", "Fable", "Moral animal stories", "🦊", sort_order=4),
            Option("mythology", "Mythology", "Gods and legends", "⚡", sort_order=5),
            Option("science_fiction", "Science Fiction", "Future and technology", "🚀", sort_order=6),
            Option("mystery", "Mystery", "Puzzle and detection", "🔍", sort_order=7),
            Option("detective", "Detective", "Crime solving", "🕵️", sort_order=8),
            Option("historical", "Historical Fiction", "Past events dramatized", "🏛️", sort_order=9),
            Option("realistic", "Realistic Fiction", "Everyday life stories", "🏠", sort_order=10),
            Option("humor", "Humor/Comedy", "Funny and entertaining", "😂", sort_order=11),
            Option("horror", "Horror", "Scary and suspenseful", "👻", sort_order=12),
            Option("thriller", "Thriller", "High tension excitement", "😰", sort_order=13),
            Option("romance", "Romance", "Love and relationships", "💕", sort_order=14),
            Option("friendship", "Friendship", "Bonds and loyalty", "🤝", sort_order=15),
            Option("school", "School Stories", "Classroom adventures", "🏫", sort_order=16),
            Option("family", "Family", "Home and relatives", "👨‍👩‍👧‍👦", sort_order=17),
            Option("animals", "Animal Stories", "Creature protagonists", "🐾", sort_order=18),
            Option("space", "Space Adventure", "Cosmic journeys", "🌌", sort_order=19),
            Option("underwater", "Underwater", "Ocean exploration", "🌊", sort_order=20),
            Option("time_travel", "Time Travel", "Past and future jumps", "⏰", sort_order=21),
            Option("superhero", "Superhero", "Powers and justice", "🦸", sort_order=22),
            Option("magical_realism", "Magical Realism", "Magic in real world", "✨", sort_order=23),
            Option("dystopian", "Dystopian", "Dark future society", "🌪️", sort_order=24),
            Option("utopian", "Utopian", "Perfect society", "🌈", sort_order=25),
        ]
    )
    
    # ============================================================
    # STORY LENGTHS
    # ============================================================
    STORY_LENGTHS = OptionGroup(
        name="story_lengths",
        label="Story Lengths",
        description="Length options for generated stories",
        icon="📏",
        sort_order=24,
        options=[
            Option("micro", "Micro (50-100 words)", "Tiny tale", "📝", sort_order=1),
            Option("short", "Short (100-500 words)", "Quick read", "📄", sort_order=2),
            Option("medium", "Medium (500-2000 words)", "Standard story", "📖", sort_order=3),
            Option("long", "Long (2000-5000 words)", "Chapter length", "📚", sort_order=4),
            Option("novella", "Novella (5000-20000 words)", "Short novel", "📚📚", sort_order=5),
            Option("novel", "Novel (20000+ words)", "Full book", "📚📚📚", sort_order=6),
        ]
    )
    
    # ============================================================
    # STORY STYLES
    # ============================================================
    STORY_STYLES = OptionGroup(
        name="story_styles",
        label="Story Styles",
        description="Narrative styles for story generation",
        icon="✍️",
        sort_order=25,
        options=[
            Option("narrative", "Narrative", "Traditional storytelling", "📖", sort_order=1),
            Option("first_person", "First Person", "I/we perspective", "👁️", sort_order=2),
            Option("second_person", "Second Person", "You perspective", "🫵", sort_order=3),
            Option("third_person", "Third Person", "He/she/they perspective", "👤", sort_order=4),
            Option("omniscient", "Omniscient", "All-knowing narrator", "👁️👁️", sort_order=5),
            Option("epistolary", "Epistolary", "Letters/diary format", "💌", sort_order=6),
            Option("dialogue_heavy", "Dialogue Heavy", "Conversation-driven", "💬", sort_order=7),
            Option("descriptive", "Descriptive", "Rich sensory detail", "🎨", sort_order=8),
            Option("minimalist", "Minimalist", "Sparse and essential", "⚪", sort_order=9),
            Option("poetic", "Poetic/Lyrical", "Rhythmic prose", "🎵", sort_order=10),
            Option("humorous", "Humorous", "Funny tone", "😄", sort_order=11),
            Option("whimsical", "Whimsical", "Playful and fanciful", "🦄", sort_order=12),
            Option("dark", "Dark/Gritty", "Serious and edgy", "🌑", sort_order=13),
            Option("cozy", "Cozy", "Warm and comforting", "☕", sort_order=14),
            Option("educational", "Educational", "Teaching through story", "🎓", sort_order=15),
        ]
    )
    
    # ============================================================
    # STORY THEMES
    # ============================================================
    STORY_THEMES = OptionGroup(
        name="story_themes",
        label="Story Themes",
        description="Themes for children's story generation",
        icon="🌟",
        sort_order=26,
        options=[
            Option("theme_friendship", "Friendship", "Stories about friendship and kindness", "🤝", sort_order=1),
            Option("theme_kindness", "Kindness", "Kind actions and caring", "💖", sort_order=2),
            Option("theme_honesty", "Honesty", "Truth and integrity", "🧠", sort_order=3),
            Option("theme_courage", "Courage", "Bravery in challenges", "🛡️", sort_order=4),
            Option("theme_teamwork", "Teamwork", "Working together", "🤜🤛", sort_order=5),
            Option("theme_respect", "Respect", "Being kind and polite", "🙏", sort_order=6),
            Option("theme_sharing", "Sharing", "Giving and sharing", "🎁", sort_order=7),
            Option("theme_family", "Family", "Family bonds and love", "👨‍👩‍👧‍👦", sort_order=8),
            Option("theme_adventure", "Adventure", "Exciting journeys", "🗺️", sort_order=9),
            Option("theme_curiosity", "Curiosity", "Asking questions about the world", "🔎", sort_order=10),
            Option("theme_responsibility", "Responsibility", "Doing the right thing", "✅", sort_order=11),
            Option("theme_creativity", "Creativity", "Using imagination", "🎨", sort_order=12),
            Option("theme_patience", "Patience", "Waiting calmly", "⏳", sort_order=13),
            Option("theme_confidence", "Confidence", "Believing in yourself", "💪", sort_order=14),
            Option("theme_leadership", "Leadership", "Guiding others kindly", "👑", sort_order=15),
            Option("theme_hope", "Hope", "Looking forward to good things", "🌈", sort_order=16),
            Option("theme_love", "Love", "Caring without limits", "❤️", sort_order=17),
            Option("theme_forgiveness", "Forgiveness", "Letting go of hurt", "☮️", sort_order=18),
            Option("theme_nature", "Nature", "Animals, plants, and outdoors", "🌿", sort_order=19),
            Option("theme_imagination", "Imagination", "Dreaming up new worlds", "✨", sort_order=20),
            Option("theme_perseverance", "Perseverance", "Never giving up", "🏃", sort_order=21),
            Option("theme_gratitude", "Gratitude", "Being thankful", "🙏", sort_order=22),
            Option("theme_empathy", "Empathy", "Understanding others' feelings", "💞", sort_order=23),
            Option("theme_justice", "Justice", "Fairness and rightness", "⚖️", sort_order=24),
            Option("theme_peace", "Peace", "Calm and harmony", "🕊️", sort_order=25),
            Option("theme_wisdom", "Wisdom", "Learning important lessons", "🧠", sort_order=26),
            Option("theme_discovery", "Discovery", "Finding something new", "🔭", sort_order=27),
            Option("theme_dreams", "Dreams", "Imaginary hopes and sleep-time stories", "💭", sort_order=28),
            Option("theme_determination", "Determination", "Strong will to succeed", "🔥", sort_order=29),
            Option("theme_self_belief", "Self-Belief", "Trusting yourself", "🌟", sort_order=30),
            Option("theme_helping_others", "Helping Others", "Kind acts for others", "🤗", sort_order=31),
            Option("theme_good_manners", "Good Manners", "Polite behavior and etiquette", "🎩", sort_order=32),
            Option("theme_bravery", "Bravery", "Courage in the face of fear", "🦁", sort_order=33),
            Option("theme_cooperation", "Cooperation", "Working well together", "🤝", sort_order=34),
            Option("theme_learning", "Learning", "Growing through lessons", "📚", sort_order=35),
            Option("theme_happiness", "Happiness", "Joy and excitement", "😄", sort_order=36),
            Option("theme_faith", "Faith", "Belief and trust", "🌙", sort_order=37),
            Option("theme_compassion", "Compassion", "Caring with feeling", "🤲", sort_order=38),
            Option("theme_problem_solving", "Problem Solving", "Finding clever answers", "🧩", sort_order=39),
            Option("theme_never_give_up", "Never Give Up", "Persevering through hard times", "🏁", sort_order=40),
        ]
    )
    
    # ============================================================
    # STORY SETTINGS
    # ============================================================
    STORY_SETTINGS = OptionGroup(
        name="story_settings",
        label="Story Settings",
        description="Settings and locations for stories",
        icon="🏞️",
        sort_order=27,
        options=[
            Option("setting_forest", "Forest", "A lush forest with trees and animals", "🌳", sort_order=1),
            Option("setting_jungle", "Jungle", "A dense tropical jungle", "🌴", sort_order=2),
            Option("setting_village", "Village", "A cozy village community", "🏘️", sort_order=3),
            Option("setting_farm", "Farm", "Animals and fields on a farm", "🚜", sort_order=4),
            Option("setting_castle", "Castle", "A royal castle with towers", "🏰", sort_order=5),
            Option("setting_school", "School", "A school full of children", "🏫", sort_order=6),
            Option("setting_library", "Library", "Quiet books and learning", "📚", sort_order=7),
            Option("setting_playground", "Playground", "Fun outside play area", "🛝", sort_order=8),
            Option("setting_mountain", "Mountain", "High rocky peaks", "⛰️", sort_order=9),
            Option("setting_desert", "Desert", "Sandy hot landscapes", "🏜️", sort_order=10),
            Option("setting_beach", "Beach", "Sandy shore and waves", "🏖️", sort_order=11),
            Option("setting_underwater", "Underwater", "Ocean depths and sea life", "🌊", sort_order=12),
            Option("setting_space_station", "Space Station", "A station orbiting Earth", "🛰️", sort_order=13),
            Option("setting_moon", "Moon", "Lunar surface adventure", "🌕", sort_order=14),
            Option("setting_mars", "Mars", "Red planet exploration", "🔴", sort_order=15),
            Option("setting_magic_kingdom", "Magic Kingdom", "A kingdom full of magic", "🪄", sort_order=16),
            Option("setting_fairy_forest", "Fairy Forest", "Enchanted fairy woods", "🧚", sort_order=17),
            Option("setting_hidden_cave", "Hidden Cave", "A secret underground cavern", "🕳️", sort_order=18),
            Option("setting_ancient_temple", "Ancient Temple", "A mysterious old temple", "🏛️", sort_order=19),
            Option("setting_snow_village", "Snow Village", "A village covered in snow", "❄️", sort_order=20),
            Option("setting_island", "Island", "Island surrounded by sea", "🏝️", sort_order=21),
            Option("setting_pirate_ship", "Pirate Ship", "A ship of swashbucklers", "🏴‍☠️", sort_order=22),
            Option("setting_airship", "Airship", "A floating ship in the sky", "🎈", sort_order=23),
            Option("setting_train", "Train", "A journey by train", "🚂", sort_order=24),
            Option("setting_city", "City", "A bustling city scene", "🏙️", sort_order=25),
            Option("setting_zoo", "Zoo", "Animals in a zoo", "🦁", sort_order=26),
            Option("setting_aquarium", "Aquarium", "Underwater animal world", "🐠", sort_order=27),
            Option("setting_museum", "Museum", "Historical and scientific exhibits", "🏛️", sort_order=28),
            Option("setting_garden", "Garden", "Beautiful flower garden", "🌷", sort_order=29),
            Option("setting_tree_house", "Tree House", "A house in the trees", "🌲", sort_order=30),
            Option("setting_candy_land", "Candy Land", "A sweet candy world", "🍬", sort_order=31),
            Option("setting_toy_world", "Toy World", "A world of toys", "🧸", sort_order=32),
            Option("setting_dinosaur_valley", "Dinosaur Valley", "Land of dinosaurs", "🦕", sort_order=33),
            Option("setting_volcano", "Volcano", "Volcanic adventure", "🌋", sort_order=34),
            Option("setting_cloud_kingdom", "Cloud Kingdom", "Floating cloud world", "☁️", sort_order=35),
            Option("setting_ice_castle", "Ice Castle", "A glittering castle of ice", "🏰", sort_order=36),
            Option("setting_rainbow_bridge", "Rainbow Bridge", "Colorful bridge over clouds", "🌈", sort_order=37),
            Option("setting_secret_laboratory", "Secret Laboratory", "A hidden science lab", "🔬", sort_order=38),
            Option("setting_robot_city", "Robot City", "A city of robots", "🤖", sort_order=39),
            Option("setting_time_machine", "Time Machine", "A machine that travels through time", "⏳", sort_order=40),
        ]
    )
    
    # ============================================================
    # ENDING STYLES
    # ============================================================
    ENDING_STYLES = OptionGroup(
        name="ending_styles",
        label="Ending Styles",
        description="Different types of story endings",
        icon="🏁",
        sort_order=28,
        options=[
            Option("ending_happy", "Happy Ending", "Positive resolution", "😊", sort_order=1),
            Option("ending_emotional", "Emotional Ending", "Heartfelt conclusion", "😢", sort_order=2),
            Option("ending_funny", "Funny Ending", "Humorous twist", "😂", sort_order=3),
            Option("ending_surprise", "Surprise Ending", "Unexpected finish", "🎉", sort_order=4),
            Option("ending_open", "Open Ending", "Leaves room for imagination", "❓", sort_order=5),
            Option("ending_inspirational", "Inspirational Ending", "Motivational conclusion", "🌟", sort_order=6),
        ]
    )
    
    # ============================================================
    # CONFLICT TYPES
    # ============================================================
    CONFLICT_TYPES = OptionGroup(
        name="conflict_types",
        label="Conflict Types",
        description="Story problems to drive the plot",
        icon="⚔️",
        sort_order=29,
        options=[
            Option("conflict_lost_item", "Lost Item", "A missing treasure or toy", "🧸", sort_order=1),
            Option("conflict_friendship_problem", "Friendship Problem", "Friends disagree or quarrel", "🤔", sort_order=2),
            Option("conflict_big_challenge", "Big Challenge", "A difficult task to overcome", "🏔️", sort_order=3),
            Option("conflict_mystery", "Mystery", "Something mysterious must be solved", "🔍", sort_order=4),
            Option("conflict_competition", "Competition", "A contest or race", "🏁", sort_order=5),
            Option("conflict_rescue_mission", "Rescue Mission", "Saving someone or something", "🚑", sort_order=6),
            Option("conflict_natural_disaster", "Natural Disaster", "Storm or earthquake challenge", "🌪️", sort_order=7),
            Option("conflict_magic_curse", "Magic Curse", "A spell causes trouble", "🪄", sort_order=8),
            Option("conflict_wrong_decision", "Wrong Decision", "A mistake must be fixed", "❌", sort_order=9),
            Option("conflict_family_problem", "Family Problem", "Home relationships are strained", "🏠", sort_order=10),
            Option("conflict_fear", "Fear", "A character is afraid of something", "😨", sort_order=11),
            Option("conflict_teamwork_challenge", "Teamwork Challenge", "Group must cooperate better", "🤝", sort_order=12),
        ]
    )
    
    # ============================================================
    # REWARDS
    # ============================================================
    REWARDS = OptionGroup(
        name="rewards",
        label="Rewards",
        description="Rewards received in story outcomes",
        icon="🏆",
        sort_order=30,
        options=[
            Option("reward_treasure", "Treasure", "A chest of treasure", "💰", sort_order=1),
            Option("reward_medal", "Medal", "A medal for bravery", "🥇", sort_order=2),
            Option("reward_friendship", "Friendship", "New friends and bonds", "🤝", sort_order=3),
            Option("reward_wisdom", "Wisdom", "Important lessons learned", "🧠", sort_order=4),
            Option("reward_magic_crystal", "Magic Crystal", "A special glowing gem", "🔮", sort_order=5),
            Option("reward_golden_key", "Golden Key", "A key to unlock new doors", "🗝️", sort_order=6),
            Option("reward_crown", "Crown", "Royal recognition", "👑", sort_order=7),
            Option("reward_new_home", "New Home", "A safe place to live", "🏡", sort_order=8),
            Option("reward_knowledge", "Knowledge", "Understanding and learning", "📘", sort_order=9),
            Option("reward_peace", "Peace", "Calm and harmony", "🕊️", sort_order=10),
        ]
    )
    
    # ============================================================
    # PROBLEMS
    # ============================================================
    PROBLEMS = OptionGroup(
        name="problems",
        label="Problems",
        description="Child-friendly story problems to solve",
        icon="🧩",
        sort_order=31,
        options=[
            Option("problem_lost_toy", "Lost Toy", "A beloved toy has disappeared", "🧸", sort_order=1),
            Option("problem_broken_friendship", "Broken Friendship", "Friends are upset with each other", "💔", sort_order=2),
            Option("problem_missing_pet", "Missing Pet", "A pet has wandered away", "🐶", sort_order=3),
            Option("problem_scary_shadow", "Scary Shadow", "A strange shadow frightens characters", "👻", sort_order=4),
            Option("problem_rainy_day", "Rainy Day", "Plans disrupted by rain", "🌧️", sort_order=5),
            Option("problem_hungry_animal", "Hungry Animal", "An animal needs food", "🐾", sort_order=6),
            Option("problem_tangled_kite", "Tangled Kite", "A kite gets stuck in a tree", "🪁", sort_order=7),
            Option("problem_flat_tire", "Flat Tire", "A vehicle breaks down", "🚲", sort_order=8),
            Option("problem_lost_map", "Lost Map", "A map has gone missing", "🗺️", sort_order=9),
            Option("problem_sleepy_hero", "Sleepy Hero", "A character is too tired for adventure", "😴", sort_order=10),
            Option("problem_dark_forest", "Dark Forest", "A path is blocked by darkness", "🌲", sort_order=11),
            Option("problem_spilled_paint", "Spilled Paint", "A mess needs cleaning up", "🎨", sort_order=12),
            Option("problem_broken_bridge", "Broken Bridge", "A bridge no longer works", "🌉", sort_order=13),
            Option("problem_mysterious_noise", "Mysterious Noise", "A strange sound must be investigated", "🔊", sort_order=14),
            Option("problem_lost_key", "Lost Key", "A key is lost before a big event", "🗝️", sort_order=15),
            Option("problem_forgotten_birthday", "Forgotten Birthday", "A special day is overlooked", "🎂", sort_order=16),
            Option("problem_closed_library", "Closed Library", "Books are inaccessible", "📚", sort_order=17),
            Option("problem_noisy_classroom", "Noisy Classroom", "Too much distraction during learning", "📣", sort_order=18),
            Option("problem_lost_recipe", "Lost Recipe", "A recipe is missing for cooking", "🍪", sort_order=19),
            Option("problem_lost_treasure", "Lost Treasure", "Treasure has vanished", "🪙", sort_order=20),
            Option("problem_missing_puzzle_piece", "Missing Puzzle Piece", "A puzzle cannot be finished", "🧩", sort_order=21),
            Option("problem_windy_day", "Windy Day", "Strong winds create trouble", "🌬️", sort_order=22),
            Option("problem_sad_robot", "Sad Robot", "A robot needs cheering up", "🤖", sort_order=23),
            Option("problem_hidden_garden", "Hidden Garden", "A secret garden is hard to find", "🌸", sort_order=24),
            Option("problem_empty_basket", "Empty Basket", "There is nothing to share", "🧺", sort_order=25),
            Option("problem_lonely_tree", "Lonely Tree", "A tree needs company", "🌳", sort_order=26),
            Option("problem_tiny_dragon", "Tiny Dragon", "A dragon needs a friend", "🐉", sort_order=27),
            Option("problem_confused_cat", "Confused Cat", "A cat cannot find home", "🐱", sort_order=28),
            Option("problem_dry_garden", "Dry Garden", "Plants need water", "💧", sort_order=29),
            Option("problem_no_power", "No Power", "Lights go out unexpectedly", "💡", sort_order=30),
        ]
    )
    
    # ============================================================
    # SOLUTIONS
    # ============================================================
    SOLUTIONS = OptionGroup(
        name="solutions",
        label="Solutions",
        description="Positive solutions for story problems",
        icon="🛠️",
        sort_order=32,
        options=[
            Option("solution_find_friend", "Find a Friend", "Reach out and make a new friend", "🤝", sort_order=1),
            Option("solution_tell_truth", "Tell the Truth", "Be honest about the situation", "🗣️", sort_order=2),
            Option("solution_help_others", "Help Others", "Lend a hand to someone in need", "🧡", sort_order=3),
            Option("solution_share", "Share", "Give part of what you have", "🎁", sort_order=4),
            Option("solution_learn", "Learn Something New", "Grow through knowledge", "📚", sort_order=5),
            Option("solution_be_brave", "Be Brave", "Face fear with courage", "🦁", sort_order=6),
            Option("solution_work_together", "Work Together", "Solve problems as a team", "🤜🤛", sort_order=7),
            Option("solution_use_kindness", "Use Kindness", "Be gentle and thoughtful", "💛", sort_order=8),
            Option("solution_find_clue", "Find a Clue", "Look for useful evidence", "🔎", sort_order=9),
            Option("solution_fix_mistake", "Fix a Mistake", "Make things right again", "🛠️", sort_order=10),
            Option("solution_pray", "Pray", "Ask for help with faith", "🕊️", sort_order=11),
            Option("solution_plan", "Make a Plan", "Think ahead before acting", "📝", sort_order=12),
            Option("solution_apologize", "Apologize", "Say sorry and heal hurt feelings", "🙏", sort_order=13),
            Option("solution_take_turns", "Take Turns", "Give others a chance too", "🔁", sort_order=14),
            Option("solution_ask_for_help", "Ask for Help", "Reach out to someone wiser", "📞", sort_order=15),
            Option("solution_close_the_gap", "Close the Gap", "Solve what is missing", "🧩", sort_order=16),
            Option("solution_water_plants", "Water the Plants", "Care for the garden", "💧", sort_order=17),
            Option("solution_find_home", "Find a Home", "Help someone settle safely", "🏡", sort_order=18),
            Option("solution_make_art", "Make Art", "Express feelings creatively", "🎨", sort_order=19),
            Option("solution_write_letter", "Write a Letter", "Share feelings on paper", "✉️", sort_order=20),
            Option("solution_give_peace", "Give Peace", "Bring calm and resolution", "☮️", sort_order=21),
            Option("solution_smile", "Smile", "Use a friendly gesture to help", "😊", sort_order=22),
            Option("solution_listen", "Listen", "Hear what others are saying", "👂", sort_order=23),
            Option("solution_be_patient", "Be Patient", "Wait calmly for a solution", "⏳", sort_order=24),
            Option("solution_share_ideas", "Share Ideas", "Brainstorm together", "💡", sort_order=25),
            Option("solution_take_care", "Take Care", "Look after people or things", "🩹", sort_order=26),
            Option("solution_believe", "Believe in Yourself", "Trust your own strength", "🌟", sort_order=27),
            Option("solution_give_hug", "Give a Hug", "Show support and comfort", "🤗", sort_order=28),
            Option("solution_play_nicely", "Play Nicely", "Cooperate during play", "🧸", sort_order=29),
            Option("solution_pick_up", "Pick Up", "Clean up and organize", "🧹", sort_order=30),
        ]
    )
    
    # ============================================================
    # MAGICAL ELEMENTS
    # ============================================================
    MAGICAL_ELEMENTS = OptionGroup(
        name="magical_elements",
        label="Magical Elements",
        description="Magical objects and creatures for stories",
        icon="🪄",
        sort_order=33,
        options=[
            Option("magic_wand", "Magic Wand", "A wand that casts spells", "🪄", sort_order=1),
            Option("flying_carpet", "Flying Carpet", "A carpet that flies through the sky", "🪁", sort_order=2),
            Option("magic_book", "Magic Book", "A book filled with spells", "📜", sort_order=3),
            Option("dragon_egg", "Dragon Egg", "A rare egg ready to hatch", "🐉", sort_order=4),
            Option("fairy_dust", "Fairy Dust", "Sparkling dust with magic power", "✨", sort_order=5),
            Option("crystal_ball", "Crystal Ball", "A ball that shows the future", "🔮", sort_order=6),
            Option("talking_tree", "Talking Tree", "A tree that speaks", "🌳", sort_order=7),
            Option("magic_ring", "Magic Ring", "A ring with enchanted power", "💍", sort_order=8),
            Option("time_portal", "Time Portal", "A door through time", "🌀", sort_order=9),
            Option("enchanted_forest", "Enchanted Forest", "A forest full of magic", "🍄", sort_order=10),
            Option("invisible_cloak", "Invisible Cloak", "A cloak that makes you unseen", "🧥", sort_order=11),
            Option("phoenix_feather", "Phoenix Feather", "A feather of rebirth", "🪶", sort_order=12),
            Option("unicorn_horn", "Unicorn Horn", "A horn of magical healing", "🦄", sort_order=13),
            Option("rainbow_stone", "Rainbow Stone", "A stone of colorful power", "🌈", sort_order=14),
            Option("moon_crystal", "Moon Crystal", "A bright moonlit gem", "🌙", sort_order=15),
            Option("magic_key", "Magic Key", "A key to unlock secrets", "🗝️", sort_order=16),
            Option("wish_star", "Wish Star", "A star that grants wishes", "⭐", sort_order=17),
            Option("spell_scroll", "Spell Scroll", "A scroll containing spells", "📜", sort_order=18),
            Option("floating_castle", "Floating Castle", "A castle that floats in the sky", "🏰", sort_order=19),
            Option("dream_potion", "Dream Potion", "A potion that creates dreams", "🧪", sort_order=20),
            Option("magic_lantern", "Magic Lantern", "A lantern filled with light magic", "🏮", sort_order=21),
            Option("guardian_sprite", "Guardian Sprite", "A tiny protective spirit", "🧚‍♂️", sort_order=22),
            Option("mystic_scroll", "Mystic Scroll", "Ancient magical text", "📜", sort_order=23),
            Option("silver_arrow", "Silver Arrow", "A magical arrow that never misses", "🏹", sort_order=24),
            Option("star_compass", "Star Compass", "A compass guided by stars", "🧭", sort_order=25),
            Option("potion_of_courage", "Potion of Courage", "Makes characters brave", "🥤", sort_order=26),
            Option("sleepsong_flute", "Sleepsong Flute", "A flute that soothes", "🎶", sort_order=27),
            Option("spell_gem", "Spell Gem", "A gem filled with spells", "💎", sort_order=28),
            Option("mystic_mirror", "Mystic Mirror", "Reflects hidden truth", "🪞", sort_order=29),
            Option("enchanted_map", "Enchanted Map", "A map that guides adventurers", "🗺️", sort_order=30),
            Option("moonlight_blade", "Moonlight Blade", "A blade powered by moonlight", "🗡️", sort_order=31),
            Option("whispering_shell", "Whispering Shell", "A shell that speaks secrets", "🐚", sort_order=32),
            Option("sunflower_scepter", "Sunflower Scepter", "A scepter that brings sunshine", "🌻", sort_order=33),
            Option("crystal_wings", "Crystal Wings", "Wings of sparkling crystals", "🪽", sort_order=34),
            Option("storm_charm", "Storm Charm", "A charm to call gentle storms", "⛈️", sort_order=35),
            Option("mystic_pendant", "Mystic Pendant", "A pendant with protective magic", "📿", sort_order=36),
            Option("luminous_staff", "Luminous Staff", "A staff that glows in the dark", "✨", sort_order=37),
            Option("galaxy_orb", "Galaxy Orb", "An orb of cosmic energy", "🌌", sort_order=38),
            Option("whimsy_wand", "Whimsy Wand", "A playful spellmaker", "🪄", sort_order=39),
        ]
    )
    
    # ============================================================
    # ISLAMIC VALUES
    # ============================================================
    ISLAMIC_VALUES = OptionGroup(
        name="islamic_values",
        label="Islamic Values",
        description="Values and virtues for Islamic stories",
        icon="🕌",
        sort_order=34,
        options=[
            Option("islamic_honesty", "Honesty", "Being truthful and sincere", "🧡", sort_order=1),
            Option("islamic_patience", "Patience", "Waiting calmly with faith", "⏳", sort_order=2),
            Option("islamic_respect", "Respect", "Treating others kindly", "🙏", sort_order=3),
            Option("islamic_kindness", "Kindness", "Helping others with compassion", "🤲", sort_order=4),
            Option("islamic_charity", "Charity", "Giving to those in need", "🤝", sort_order=5),
            Option("islamic_gratitude", "Gratitude", "Thankfulness to Allah", "🕌", sort_order=6),
            Option("islamic_trust_in_allah", "Trust in Allah", "Belief in Allah's plan", "🌙", sort_order=7),
            Option("islamic_forgiveness", "Forgiveness", "Forgiving others kindly", "🕊️", sort_order=8),
            Option("islamic_good_manners", "Good Manners", "Polite and respectful behavior", "🤝", sort_order=9),
            Option("islamic_mercy", "Mercy", "Showing compassion and care", "💛", sort_order=10),
            Option("islamic_justice", "Justice", "Fairness for everyone", "⚖️", sort_order=11),
            Option("islamic_helping_parents", "Helping Parents", "Serving and respecting parents", "👪", sort_order=12),
            Option("islamic_keeping_promises", "Keeping Promises", "Being trustworthy", "✍️", sort_order=13),
            Option("islamic_humility", "Humility", "Being modest and humble", "🙏", sort_order=14),
            Option("islamic_truthfulness", "Truthfulness", "Speaking the truth always", "🗣️", sort_order=15),
            Option("islamic_generosity", "Generosity", "Sharing with others", "🎁", sort_order=16),
            Option("islamic_compassion", "Compassion", "Caring for others' feelings", "🤍", sort_order=17),
            Option("islamic_cleanliness", "Cleanliness", "Keeping body and space pure", "🧼", sort_order=18),
            Option("islamic_sincerity", "Sincerity", "Intentions from the heart", "🧡", sort_order=19),
            Option("islamic_brotherhood", "Brotherhood", "Community love", "🤝", sort_order=20),
        ]
    )
    
    # ============================================================
    # DUAS
    # ============================================================
    DUAS = OptionGroup(
        name="duas",
        label="Duas",
        description="Short child-friendly duas for stories",
        icon="🕌",
        sort_order=35,
        options=[
            Option("dua_subhan_allah", "SubhanAllah", "Praise Allah's perfection", "✨", sort_order=1),
            Option("dua_alhamdulillah", "Alhamdulillah", "Thank Allah for blessings", "🙏", sort_order=2),
            Option("dua_allahu_akbar", "Allahu Akbar", "Allah is the greatest", "🌙", sort_order=3),
            Option("dua_bismillah", "Bismillah", "In the name of Allah", "📿", sort_order=4),
            Option("dua_insha_allah", "InshaAllah", "If Allah wills it", "🤲", sort_order=5),
            Option("dua_astaghfirullah", "Astaghfirullah", "Ask forgiveness from Allah", "😔", sort_order=6),
            Option("dua_rabbana_atina", "Rabbana Atina", "Ask for good things", "🌟", sort_order=7),
            Option("dua_ya_allah", "Ya Allah", "Call out to Allah for help", "🙏", sort_order=8),
            Option("dua_shukr", "Shukr", "Thankfulness and gratitude", "🌼", sort_order=9),
            Option("dua_sabr", "Sabr", "Ask for patience", "⏳", sort_order=10),
            Option("dua_amni", "Safe Journey", "Pray for safe travel", "🛤️", sort_order=11),
            Option("dua_good_sleep", "Good Sleep", "Pray for peaceful rest", "😴", sort_order=12),
            Option("dua_good_health", "Good Health", "Pray for health and wellness", "💪", sort_order=13),
            Option("dua_good_food", "Thankful for Food", "Pray before eating", "🍽️", sort_order=14),
            Option("dua_family", "Family Blessings", "Pray for family happiness", "👨‍👩‍👧‍👦", sort_order=15),
            Option("dua_friends", "Friendship Blessings", "Pray for friends' well-being", "🤝", sort_order=16),
            Option("dua_help_others", "Help Others", "Pray for ability to help others", "🤲", sort_order=17),
            Option("dua_be_kind", "Be Kind", "Pray for kind heart", "💛", sort_order=18),
            Option("dua_be_grateful", "Be Grateful", "Pray to stay thankful", "🙏", sort_order=19),
            Option("dua_love", "Love and Caring", "Pray for love in your heart", "❤️", sort_order=20),
        ]
    )
    
    # ============================================================
    # SPACE VEHICLES
    # ============================================================
    SPACE_VEHICLES = OptionGroup(
        name="space_vehicles",
        label="Space Vehicles",
        description="Vehicles for space adventure stories",
        icon="🚀",
        sort_order=36,
        options=[
            Option("space_vehicle_rocket", "Rocket", "A rocket that flies to space", "🚀", sort_order=1),
            Option("space_vehicle_space_shuttle", "Space Shuttle", "A reusable spaceplane", "🛩️", sort_order=2),
            Option("space_vehicle_lunar_lander", "Lunar Lander", "A craft for moon landings", "🌕", sort_order=3),
            Option("space_vehicle_space_capsule", "Space Capsule", "A small crewed capsule", "🛰️", sort_order=4),
            Option("space_vehicle_explorer_ship", "Explorer Ship", "A ship for deep space", "🚀", sort_order=5),
            Option("space_vehicle_research_craft", "Research Craft", "A science mission vessel", "🔬", sort_order=6),
            Option("space_vehicle_mars_rover", "Mars Rover", "A rover exploring Mars", "🛻", sort_order=7),
            Option("space_vehicle_star_cruiser", "Star Cruiser", "A fast interstellar ship", "🌌", sort_order=8),
            Option("space_vehicle_orbiter", "Orbiter", "A craft that circles a planet", "🛰️", sort_order=9),
            Option("space_vehicle_rescue_ship", "Rescue Ship", "A ship that rescues astronauts", "🚑", sort_order=10),
            Option("space_vehicle_landing_module", "Landing Module", "A surface lander", "🛬", sort_order=11),
            Option("space_vehicle_astro_tug", "Astro Tug", "A small support craft", "🛠️", sort_order=12),
            Option("space_vehicle_star_freighter", "Star Freighter", "Carrier of cargo in space", "📦", sort_order=13),
            Option("space_vehicle_moon_buggy", "Moon Buggy", "Surface rover for the moon", "🚙", sort_order=14),
            Option("space_vehicle_alien_cruiser", "Alien Cruiser", "A mysterious alien ship", "👽", sort_order=15),
            Option("space_vehicle_warp_ship", "Warp Ship", "Faster-than-light vessel", "✨", sort_order=16),
            Option("space_vehicle_galaxy_sailer", "Galaxy Sailer", "A graceful cosmic ship", "⛵", sort_order=17),
            Option("space_vehicle_asteroid_miner", "Asteroid Miner", "Ship that mines asteroids", "⛏️", sort_order=18),
            Option("space_vehicle_lunar_taxi", "Lunar Taxi", "Moon transport service", "🚕", sort_order=19),
            Option("space_vehicle_rocket_boat", "Rocket Boat", "A hybrid space/sea vehicle", "🚤", sort_order=20),
        ]
    )
    
    # ============================================================
    # MISSIONS
    # ============================================================
    MISSIONS = OptionGroup(
        name="missions",
        label="Missions",
        description="Mission objectives for stories",
        icon="🎯",
        sort_order=37,
        options=[
            Option("mission_rescue", "Rescue", "Save someone or something", "🚑", sort_order=1),
            Option("mission_exploration", "Exploration", "Discover new places", "🧭", sort_order=2),
            Option("mission_discovery", "Discovery", "Find something amazing", "🔎", sort_order=3),
            Option("mission_research", "Research", "Study and learn from the world", "🔬", sort_order=4),
            Option("mission_save_planet", "Save the Planet", "Protect the Earth", "🌍", sort_order=5),
            Option("mission_find_treasure", "Find Treasure", "Search for hidden treasure", "🏴‍☠️", sort_order=6),
            Option("mission_deliver_message", "Deliver Message", "Carry an important message", "✉️", sort_order=7),
            Option("mission_meet_aliens", "Meet Aliens", "Make contact with extraterrestrials", "👽", sort_order=8),
            Option("mission_collect_samples", "Collect Samples", "Gather things to study", "🧪", sort_order=9),
            Option("mission_build_colony", "Build Colony", "Create a new home", "🏠", sort_order=10),
            Option("mission_protect_friends", "Protect Friends", "Keep loved ones safe", "🛡️", sort_order=11),
            Option("mission_restore_balance", "Restore Balance", "Fix an upset situation", "⚖️", sort_order=12),
            Option("mission_save_animals", "Save Animals", "Help animals in danger", "🐾", sort_order=13),
            Option("mission_find_legend", "Find a Legend", "Uncover a famous story object", "📜", sort_order=14),
            Option("mission_repair", "Repair", "Fix broken things", "🔧", sort_order=15),
            Option("mission_teach", "Teach", "Share knowledge with others", "📘", sort_order=16),
            Option("mission_protect_nature", "Protect Nature", "Care for the environment", "🍃", sort_order=17),
            Option("mission_escape", "Escape", "Help someone get away safely", "🏃", sort_order=18),
            Option("mission_find_home", "Find Home", "Find a safe place to live", "🏡", sort_order=19),
            Option("mission_make_peace", "Make Peace", "Resolve a disagreement", "🕊️", sort_order=20),
            Option("mission_surprise_party", "Surprise Party", "Prepare a special celebration", "🎉", sort_order=21),
            Option("mission_solve_riddle", "Solve Riddle", "Figure out a clever puzzle", "🧠", sort_order=22),
            Option("mission_open_book", "Open Book", "Unlock knowledge through reading", "📖", sort_order=23),
            Option("mission_find_star", "Find Star", "Locate a shining star", "⭐", sort_order=24),
            Option("mission_save_rainforest", "Save Rainforest", "Protect jungle habitat", "🌿", sort_order=25),
            Option("mission_restore_river", "Restore River", "Clean a waterway", "🌊", sort_order=26),
            Option("mission_build_bridge", "Build Bridge", "Connect two places", "🌉", sort_order=27),
            Option("mission_create_garden", "Create Garden", "Grow a beautiful garden", "🌷", sort_order=28),
            Option("mission_train_dragon", "Train Dragon", "Teach a dragon new skills", "🐉", sort_order=29),
            Option("mission_invite_friends", "Invite Friends", "Bring everyone together", "🎊", sort_order=30),
        ]
    )
    
    # ============================================================
    # FUNNY SITUATIONS
    # ============================================================
    FUNNY_SITUATIONS = OptionGroup(
        name="funny_situations",
        label="Funny Situations",
        description="Silly situations for lighthearted stories",
        icon="😂",
        sort_order=38,
        options=[
            Option("funny_banana_peel", "Banana Peel", "Slipping on a banana peel", "🍌", sort_order=1),
            Option("funny_talking_chicken", "Talking Chicken", "A chicken that speaks", "🐔", sort_order=2),
            Option("funny_dancing_elephant", "Dancing Elephant", "An elephant that dances", "🕺", sort_order=3),
            Option("funny_invisible_hat", "Invisible Hat", "A hat everyone can’t see", "🎩", sort_order=4),
            Option("funny_wrong_shoes", "Wrong Shoes", "Wearing mismatched shoes", "🥾", sort_order=5),
            Option("funny_flying_cake", "Flying Cake", "A cake takes flight", "🎂", sort_order=6),
            Option("funny_laughing_robot", "Laughing Robot", "A robot that giggles", "🤖", sort_order=7),
            Option("funny_giant_bubble", "Giant Bubble", "A huge floating bubble", "🫧", sort_order=8),
            Option("funny_backwards_day", "Backwards Day", "Everything is reversed", "🔄", sort_order=9),
            Option("funny_silly_race", "Silly Race", "A funny race with odd rules", "🏃", sort_order=10),
            Option("funny_sneezing_dragon", "Sneezing Dragon", "A dragon sneezes fire", "🐉", sort_order=11),
            Option("funny_giggling_tree", "Giggling Tree", "A tree that laughs", "🌳", sort_order=12),
            Option("funny_spinning_pizza", "Spinning Pizza", "A pizza that spins by itself", "🍕", sort_order=13),
            Option("funny_bouncing_ball", "Bouncing Ball", "A ball that hops everywhere", "🏀", sort_order=14),
            Option("funny_magic_puddle", "Magic Puddle", "A puddle with surprises", "💧", sort_order=15),
            Option("funny_pajama_parade", "Pajama Parade", "Kids march in pajamas", "🛌", sort_order=16),
            Option("funny_sleeping_bear", "Sleeping Bear", "A bear snores loudly", "🐻", sort_order=17),
            Option("funny_fluffy_cloud", "Fluffy Cloud", "A cloud with a face", "☁️", sort_order=18),
            Option("funny_opposite_socks", "Opposite Socks", "Socks are on the wrong feet", "🧦", sort_order=19),
            Option("funny_juggling_cat", "Juggling Cat", "A cat juggling toys", "🐱", sort_order=20),
            Option("funny_sparkling_toothpaste", "Sparkling Toothpaste", "Magic toothpaste sparkles", "🪥", sort_order=21),
            Option("funny_bubble_hat", "Bubble Hat", "A hat made of bubbles", "🫧", sort_order=22),
            Option("funny_march_of_penguins", "March of Penguins", "Penguins march in a line", "🐧", sort_order=23),
            Option("funny_bouncing_cookie", "Bouncing Cookie", "A cookie that leaps", "🍪", sort_order=24),
            Option("funny_superhero_snail", "Superhero Snail", "A snail with a cape", "🐌", sort_order=25),
            Option("funny_giggle_bubbles", "Giggle Bubbles", "Bubbles that make everyone laugh", "🫧", sort_order=26),
            Option("funny_sleepwalking_unicorn", "Sleepwalking Unicorn", "A unicorn walking in its sleep", "🦄", sort_order=27),
            Option("funny_pirate_parrot", "Pirate Parrot", "A parrot with a pirate hat", "🦜", sort_order=28),
            Option("funny_underwear_rain", "Underwear Rain", "Underwear falls from the sky", "🩲", sort_order=29),
            Option("funny_muddy_paint", "Muddy Paint", "Paint turns into mud", "🎨", sort_order=30),
            Option("funny_spinning_slide", "Spinning Slide", "A slide spins around the playground", "🛝", sort_order=31),
            Option("funny_chirping_clock", "Chirping Clock", "A clock that sings", "🕰️", sort_order=32),
            Option("funny_adorable_robot", "Adorable Robot", "A robot that acts silly", "🤖", sort_order=33),
            Option("funny_tiny_giant", "Tiny Giant", "A giant who is very small", "🧍", sort_order=34),
            Option("funny_treasure_hat", "Treasure Hat", "A hat filled with treasure", "🎩", sort_order=35),
            Option("funny_napping_owl", "Napping Owl", "An owl nodding off", "🦉", sort_order=36),
            Option("funny_cupcake_cloud", "Cupcake Cloud", "A cloud shaped like a cupcake", "🧁", sort_order=37),
            Option("funny_silly_spoon", "Silly Spoon", "A spoon that dances", "🥄", sort_order=38),
            Option("funny_marching_pencils", "Marching Pencils", "Pencils marching in a row", "✏️", sort_order=39),
            Option("funny_lucky_purse", "Lucky Purse", "A purse that giggles when opened", "👜", sort_order=40),
        ]
    )
    
    # ============================================================
    # MYSTERIES
    # ============================================================
    MYSTERIES = OptionGroup(
        name="mysteries",
        label="Mysteries",
        description="Mysteries and puzzles for stories",
        icon="🕵️",
        sort_order=39,
        options=[
            Option("mystery_missing_key", "Missing Key", "A key has disappeared", "🗝️", sort_order=1),
            Option("mystery_hidden_treasure", "Hidden Treasure", "Treasure hidden away", "💰", sort_order=2),
            Option("mystery_secret_door", "Secret Door", "A door hides a mystery", "🚪", sort_order=3),
            Option("mystery_lost_map", "Lost Map", "A map is missing", "🗺️", sort_order=4),
            Option("mystery_strange_footprints", "Strange Footprints", "Unusual prints appear", "👣", sort_order=5),
            Option("mystery_ghost_light", "Ghost Light", "A mysterious glowing light", "👻", sort_order=6),
            Option("mystery_missing_toy", "Missing Toy", "A toy vanishes unexpectedly", "🧸", sort_order=7),
            Option("mystery_magic_necklace", "Magic Necklace", "A necklace with secrets", "📿", sort_order=8),
            Option("mystery_secret_letter", "Secret Letter", "A hidden message arrives", "✉️", sort_order=9),
            Option("mystery_hidden_cave", "Hidden Cave", "A cave hides a secret", "🕳️", sort_order=10),
            Option("mystery_lost_song", "Lost Song", "A song is forgotten", "🎵", sort_order=11),
            Option("mystery_golden_shadow", "Golden Shadow", "A shadow that glows golden", "🌟", sort_order=12),
            Option("mystery_disappearing_path", "Disappearing Path", "A path vanishes suddenly", "🛣️", sort_order=13),
            Option("mystery_talking_statue", "Talking Statue", "A statue that speaks", "🗿", sort_order=14),
            Option("mystery_missing_star", "Missing Star", "A star goes missing in the sky", "⭐", sort_order=15),
            Option("mystery_silent_forest", "Silent Forest", "A forest falls quiet", "🌲", sort_order=16),
            Option("mystery_mirror_maze", "Mirror Maze", "A maze of reflections", "🪞", sort_order=17),
            Option("mystery_whispering_wind", "Whispering Wind", "Wind that whispers secrets", "🌬️", sort_order=18),
            Option("mystery_hidden_note", "Hidden Note", "A note tucked away", "📝", sort_order=19),
            Option("mystery_disappearing_rainbow", "Disappearing Rainbow", "A rainbow fades away", "🌈", sort_order=20),
            Option("mystery_unread_book", "Unread Book", "A book with missing pages", "📖", sort_order=21),
            Option("mystery_silver_bell", "Silver Bell", "A bell with a secret sound", "🔔", sort_order=22),
            Option("mystery_tiny_giant", "Tiny Giant", "A giant with a secret", "🧍", sort_order=23),
            Option("mystery_stolen_crown", "Stolen Crown", "A crown is taken", "👑", sort_order=24),
            Option("mystery_moon_riddle", "Moon Riddle", "A riddle from the moon", "🌕", sort_order=25),
            Option("mystery_feather_clue", "Feather Clue", "A feather that points the way", "🪶", sort_order=26),
            Option("mystery_glowing_potion", "Glowing Potion", "A potion with a secret glow", "🧪", sort_order=27),
            Option("mystery_time_capsule", "Time Capsule", "A message from the past", "⌛", sort_order=28),
            Option("mystery_starlit_door", "Starlit Door", "A door lit by stars", "🚪", sort_order=29),
            Option("mystery_whispering_book", "Whispering Book", "A book that whispers", "📚", sort_order=30),
            Option("mystery_hidden_picture", "Hidden Picture", "A picture with a secret image", "🖼️", sort_order=31),
            Option("mystery_singing_fish", "Singing Fish", "A fish that sings clues", "🐟", sort_order=32),
            Option("mystery_magic_clock", "Magic Clock", "A clock with time secrets", "🕰️", sort_order=33),
            Option("mystery_icy_crown", "Icy Crown", "A crown frozen in ice", "❄️", sort_order=34),
            Option("mystery_dusty_attic", "Dusty Attic", "A quiet old attic", "🏚️", sort_order=35),
            Option("mystery_riddle_river", "Riddle River", "A river that asks questions", "🌊", sort_order=36),
            Option("mystery_starlight_key", "Starlight Key", "A key shining with starlight", "🔑", sort_order=37),
            Option("mystery_cloud_castle", "Cloud Castle", "A castle hidden in clouds", "☁️", sort_order=38),
        ]
    )
    
    # ============================================================
    # CLUES
    # ============================================================
    CLUES = OptionGroup(
        name="clues",
        label="Clues",
        description="Clues to help solve story mysteries",
        icon="🕵️",
        sort_order=40,
        options=[
            Option("clue_footprints", "Footprints", "Tracks left by someone", "👣", sort_order=1),
            Option("clue_feather", "Feather", "A soft feather left behind", "🪶", sort_order=2),
            Option("clue_broken_key", "Broken Key", "A key with a broken edge", "🗝️", sort_order=3),
            Option("clue_map_piece", "Map Piece", "A piece of a missing map", "🗺️", sort_order=4),
            Option("clue_old_book", "Old Book", "A dusty ancient book", "📚", sort_order=5),
            Option("clue_strange_sound", "Strange Sound", "An odd sound that hints the mystery", "🔊", sort_order=6),
            Option("clue_fingerprints", "Fingerprints", "Marks left by fingers", "👆", sort_order=7),
            Option("clue_crystal", "Crystal", "A sparkling crystal clue", "🔮", sort_order=8),
            Option("clue_secret_code", "Secret Code", "A hidden code to decode", "🔐", sort_order=9),
            Option("clue_compass", "Compass", "A compass pointing the way", "🧭", sort_order=10),
            Option("clue_mysterious_note", "Mysterious Note", "A note with a hint", "✉️", sort_order=11),
            Option("clue_sparkle_dust", "Sparkle Dust", "Glimmering magical dust", "✨", sort_order=12),
            Option("clue_hidden_door", "Hidden Door", "A door behind a secret wall", "🚪", sort_order=13),
            Option("clue_torn_photo", "Torn Photo", "A photo in pieces", "🖼️", sort_order=14),
            Option("clue_glowing_stone", "Glowing Stone", "A stone that lights up", "💡", sort_order=15),
            Option("clue_puzzle_piece", "Puzzle Piece", "A piece of a bigger puzzle", "🧩", sort_order=16),
            Option("clue_moonlight", "Moonlight", "Light from the moon", "🌙", sort_order=17),
            Option("clue_secret_ingredient", "Secret Ingredient", "A special recipe item", "🥣", sort_order=18),
            Option("clue_tiny_key", "Tiny Key", "A small but important key", "🗝️", sort_order=19),
            Option("clue_royal_letter", "Royal Letter", "A letter from a prince or princess", "📜", sort_order=20),
            Option("clue_cracked_shell", "Cracked Shell", "A broken shell clue", "🐚", sort_order=21),
            Option("clue_starlight_fragment", "Starlight Fragment", "A piece of glowing star", "🌟", sort_order=22),
            Option("clue_hidden_ribbon", "Hidden Ribbon", "A ribbon tied to a secret", "🎀", sort_order=23),
            Option("clue_lost_map", "Lost Map", "A missing treasure map", "🗺️", sort_order=24),
            Option("clue_scent_of_cinnamon", "Scent of Cinnamon", "A warm scent clue", "🌿", sort_order=25),
            Option("clue_mysterious_keyhole", "Mysterious Keyhole", "A keyhole with a hidden lock", "🔒", sort_order=26),
            Option("clue_glowing_ink", "Glowing Ink", "Writing that shines", "🖋️", sort_order=27),
            Option("clue_whispering_wind", "Whispering Wind", "Wind that carries a clue", "🌬️", sort_order=28),
            Option("clue_tiny_footprint", "Tiny Footprint", "A small set of tracks", "👣", sort_order=29),
            Option("clue_mystic_leaf", "Mystic Leaf", "A leaf with magic power", "🍃", sort_order=30),
            Option("clue_locket", "Locket", "A keepsake with a secret", "📿", sort_order=31),
            Option("clue_ancient_coin", "Ancient Coin", "A coin from long ago", "🪙", sort_order=32),
            Option("clue_hidden_message", "Hidden Message", "A secret written message", "📝", sort_order=33),
            Option("clue_glowing_pebble", "Glowing Pebble", "A pebble that glows softly", "🪨", sort_order=34),
            Option("clue_cracked_globe", "Cracked Globe", "A globe with a hidden map", "🌎", sort_order=35),
            Option("clue_cloth_rag", "Cloth Rag", "A worn cloth with a clue", "🧵", sort_order=36),
            Option("clue_silver_thread", "Silver Thread", "A thread that leads the way", "🧵", sort_order=37),
            Option("clue_hidden_button", "Hidden Button", "A button that opens something", "🔘", sort_order=38),
            Option("clue_glimmering_scale", "Glimmering Scale", "A scale from a magical creature", "🐉", sort_order=39),
            Option("clue_sunbeam", "Sunbeam", "A ray of sunlight clue", "☀️", sort_order=40),
        ]
    )
    
    # ============================================================
    # STORY TITLES
    # ============================================================
    STORY_TITLES = OptionGroup(
        name="story_titles",
        label="Story Titles",
        description="Category-specific titles for children's stories",
        icon="📚",
        sort_order=41,
        options=[
            Option("bedtime_moonlight", "The Soft Moonlight Adventure", "A gentle journey under the moon", "🌙", sort_order=1),
            Option("bedtime_sleepy_star", "The Sleepy Little Star", "A star searching for rest", "⭐", sort_order=2),
            Option("bedtime_cozy_blanket", "The Cozy Blanket Fort", "Building a warm nest", "🛌", sort_order=3),
            Option("bedtime_lullaby_forest", "The Lullaby Forest", "Trees that sing sleepy songs", "🌲", sort_order=4),
            Option("bedtime_dreamy_cloud", "The Dreamy Cloud Ride", "Floating on soft clouds", "☁️", sort_order=5),
            Option("bedtime_teddy_goodnight", "The Teddy Bear's Goodnight", "A bear's bedtime ritual", "🧸", sort_order=6),
            Option("bedtime_whispering_wind", "The Whispering Wind", "Wind that carries lullabies", "💨", sort_order=7),
            Option("bedtime_nighttime_garden", "The Nighttime Garden", "Flowers that glow at dusk", "🌷", sort_order=8),
            Option("bedtime_yawn_traveled", "The Yawn That Traveled", "A yawn spreading through the land", "😴", sort_order=9),
            Option("bedtime_pillow_palace", "The Pillow Palace", "A kingdom of soft pillows", "🛋️", sort_order=10),
            Option("bedtime_twinkling_goodnight", "The Twinkling Goodnight", "Stars saying goodnight", "✨", sort_order=11),
            Option("bedtime_sleepy_sloth", "The Sleepy Sloth's Journey", "A sloth finding a bedtime tree", "🦥", sort_order=12),
            Option("bedtime_moonbeam_ladder", "The Moonbeam Ladder", "Climbing to dreamland", "🌜", sort_order=13),
            Option("bedtime_hushabye_express", "The Hushabye Express", "A train to sleepy town", "🚂", sort_order=14),
            Option("bedtime_starlight_blanket", "The Starlight Blanket", "A blanket woven from stars", "🌟", sort_order=15),
            Option("bedtime_dozing_dragon", "The Dozing Dragon", "A dragon learning to sleep", "🐉", sort_order=16),
            Option("bedtime_quiet_pond", "The Quiet Pond Story", "Still water at bedtime", "🐸", sort_order=17),
            Option("bedtime_butterfly_night", "The Bedtime Butterfly", "A butterfly settling for the night", "🦋", sort_order=18),
            Option("bedtime_dream_chaser", "The Dream Chaser", "Catching sweet dreams", "💭", sort_order=19),
            Option("bedtime_sleepy_puppy", "The Sleepy Puppy's Adventure", "A puppy curling up tight", "🐶", sort_order=20),
            Option("moral_honest_fox", "The Honest Little Fox", "Truth always wins", "🦊", sort_order=21),
            Option("moral_kindness_tree", "The Kindness Tree", "A tree that gives to all", "🌳", sort_order=22),
            Option("moral_sharing_rainbow", "The Sharing Rainbow", "Colors shared with friends", "🌈", sort_order=23),
            Option("moral_brave_seed", "The Brave Little Seed", "Courage to grow tall", "🌱", sort_order=24),
            Option("moral_helpful_ants", "The Helpful Ants", "Teamwork saves the day", "🐜", sort_order=25),
            Option("moral_truthful_turtle", "The Truthful Turtle", "Honesty over speed", "🐢", sort_order=26),
            Option("moral_patient_caterpillar", "The Patient Caterpillar", "Waiting for beautiful wings", "🐛", sort_order=27),
            Option("moral_respectful_river", "The Respectful River", "Flowing kindly around all", "🏞️", sort_order=28),
            Option("moral_generous_bee", "The Generous Bee", "Sharing sweet nectar", "🐝", sort_order=29),
            Option("moral_forgiveness_flower", "The Forgiveness Flower", "Blooming after a storm", "🌸", sort_order=30),
            Option("moral_grateful_sparrow", "The Grateful Sparrow", "Thanking those who help", "🐦", sort_order=31),
            Option("moral_caring_cloud", "The Caring Cloud", "A cloud that rains kindness", "☁️", sort_order=32),
            Option("moral_polite_penguin", "The Polite Penguin", "Manners in the cold", "🐧", sort_order=33),
            Option("moral_wise_oak", "The Wise Old Oak", "Lessons from a strong tree", "🌳", sort_order=34),
            Option("moral_gentle_giant", "The Gentle Giant", "Strength used with kindness", "👹", sort_order=35),
            Option("moral_loyal_dog", "The Loyal Dog", "A friend who never leaves", "🐕", sort_order=36),
            Option("moral_thankful_raindrop", "The Thankful Raindrop", "Gratitude falling from clouds", "💧", sort_order=37),
            Option("moral_helpful_hedgehog", "The Helpful Hedgehog", "Small help, big heart", "🦔", sort_order=38),
            Option("moral_brave_mouse", "The Brave Little Mouse", "Courage in a tiny heart", "🐭", sort_order=39),
            Option("moral_honest_bee", "The Honest Bee", "Truth in every buzz", "🐝", sort_order=40),
            Option("adventure_lost_treasure", "The Lost Treasure Map", "A map to hidden gold", "🗺️", sort_order=41),
            Option("adventure_hidden_cave", "The Hidden Cave Explorer", "Discovering a secret cave", "🕳️", sort_order=42),
            Option("adventure_mountain_climb", "The Mountain Climb", "Scaling the tallest peak", "⛰️", sort_order=43),
            Option("adventure_river_quest", "The River Quest", "Following the winding river", "🏞️", sort_order=44),
            Option("adventure_secret_island", "The Secret Island", "Finding a hidden paradise", "🏝️", sort_order=45),
            Option("adventure_brave_expedition", "The Brave Expedition", "A journey into the unknown", "🧭", sort_order=46),
            Option("adventure_enchanted_path", "The Enchanted Forest Path", "A trail full of magic", "🌲", sort_order=47),
            Option("adventure_golden_compass", "The Golden Compass", "Finding the way forward", "🧭", sort_order=48),
            Option("adventure_pirate_cove", "The Pirate's Hidden Cove", "Treasure beneath the sand", "🏴‍☠️", sort_order=49),
            Option("adventure_volcanic", "The Volcanic Adventure", "Crossing fire and ash", "🌋", sort_order=50),
            Option("adventure_ancient_ruins", "The Ancient Ruins", "Echoes of the past", "🏛️", sort_order=51),
            Option("adventure_storm_chaser", "The Storm Chaser", "Racing the thunder", "⛈️", sort_order=52),
            Option("adventure_desert_journey", "The Desert Journey", "Crossing golden sands", "🏜️", sort_order=53),
            Option("adventure_underground_maze", "The Underground Maze", "Tunnels full of wonder", "🕳️", sort_order=54),
            Option("adventure_sky_mission", "The Sky High Mission", "Above the clouds", "✈️", sort_order=55),
            Option("adventure_crystal_cave", "The Crystal Cave", "Gems that light the way", "💎", sort_order=56),
            Option("adventure_forgotten_bridge", "The Forgotten Bridge", "A path to the other side", "🌉", sort_order=57),
            Option("adventure_wild_west", "The Wild West Quest", "Cowboys and canyons", "🤠", sort_order=58),
            Option("adventure_jungle_expedition", "The Jungle Expedition", "Through green wilderness", "🌿", sort_order=59),
            Option("adventure_ice_cave", "The Ice Cave Discovery", "Frozen tunnels of ice", "❄️", sort_order=60),
            Option("fairy_crystal_slipper", "The Crystal Slipper", "A shoe of magic and grace", "👠", sort_order=61),
            Option("fairy_enchanted_rose", "The Enchanted Rose", "A rose that never fades", "🌹", sort_order=62),
            Option("fairy_magic_mirror", "The Magic Mirror", "A mirror that tells the truth", "🪞", sort_order=63),
            Option("fairy_wishing_star", "The Wishing Star", "A star that grants desires", "⭐", sort_order=64),
            Option("fairy_godmother_gift", "The Fairy Godmother's Gift", "Magic help at midnight", "🧚", sort_order=65),
            Option("fairy_dragons_secret", "The Dragon's Secret", "A dragon with a gentle heart", "🐉", sort_order=66),
            Option("fairy_princess_pea", "The Princess and the Pea", "A true princess test", "👸", sort_order=67),
            Option("fairy_golden_goose", "The Golden Goose", "A goose of golden eggs", "🪿", sort_order=68),
            Option("fairy_magic_beans", "The Magic Beans", "Beans that grow to the sky", "🌱", sort_order=69),
            Option("fairy_talking_mirror", "The Talking Mirror", "A mirror with a voice", "🗣️", sort_order=70),
            Option("fairy_hidden_kingdom", "The Hidden Kingdom", "A kingdom behind a waterfall", "🏰", sort_order=71),
            Option("fairy_spellbound_forest", "The Spellbound Forest", "Trees full of fairy magic", "🌲", sort_order=72),
            Option("fairy_royal_ball", "The Royal Ball", "A night of magic and dance", "💃", sort_order=73),
            Option("fairy_witch_cottage", "The Witch's Cottage", "Gingerbread and spells", "🏚️", sort_order=74),
            Option("fairy_fairy_ring", "The Fairy Ring", "A circle of dancing sprites", "🍄", sort_order=75),
            Option("fairy_silver_crown", "The Silver Crown", "A crown of moonlight", "👑", sort_order=76),
            Option("fairy_unicorn_gift", "The Unicorn's Gift", "A horn of healing light", "🦄", sort_order=77),
            Option("fairy_mermaid_pearl", "The Mermaid's Pearl", "A pearl from the deep", "🧜", sort_order=78),
            Option("fairy_wizard_tower", "The Wizard's Tower", "A tower of ancient spells", "🗼", sort_order=79),
            Option("fairy_magic_carpet", "The Magic Carpet", "A carpet that flies", "🪁", sort_order=80),
            Option("islamic_patient_prophet", "The Patient Prophet", "Faith through hard times", "🌙", sort_order=81),
            Option("islamic_honest_merchant", "The Honest Merchant", "Truth in every trade", "⚖️", sort_order=82),
            Option("islamic_kind_neighbor", "The Kind Neighbor", "Caring across fences", "🤲", sort_order=83),
            Option("islamic_truthful_camel", "The Truthful Camel", "A camel of honesty", "🐪", sort_order=84),
            Option("islamic_sharing_date", "The Sharing Date Tree", "Dates given freely", "🌴", sort_order=85),
            Option("islamic_grateful_orphan", "The Grateful Orphan", "Thankful for every blessing", "🙏", sort_order=86),
            Option("islamic_respectful_child", "The Respectful Child", "Kind words to elders", "👦", sort_order=87),
            Option("islamic_helpful_siblings", "The Helpful Siblings", "Brothers and sisters who care", "👨‍👩‍👧‍👦", sort_order=88),
            Option("islamic_brave_believer", "The Brave Little Believer", "Standing firm in faith", "💪", sort_order=89),
            Option("islamic_trusting_fisherman", "The Trusting Fisherman", "Faith while casting nets", "🎣", sort_order=90),
            Option("islamic_forgiving_friend", "The Forgiving Friend", "Letting go with grace", "🕊️", sort_order=91),
            Option("islamic_generous_baker", "The Generous Baker", "Bread shared with all", "🍞", sort_order=92),
            Option("islamic_prayerful_bird", "The Prayerful Little Bird", "Wings that remember Allah", "🐦", sort_order=93),
            Option("islamic_just_judge", "The Just Judge", "Fairness for everyone", "⚖️", sort_order=94),
            Option("islamic_humble_scholar", "The Humble Scholar", "Wisdom with humility", "📚", sort_order=95),
            Option("islamic_patient_gardener", "The Patient Gardener", "Waiting for the harvest", "🌱", sort_order=96),
            Option("islamic_truthful_keeper", "The Truthful Keeper", "A trust never broken", "🗝️", sort_order=97),
            Option("islamic_kind_helper", "The Kind Helper", "Lending a hand always", "🤝", sort_order=98),
            Option("islamic_gentle_teacher", "The Gentle Teacher", "Knowledge shared with love", "📖", sort_order=99),
            Option("islamic_trustworthy_friend", "The Trustworthy Friend", "A friend who keeps promises", "🤝", sort_order=100),
            Option("jungle_monkey_swing", "The Monkey's Big Swing", "Swinging through the trees", "🐒", sort_order=101),
            Option("jungle_lion_roar", "The Lion's Roar", "The king of the jungle speaks", "🦁", sort_order=102),
            Option("jungle_elephant_bath", "The Elephant's Bath", "A giant's spa day", "🐘", sort_order=103),
            Option("jungle_parrot_secret", "The Parrot's Secret", "A bird who knows too much", "🦜", sort_order=104),
            Option("jungle_snake_path", "The Snake's Hidden Path", "A winding trail to follow", "🐍", sort_order=105),
            Option("jungle_tiger_stalk", "The Tiger's Stalk", "A silent walk through ferns", "🐅", sort_order=106),
            Option("jungle_crocodile_smile", "The Crocodile's Smile", "A grin by the river", "🐊", sort_order=107),
            Option("jungle_gorilla_treasure", "The Gorilla's Treasure", "A chest deep in the vines", "🦍", sort_order=108),
            Option("jungle_cheetah_race", "The Cheetah's Race", "Fastest paws in the jungle", "🐆", sort_order=109),
            Option("jungle_hippo_yawn", "The Hippo's Yawn", "A giant morning stretch", "🦛", sort_order=110),
            Option("jungle_giraffe_neck", "The Giraffe's Neck", "The tallest view in town", "🦒", sort_order=111),
            Option("jungle_panda_feast", "The Panda's Bamboo Feast", "Crunching green treats", "🐼", sort_order=112),
            Option("jungle_bear_honey", "The Bear's Honey Pot", "A sweet treasure found", "🐻", sort_order=113),
            Option("jungle_fox_plan", "The Fox's Clever Plan", "Outsmarting the jungle", "🦊", sort_order=114),
            Option("jungle_rabbit_burrow", "The Rabbit's Burrow", "A cozy home underground", "🐰", sort_order=115),
            Option("jungle_owl_watch", "The Owl's Night Watch", "Eyes in the dark trees", "🦉", sort_order=116),
            Option("jungle_frog_pond", "The Frog's Pond", "Ribbits by the lily pads", "🐸", sort_order=117),
            Option("jungle_turtle_journey", "The Turtle's Slow Journey", "Steady steps through leaves", "🐢", sort_order=118),
            Option("jungle_deer_leap", "The Deer's Leaping", "Grace in the green", "🦌", sort_order=119),
            Option("jungle_peacock_feathers", "The Peacock's Feathers", "Colors that dazzle", "🦚", sort_order=120),
            Option("space_rocket_mars", "The Rocket to Mars", "Blasting off to the red planet", "🚀", sort_order=121),
            Option("space_moon_base", "The Moon Base Adventure", "Living on lunar soil", "🌕", sort_order=122),
            Option("space_alien_encounter", "The Alien Encounter", "Meeting a friend from far away", "👽", sort_order=123),
            Option("space_asteroid_field", "The Asteroid Field", "Dodging space rocks", "☄️", sort_order=124),
            Option("space_star_explorer", "The Star Explorer", "Mapping distant suns", "⭐", sort_order=125),
            Option("space_station_mystery", "The Space Station Mystery", "A secret on the station", "🛰️", sort_order=126),
            Option("space_jupiter_journey", "The Jupiter Journey", "Orbiting the giant planet", "🪐", sort_order=127),
            Option("space_saturn_rings", "The Saturn Rings", "Skating on icy rings", "🪐", sort_order=128),
            Option("space_black_hole", "The Black Hole", "A mystery of gravity", "🕳️", sort_order=129),
            Option("space_comet_chase", "The Comet Chase", "Riding a fiery tail", "☄️", sort_order=130),
            Option("space_galaxy_quest", "The Galaxy Quest", "Sailing the Milky Way", "🌌", sort_order=131),
            Option("space_spacewalk", "The Spacewalk", "Floating in the void", "🚶", sort_order=132),
            Option("space_alien_friend", "The Alien Friend", "A buddy from another world", "👽", sort_order=133),
            Option("space_mars_rover", "The Mars Rover", "Driving on red dunes", "🛻", sort_order=134),
            Option("space_moon_buggy", "The Moon Buggy", "Bouncing on craters", "🚙", sort_order=135),
            Option("space_star_map", "The Star Map", "Charting new worlds", "🗺️", sort_order=136),
            Option("space_cosmic_storm", "The Cosmic Storm", "Weather in deep space", "⛈️", sort_order=137),
            Option("space_solar_tour", "The Solar System Tour", "Visiting every planet", "🌍", sort_order=138),
            Option("space_rescue", "The Space Rescue", "Saving a stranded ship", "🚑", sort_order=139),
            Option("space_meteor_shower", "The Meteor Shower", "Dancing with shooting stars", "🌠", sort_order=140),
            Option("funny_dance_party", "The Silly Dance Party", "Dancing till you drop", "💃", sort_order=141),
            Option("funny_laughing_cloud", "The Laughing Cloud", "A cloud that giggles rain", "☁️", sort_order=142),
            Option("funny_jellybean_rain", "The Jellybean Rain", "Sweet drops from the sky", "🍬", sort_order=143),
            Option("funny_backwards_day", "The Backwards Day", "Everything topsy-turvy", "🔄", sort_order=144),
            Option("funny_giggle_factory", "The Giggle Factory", "A building that laughs", "🏭", sort_order=145),
            Option("funny_bouncing_bed", "The Bouncing Bed", "A bed that jumps", "🛏️", sort_order=146),
            Option("funny_talking_sock", "The Talking Sock", "A sock with opinions", "🧦", sort_order=147),
            Option("funny_ice_cream_snow", "The Ice Cream Snow", "A frosty sweet storm", "🍦", sort_order=148),
            Option("funny_invisible_homework", "The Invisible Homework", "Assignments that vanish", "📚", sort_order=149),
            Option("funny_flying_chair", "The Flying Chair", "A seat that soars", "🪑", sort_order=150),
            Option("funny_chocolate_river", "The Chocolate River", "Flowing sweet treats", "🍫", sort_order=151),
            Option("funny_dancing_tree", "The Dancing Tree", "A tree with rhythm", "🌳", sort_order=152),
            Option("funny_bubble_trouble", "The Bubble Trouble", "Bubbles everywhere", "🫧", sort_order=153),
            Option("funny_hat_parade", "The Silly Hat Parade", "Hats of every shape", "🎩", sort_order=154),
            Option("funny_pizza_planet", "The Pizza Planet", "A world of pepperoni", "🍕", sort_order=155),
            Option("funny_giggling_shadows", "The Giggling Shadows", "Shadows that laugh back", "👥", sort_order=156),
            Option("funny_wobbly_tooth", "The Wobbly Tooth", "A tooth with a plan", "🦷", sort_order=157),
            Option("funny_sneezing_dragon", "The Sneezing Dragon", "A dragon with allergies", "🐉", sort_order=158),
            Option("funny_topsy_turvy", "The Topsy-Turvy Town", "Where upside-down is right", "🏘️", sort_order=159),
            Option("funny_magic_pencil", "The Magic Pencil", "A pencil with a mind", "✏️", sort_order=160),
            Option("mystery_missing_key", "The Missing Key", "A key that disappeared", "🗝️", sort_order=161),
            Option("mystery_hidden_treasure", "The Hidden Treasure", "Gold tucked away", "💰", sort_order=162),
            Option("mystery_secret_door", "The Secret Door", "A door no one sees", "🚪", sort_order=163),
            Option("mystery_lost_map", "The Lost Map", "Directions gone missing", "🗺️", sort_order=164),
            Option("mystery_strange_footprints", "The Strange Footprints", "Tracks in the hall", "👣", sort_order=165),
            Option("mystery_ghost_light", "The Ghost Light", "A glow without a source", "👻", sort_order=166),
            Option("mystery_missing_crown", "The Missing Crown", "A royal crown stolen", "👑", sort_order=167),
            Option("mystery_talking_statue", "The Talking Statue", "A statue with secrets", "🗿", sort_order=168),
            Option("mystery_whispering_wind", "The Whispering Wind", "Wind that tells tales", "🌬️", sort_order=169),
            Option("mystery_disappearing_path", "The Disappearing Path", "A trail that vanishes", "🛣️", sort_order=170),
            Option("mystery_magic_necklace", "The Magic Necklace", "A necklace of riddles", "📿", sort_order=171),
            Option("mystery_secret_code", "The Secret Code", "A cipher to crack", "🔐", sort_order=172),
            Option("mystery_hidden_note", "The Hidden Note", "A message tucked away", "📝", sort_order=173),
            Option("mystery_starlit_key", "The Starlit Key", "A key glowing at night", "🔑", sort_order=174),
            Option("mystery_mirror_maze", "The Mirror Maze", "Reflections that confuse", "🪞", sort_order=175),
            Option("mystery_vanishing_rainbow", "The Vanishing Rainbow", "Colors that fade away", "🌈", sort_order=176),
            Option("mystery_silver_bell", "The Silver Bell", "A bell with a secret ring", "🔔", sort_order=177),
            Option("mystery_time_capsule", "The Time Capsule", "A message from the past", "⌛", sort_order=178),
            Option("mystery_dusty_attic", "The Dusty Attic", "A room full of clues", "🏚️", sort_order=179),
            Option("mystery_cloud_castle", "The Cloud Castle", "A fortress in the sky", "☁️", sort_order=180),
        ]
    )
    
    # ============================================================
    # STORY CHARACTERS & ELEMENTS
    # ============================================================
    STORY_MAIN_CHARACTERS = OptionGroup(
        name="story_main_characters",
        label="Story Main Characters",
        description="Kid-friendly main character options",
        icon="🦸",
        sort_order=42,
        options=[
            Option("luna_the_brave", "Luna the Brave", "A curious and courageous girl", "🌙", sort_order=1),
            Option("captain_cosmos", "Captain Cosmos", "A space explorer kid", "🚀", sort_order=2),
            Option("princess_aurora", "Princess Aurora", "A kind and clever princess", "👸", sort_order=3),
            Option("max_the_dragon", "Max the Dragon", "A friendly young dragon", "🐉", sort_order=4),
            Option("zara_the_fairy", "Zara the Fairy", "A tiny fairy with big magic", "🧚", sort_order=5),
            Option("leo_the_lion", "Leo the Lion", "A brave little lion cub", "🦁", sort_order=6),
            Option("nina_the_mermaid", "Nina the Mermaid", "An ocean-loving mermaid", "🧜", sort_order=7),
            Option("tommy_robot", "Tommy Robot", "A helpful robot friend", "🤖", sort_order=8),
            Option("sophie_superhero", "Sophie Superhero", "A hero with a cape", "🦸", sort_order=9),
            Option("ollie_owl", "Ollie Owl", "A wise little owl", "🦉", sort_order=10),
            Option("mia_the_explorer", "Mia the Explorer", "An adventurous discoverer", "🧭", sort_order=11),
            Option("felix_fox", "Felix Fox", "A clever and sneaky fox", "🦊", sort_order=12),
        ]
    )
    
    STORY_COMPANIONS = OptionGroup(
        name="story_companions",
        label="Story Companions",
        description="Animal and fantasy companion options",
        icon="🐧",
        sort_order=43,
        options=[
            Option("pip_the_penguin", "Pip the Penguin", "A waddling friend", "🐧", sort_order=1),
            Option("spark_the_dragon", "Spark the Dragon", "A tiny fire-breather", "🐉", sort_order=2),
            Option("bella_butterfly", "Bella Butterfly", "A colorful flying buddy", "🦋", sort_order=3),
            Option("rocky_rabbit", "Rocky Rabbit", "A fast-hopping pal", "🐰", sort_order=4),
            Option("chatter_squirrel", "Chatter Squirrel", "A nut-loving chatterbox", "🐿️", sort_order=5),
            Option("waves_dolphin", "Waves Dolphin", "A playful ocean friend", "🐬", sort_order=6),
            Option("flutter_bird", "Flutter Bird", "A tiny singing bird", "🐦", sort_order=7),
            Option("cuddles_bear", "Cuddles Bear", "A soft and warm bear", "🐻", sort_order=8),
            Option("swift_fox", "Swift Fox", "A quick and clever fox", "🦊", sort_order=9),
            Option("giggles_monkey", "Giggles Monkey", "A silly swinging buddy", "🐒", sort_order=10),
            Option("stripe_tiger", "Stripe Tiger", "A brave little tiger", "🐅", sort_order=11),
            Option("pegasus_foal", "Pegasus Foal", "A tiny winged horse", "🦄", sort_order=12),
        ]
    )
    
    STORY_MORAL_LESSONS = OptionGroup(
        name="story_moral_lessons",
        label="Moral Lessons",
        description="Values and lessons for stories",
        icon="💖",
        sort_order=44,
        options=[
            Option("always_be_kind", "Always Be Kind", "Kindness wins every time", "💖", sort_order=1),
            Option("honesty_is_best", "Honesty Is Best", "Truth is always right", "🤍", sort_order=2),
            Option("help_others", "Help Others", "Lending a hand matters", "🤝", sort_order=3),
            Option("share_with_friends", "Share With Friends", "Sharing brings joy", "🎁", sort_order=4),
            Option("be_brave", "Be Brave", "Courage inside you", "💪", sort_order=5),
            Option("never_give_up", "Never Give Up", "Keep trying always", "🏆", sort_order=6),
            Option("respect_everyone", "Respect Everyone", "Treat all with care", "🙏", sort_order=7),
            Option("gratitude_matters", "Gratitude Matters", "Thankful heart is happy", "🙌", sort_order=8),
        ]
    )
    
    STORY_BACKGROUNDS = OptionGroup(
        name="story_backgrounds",
        label="Story Backgrounds",
        description="Enchanting settings and environments",
        icon="🌄",
        sort_order=45,
        options=[
            Option("sunset_meadow", "Sunset Meadow", "A field of golden light", "🌅", sort_order=1),
            Option("enchanted_forest", "Enchanted Forest", "Trees full of magic", "🌲", sort_order=2),
            Option("starry_night_sky", "Starry Night Sky", "Twinkling stars above", "🌌", sort_order=3),
            Option("cozy_village", "Cozy Village", "A warm little town", "🏘️", sort_order=4),
            Option("mountain_top", "Mountain Top", "High above the clouds", "⛰️", sort_order=5),
            Option("underwater_cave", "Underwater Cave", "Deep blue secrets", "🌊", sort_order=6),
            Option("cloud_kingdom", "Cloud Kingdom", "A land of soft clouds", "☁️", sort_order=7),
            Option("candy_land", "Candy Land", "Sweet treats everywhere", "🍭", sort_order=8),
            Option("jungle_waterfall", "Jungle Waterfall", "Roaring water and green vines", "🌿", sort_order=9),
            Option("castle_tower", "Castle Tower", "A tall stone fortress", "🏰", sort_order=10),
            Option("space_station", "Space Station", "Orbiting high above Earth", "🛰️", sort_order=11),
            Option("secret_garden", "Secret Garden", "A hidden flower paradise", "🌷", sort_order=12),
        ]
    )
    
    STORY_SUPPORTING_CHARACTERS = OptionGroup(
        name="story_supporting_characters",
        label="Supporting Characters",
        description="Friends and helpers in the story",
        icon="🐧",
        sort_order=46,
        options=[
            Option("pip_the_penguin", "Pip the Penguin", "A loyal friend", "🐧", sort_order=1),
            Option("professor_owl", "Professor Owl", "A wise helper", "🦉", sort_order=2),
            Option("sparky_robot", "Sparky Robot", "A helpful machine", "🤖", sort_order=3),
            Option("bella_fairy", "Bella Fairy", "A magical guide", "🧚", sort_order=4),
            Option("rocky_bear", "Rocky Bear", "A strong protector", "🐻", sort_order=5),
            Option("chatter_squirrel", "Chatter Squirrel", "A quick messenger", "🐿️", sort_order=6),
            Option("waves_dolphin", "Waves Dolphin", "An ocean guide", "🐬", sort_order=7),
            Option("felix_fox", "Felix Fox", "A clever trickster", "🦊", sort_order=8),
            Option("giggles_monkey", "Giggles Monkey", "A funny companion", "🐒", sort_order=9),
            Option("stripe_tiger", "Stripe Tiger", "A brave ally", "🐅", sort_order=10),
            Option("pegasus_foal", "Pegasus Foal", "A winged helper", "🦄", sort_order=11),
            Option("cuddles_bear", "Cuddles Bear", "A soft friend", "🐻", sort_order=12),
        ]
    )
    
    STORY_HEROES = OptionGroup(
        name="story_heroes",
        label="Story Heroes",
        description="Brave heroes for adventure stories",
        icon="🦸",
        sort_order=47,
        options=[
            Option("captain_cosmos", "Captain Cosmos", "A space explorer hero", "🚀", sort_order=1),
            Option("sir_gallant", "Sir Gallant", "A knight of honor", "⚔️", sort_order=2),
            Option("ninja_nova", "Ninja Nova", "A stealthy hero", "🥷", sort_order=3),
            Option("super_sam", "Super Sam", "A strong and kind hero", "🦸", sort_order=4),
            Option("pirate_pete", "Pirate Pete", "A friendly sea captain", "🏴‍☠️", sort_order=5),
            Option("wizard_will", "Wizard Will", "A young magic user", "🧙", sort_order=6),
            Option("ranger_rachel", "Ranger Rachel", "A nature protector", "🌿", sort_order=7),
            Option("inventor_ivan", "Inventor Ivan", "A creative builder", "🔧", sort_order=8),
            Option("detective_daisy", "Detective Daisy", "A sharp-eyed sleuth", "🕵️", sort_order=9),
            Option("hero_henry", "Hero Henry", "An everyday hero", "🌟", sort_order=10),
            Option("knight_lily", "Knight Lily", "A brave young knight", "🛡️", sort_order=11),
            Option("captain_storm", "Captain Storm", "A daring leader", "⛈️", sort_order=12),
        ]
    )
    
    STORY_SIDEKICKS = OptionGroup(
        name="story_sidekicks",
        label="Story Sidekicks",
        description="Loyal sidekicks for heroes",
        icon="🤖",
        sort_order=48,
        options=[
            Option("sparky_robot", "Sparky Robot", "A funny robot buddy", "🤖", sort_order=1),
            Option("whiskers_cat", "Whiskers Cat", "A sneaky little cat", "🐱", sort_order=2),
            Option("buzz_bee", "Buzz Bee", "A busy little bee", "🐝", sort_order=3),
            Option("chirp_bird", "Chirp Bird", "A singing messenger", "🐦", sort_order=4),
            Option("hoppy_frog", "Hoppy Frog", "A jumpy friend", "🐸", sort_order=5),
            Option("swift_fox", "Swift Fox", "A fast and sly fox", "🦊", sort_order=6),
            Option("giggles_monkey", "Giggles Monkey", "A silly sidekick", "🐒", sort_order=7),
            Option("rocky_turtle", "Rocky Turtle", "A slow but steady friend", "🐢", sort_order=8),
            Option("daisy_dog", "Daisy Dog", "A loyal puppy", "🐶", sort_order=9),
            Option("stripe_tiger", "Stripe Tiger", "A fierce little tiger", "🐅", sort_order=10),
            Option("flutter_butterfly", "Flutter Butterfly", "A tiny magical helper", "🦋", sort_order=11),
            Option("pegasus_foal", "Pegasus Foal", "A tiny winged horse", "🦄", sort_order=12),
        ]
    )
    
    STORY_VILLAINS = OptionGroup(
        name="story_villains",
        label="Story Villains",
        description="Not-so-scary villains for kids",
        icon="👑",
        sort_order=49,
        options=[
            Option("the_shadow_king", "The Shadow King", "A misunderstood ruler", "👑", sort_order=1),
            Option("dr_chaos", "Dr. Chaos", "A silly mad scientist", "🧪", sort_order=2),
            Option("grumble_goblin", "Grumble Goblin", "A grumpy but funny goblin", "👺", sort_order=3),
            Option("wicked_witch", "Wicked Witch", "A spell-casting troublemaker", "🧙‍♀️", sort_order=4),
            Option("sly_snake", "Sly Snake", "A cunning trickster", "🐍", sort_order=5),
            Option("foggi_ghost", "Foggi Ghost", "A shy spooky spirit", "👻", sort_order=6),
            Option("robo_rascal", "Robo Rascal", "A mischievous robot", "🤖", sort_order=7),
            Option("buzz_fly", "Buzz Fly", "A buzzing nuisance", "🪰", sort_order=8),
            Option("crabby_captain", "Crabby Captain", "A grumpy sea captain", "🏴‍☠️", sort_order=9),
            Option("storm_dragon", "Storm Dragon", "A loud but not-so-scary dragon", "🐉", sort_order=10),
            Option("troll_tremor", "Troll Tremor", "A bridge-dwelling grump", "🧌", sort_order=11),
            Option("moody_wizard", "Moody Wizard", "A temperamental magic user", "🧙", sort_order=12),
        ]
    )
    
    STORY_OBSTACLES = OptionGroup(
        name="story_obstacles",
        label="Story Obstacles",
        description="Challenges and obstacles for heroes",
        icon="🧩",
        sort_order=50,
        options=[
            Option("a_difficult_challenge", "A Difficult Challenge", "Something hard to overcome", "🧩", sort_order=1),
            Option("dark_forest", "Dark Forest", "A spooky path ahead", "🌲", sort_order=2),
            Option("raging_river", "Raging River", "Water blocking the way", "🌊", sort_order=3),
            Option("tall_mountain", "Tall Mountain", "A steep climb needed", "⛰️", sort_order=4),
            Option("mystery_door", "Mystery Door", "A locked door with no key", "🚪", sort_order=5),
            Option("lost_map", "Lost Map", "Directions gone missing", "🗺️", sort_order=6),
            Option("foggy_path", "Foggy Path", "Can't see what's ahead", "🌫️", sort_order=7),
            Option("broken_bridge", "Broken Bridge", "A gap too wide to jump", "🌉", sort_order=8),
        ]
    )
    
    STORY_PRINCESSES_PRINCES = OptionGroup(
        name="story_princesses_princes",
        label="Princesses and Princes",
        description="Royal characters for fairy tales",
        icon="👸",
        sort_order=51,
        options=[
            Option("princess_aurora", "Princess Aurora", "A kind sleeping beauty", "👸", sort_order=1),
            Option("princess_jasmine", "Princess Jasmine", "A brave desert princess", "👸", sort_order=2),
            Option("princess_sofia", "Princess Sofia", "A curious young queen", "👸", sort_order=3),
            Option("princess_ella", "Princess Ella", "A gentle glass slipper girl", "👸", sort_order=4),
            Option("prince_charming", "Prince Charming", "A gallant prince", "🤴", sort_order=5),
            Option("prince_eric", "Prince Eric", "A sea-loving prince", "🤴", sort_order=6),
            Option("prince_philip", "Prince Philip", "A dragon-slaying prince", "🤴", sort_order=7),
            Option("prince_naveen", "Prince Naveen", "A frog prince with fun", "🤴", sort_order=8),
            Option("princess_mulan", "Princess Mulan", "A warrior princess", "👸", sort_order=9),
            Option("princess_tiana", "Princess Tiana", "A hardworking princess", "👸", sort_order=10),
            Option("prince_aladdin", "Prince Aladdin", "A street-smart prince", "🤴", sort_order=11),
            Option("princess_rapunzel", "Princess Rapunzel", "A long-haired princess", "👸", sort_order=12),
        ]
    )
    
    STORY_MAGICAL_CHARACTERS = OptionGroup(
        name="story_magical_characters",
        label="Magical Characters",
        description="Wizards, fairies, and magical beings",
        icon="🧚",
        sort_order=52,
        options=[
            Option("fairy_godmother", "Fairy Godmother", "A helpful fairy", "🧚", sort_order=1),
            Option("merlin_wizard", "Merlin Wizard", "An ancient wise wizard", "🧙", sort_order=2),
            Option("gingerbread_witch", "Gingerbread Witch", "A sweet but tricky witch", "🏚️", sort_order=3),
            Option("unicorn_guardian", "Unicorn Guardian", "A magical horned horse", "🦄", sort_order=4),
            Option("dragon_friend", "Dragon Friend", "A tiny fire-breather", "🐉", sort_order=5),
            Option("magic_mirror", "Magic Mirror", "A truth-telling mirror", "🪞", sort_order=6),
            Option("wishing_star", "Wishing Star", "A star that grants wishes", "⭐", sort_order=7),
            Option("flying_carpet", "Flying Carpet", "A magic rug that flies", "🪁", sort_order=8),
            Option("potion_maker", "Potion Maker", "A brew-mixing alchemist", "⚗️", sort_order=9),
            Option("spell_book", "Spell Book", "A book of ancient magic", "📕", sort_order=10),
            Option("crystal_ball", "Crystal Ball", "A seeing orb", "🔮", sort_order=11),
            Option("magic_beanstalk", "Magic Beanstalk", "A bean that grows to sky", "🌱", sort_order=12),
        ]
    )
    
    STORY_KINGDOMS = OptionGroup(
        name="story_kingdoms",
        label="Kingdoms",
        description="Magical kingdoms and lands",
        icon="🏰",
        sort_order=53,
        options=[
            Option("a_magical_kingdom", "A Magical Kingdom", "A land of wonder", "🏰", sort_order=1),
            Option("enchanted_castle", "Enchanted Castle", "A tower of spells", "🏰", sort_order=2),
            Option("candy_kingdom", "Candy Kingdom", "A sweet sugary land", "🍭", sort_order=3),
            Option("underwater_kingdom", "Underwater Kingdom", "A deep blue realm", "🌊", sort_order=4),
            Option("cloud_kingdom", "Cloud Kingdom", "A fluffy sky land", "☁️", sort_order=5),
            Option("jungle_kingdom", "Jungle Kingdom", "A wild green empire", "🌿", sort_order=6),
            Option("space_kingdom", "Space Kingdom", "A star-filled realm", "🌌", sort_order=7),
            Option("toy_kingdom", "Toy Kingdom", "A land of play", "🧸", sort_order=8),
        ]
    )
    
    STORY_PROPHETS_PERSONALITIES = OptionGroup(
        name="story_prophets_personalities",
        label="Prophets and Personalities",
        description="Respected Islamic prophets and personalities",
        icon="🕌",
        sort_order=54,
        options=[
            Option("prophet_muhammad", "Prophet Muhammad (PBUH)", "The final prophet of Islam", "🌙", sort_order=1),
            Option("prophet_ibrahim", "Prophet Ibrahim (AS)", "The friend of Allah", "🕌", sort_order=2),
            Option("prophet_musa", "Prophet Musa (AS)", "The leader of Bani Israel", "🌊", sort_order=3),
            Option("prophet_isa", "Prophet Isa (AS)", "The messenger of peace", "🕊️", sort_order=4),
            Option("prophet_nuh", "Prophet Nuh (AS)", "The builder of the ark", "⛵", sort_order=5),
            Option("prophet_yusuf", "Prophet Yusuf (AS)", "The beautiful soul", "🌞", sort_order=6),
            Option("prophet_dawud", "Prophet Dawud (AS)", "The wise king", "👑", sort_order=7),
            Option("prophet_sulaiman", "Prophet Sulaiman (AS)", "The king of animals", "🦁", sort_order=8),
            Option("khadija_ra", "Khadija (RA)", "The first believer", "💎", sort_order=9),
            Option("aisha_ra", "Aisha (RA)", "The teacher of knowledge", "📚", sort_order=10),
            Option("ali_ra", "Ali (RA)", "The brave lion of Allah", "⚔️", sort_order=11),
            Option("bilal_ra", "Bilal (RA)", "The caller of prayer", "📢", sort_order=12),
        ]
    )
    
    STORY_LOCATIONS = OptionGroup(
        name="story_locations",
        label="Story Locations",
        description="Places and settings for stories",
        icon="📍",
        sort_order=55,
        options=[
            Option("a_peaceful_village", "A Peaceful Village", "A quiet small town", "🏘️", sort_order=1),
            Option("bustling_market", "Bustling Market", "A busy trading place", "🏪", sort_order=2),
            Option("green_valley", "Green Valley", "A lush green land", "🌿", sort_order=3),
            Option("desert_oasis", "Desert Oasis", "A water haven in sand", "🌴", sort_order=4),
            Option("snowy_mountain", "Snowy Mountain", "A cold tall peak", "❄️", sort_order=5),
            Option("beautiful_beach", "Beautiful Beach", "Sand and waves", "🏖️", sort_order=6),
            Option("old_library", "Old Library", "A room full of books", "📚", sort_order=7),
            Option("magic_garden", "Magic Garden", "Flowers that talk", "🌷", sort_order=8),
        ]
    )
    
    STORY_LESSONS = OptionGroup(
        name="story_lessons",
        label="Story Lessons",
        description="Educational lessons for stories",
        icon="📖",
        sort_order=56,
        options=[
            Option("an_important_lesson", "An Important Lesson", "Something to remember", "📖", sort_order=1),
            Option("friendship_forever", "Friendship Forever", "Friends last always", "🤝", sort_order=2),
            Option("courage_counts", "Courage Counts", "Bravery inside you", "💪", sort_order=3),
            Option("teamwork_wins", "Teamwork Wins", "Together we achieve", "👥", sort_order=4),
            Option("honesty_best", "Honesty Best", "Truth always matters", "🤍", sort_order=5),
            Option("share_care", "Share and Care", "Giving brings joy", "🎁", sort_order=6),
            Option("respect_all", "Respect All", "Treat everyone well", "🙏", sort_order=7),
            Option("try_again", "Try Again", "Never give up hope", "🏆", sort_order=8),
        ]
    )
    
    STORY_ASTRONAUTS = OptionGroup(
        name="story_astronauts",
        label="Astronauts",
        description="Space explorer characters",
        icon="👨‍🚀",
        sort_order=57,
        options=[
            Option("captain_nova", "Captain Nova", "A brave space captain", "🚀", sort_order=1),
            Option("commander_vega", "Commander Vega", "A skilled pilot", "👨‍🚀", sort_order=2),
            Option("astro_emma", "Astro Emma", "A curious scientist", "👩‍🚀", sort_order=3),
            Option("pilot_mars", "Pilot Mars", "A red-planet explorer", "🚀", sort_order=4),
            Option("luna_astronaut", "Luna Astronaut", "A moonwalker", "👩‍🚀", sort_order=5),
            Option("rocket_ron", "Rocket Ron", "A speed-loving astronaut", "🚀", sort_order=6),
            Option("star_sarah", "Star Sarah", "A constellation mapper", "⭐", sort_order=7),
            Option("orbit_oscar", "Orbit Oscar", "A station builder", "🛰️", sort_order=8),
            Option("comet_carla", "Comet Carla", "A trail-blazer", "☄️", sort_order=9),
            Option("galaxy_gabe", "Galaxy Gabe", "A deep-space explorer", "🌌", sort_order=10),
            Option("nebula_nina", "Nebula Nina", "A cloud walker", "🌌", sort_order=11),
            Option("zero_zoom", "Zero Zoom", "A zero-gravity ace", "👨‍🚀", sort_order=12),
        ]
    )
    
    STORY_ALIENS = OptionGroup(
        name="story_aliens",
        label="Aliens",
        description="Friendly alien characters",
        icon="👽",
        sort_order=58,
        options=[
            Option("zog_friendly_alien", "Zog the Friendly Alien", "A green little buddy", "👽", sort_order=1),
            Option("glimmer_star_being", "Glimmer Star Being", "A sparkling space friend", "✨", sort_order=2),
            Option("blip_robot", "Blip Robot", "A mechanical alien", "🤖", sort_order=3),
            Option("zorba_martian", "Zorba Martian", "A red planet visitor", "👽", sort_order=4),
            Option("cosmic_casper", "Cosmic Casper", "A friendly space ghost", "👻", sort_order=5),
            Option("nova_nebula", "Nova Nebula", "A star-born alien", "🌟", sort_order=6),
            Option("quasar_quinn", "Quasar Quinn", "A bright alien child", "☀️", sort_order=7),
            Option("meteor_mike", "Meteor Mike", "A fast-flying alien", "☄️", sort_order=8),
            Option("galaxy_grace", "Galaxy Grace", "A cosmic dancer", "🌌", sort_order=9),
            Option("orbit_olive", "Orbit Olive", "A tiny green explorer", "🪐", sort_order=10),
            Option("starlight_sam", "Starlight Sam", "A bright-eyed visitor", "⭐", sort_order=11),
            Option("comet_carl", "Comet Carl", "A speedy space friend", "☄️", sort_order=12),
        ]
    )
    
    STORY_DISCOVERIES = OptionGroup(
        name="story_discoveries",
        label="Discoveries",
        description="Amazing things to discover",
        icon="🔍",
        sort_order=59,
        options=[
            Option("an_amazing_discovery", "An Amazing Discovery", "Something wonderful found", "🔍", sort_order=1),
            Option("hidden_treasure", "Hidden Treasure", "Gold tucked away", "💰", sort_order=2),
            Option("secret_garden", "Secret Garden", "A hidden flower paradise", "🌷", sort_order=3),
            Option("ancient_artifact", "Ancient Artifact", "A relic from long ago", "🏺", sort_order=4),
            Option("new_planet", "New Planet", "A world no one knew", "🪐", sort_order=5),
            Option("magic_stone", "Magic Stone", "A gem with power", "💎", sort_order=6),
            Option("lost_tribe", "Lost Tribe", "A hidden community", "👥", sort_order=7),
            Option("forgotten_spell", "Forgotten Spell", "Magic remembered again", "📜", sort_order=8),
        ]
    )
    
    STORY_FUNNY_FRIENDS = OptionGroup(
        name="story_funny_friends",
        label="Funny Friends",
        description="Silly and humorous characters",
        icon="🐰",
        sort_order=60,
        options=[
            Option("benny_the_bunny", "Benny the Bunny", "A hopping joker", "🐰", sort_order=1),
            Option("chuckles_chipmunk", "Chuckles Chipmunk", "A nut-cracking comedian", "🐿️", sort_order=2),
            Option("giggles_gorilla", "Giggles Gorilla", "A laughing big buddy", "🦍", sort_order=3),
            Option("wacky_walrus", "Wacky Walrus", "A sliding funny friend", "🐬", sort_order=4),
            Option("silly_sloth", "Silly Sloth", "A slow-motion comedian", "🦥", sort_order=5),
            Option("punny_penguin", "Punny Penguin", "A joke-telling bird", "🐧", sort_order=6),
            Option("jokey_jaguar", "Jokey Jaguar", "A spotted prankster", "🐆", sort_order=7),
            Option("dizzy_donkey", "Dizzy Donkey", "A bouncing buddy", "🫏", sort_order=8),
            Option("goofy_goat", "Goofy Goat", "A climbing comedian", "🐐", sort_order=9),
            Option("bubble_frog", "Bubble Frog", "A ribbiting funny friend", "🐸", sort_order=10),
            Option("zany_zebra", "Zany Zebra", "A striped silly pal", "🦓", sort_order=11),
            Option("loopy_lemur", "Loopy Lemur", "A tail-swinging buddy", "🐒", sort_order=12),
        ]
    )
    
    STORY_ENDINGS = OptionGroup(
        name="story_endings",
        label="Story Endings",
        description="How stories can end",
        icon="🏁",
        sort_order=61,
        options=[
            Option("ending_happy", "Happy Ending", "Everything works out", "😊", sort_order=1),
            Option("ending_emotional", "Emotional Ending", "A touching conclusion", "🥹", sort_order=2),
            Option("ending_funny", "Funny Ending", "A humorous wrap-up", "😂", sort_order=3),
            Option("ending_surprise", "Surprise Ending", "An unexpected twist", "😲", sort_order=4),
            Option("ending_open", "Open Ending", "Left to imagination", "💭", sort_order=5),
            Option("ending_inspirational", "Inspirational Ending", "A motivating finish", "🌟", sort_order=6),
            Option("ending_friendship", "Friendship Ending", "Bonds strengthened", "🤝", sort_order=7),
            Option("ending_adventure", "Adventure Ending", "A new journey begins", "🗺️", sort_order=8),
        ]
    )
    
    STORY_DETECTIVES = OptionGroup(
        name="story_detectives",
        label="Detectives",
        description="Kid-friendly detective characters",
        icon="🕵️",
        sort_order=62,
        options=[
            Option("detective_daisy", "Detective Daisy", "A sharp-eyed sleuth", "🕵️", sort_order=1),
            Option("inspector_whiskers", "Inspector Whiskers", "A cat detective", "🐱", sort_order=2),
            Option("sherlock_shorts", "Sherlock Shorts", "A young genius detective", "🧐", sort_order=3),
            Option("agent_apple", "Agent Apple", "A fruity spy", "🍎", sort_order=4),
            Option("detective_doodle", "Detective Doodle", "A drawing-solving detective", "✏️", sort_order=5),
            Option("chief_chip", "Chief Chip", "A squirrel investigator", "🐿️", sort_order=6),
            Option("mystery_mia", "Mystery Mia", "A puzzle-loving detective", "🔍", sort_order=7),
            Option("clue_catcher", "Clue Catcher", "A net-wielding sleuth", "🕸️", sort_order=8),
            Option("private_pepper", "Private Pepper", "A spicy investigator", "🌶️", sort_order=9),
            Option("gumshoe_gus", "Gumshoe Gus", "A shoe-string detective", "👞", sort_order=10),
            Option("spy_squirrel", "Spy Squirrel", "A nut-nabbing agent", "🐿️", sort_order=11),
            Option("sleuth_sam", "Sleuth Sam", "A methodical finder", "🔎", sort_order=12),
        ]
    )
    
    STORY_ASSISTANTS = OptionGroup(
        name="story_assistants",
        label="Detective Assistants",
        description="Helpers for detective stories",
        icon="👮",
        sort_order=63,
        options=[
            Option("officer_ollie", "Officer Ollie", "A helpful police helper", "👮", sort_order=1),
            Option("sergeant_paws", "Sergeant Paws", "A dog deputy", "🐕", sort_order=2),
            Option("detective_dot", "Detective Dot", "A small but smart helper", "🔘", sort_order=3),
            Option("agent_arrow", "Agent Arrow", "A sharp-shooting aide", "🏹", sort_order=4),
            Option("clue_cat", "Clue Cat", "A curious cat assistant", "🐱", sort_order=5),
            Option("helper_henry", "Helper Henry", "A reliable sidekick", "🤝", sort_order=6),
            Option("tech_tina", "Tech Tina", "A gadget expert", "💻", sort_order=7),
            Option("map_mia", "Map Mia", "A direction-finder", "🗺️", sort_order=8),
            Option("note_ned", "Note Ned", "A writing recorder", "📝", sort_order=9),
            Option("lens_larry", "Lens Larry", "A photo-taker aide", "📸", sort_order=10),
            Option("badge_benny", "Badge Benny", "A badge-wearing helper", "🏅", sort_order=11),
            Option("radio_rita", "Radio Rita", "A communicator operator", "📻", sort_order=12),
        ]
    )
    
    # ============================================================
    # VIDEO DURATIONS
    # ============================================================
    VIDEO_DURATIONS = OptionGroup(
        name="video_durations",
        label="Video Durations",
        description="Standard video length options",
        icon="⏱️",
        sort_order=26,
        options=[
            Option("5s", "5 Seconds", "Micro content", "⚡", sort_order=1),
            Option("15s", "15 Seconds", "Reels/Shorts/TikTok", "📱", sort_order=2),
            Option("30s", "30 Seconds", "Standard short", "📱", sort_order=3),
            Option("60s", "60 Seconds", "Long short-form", "📱", sort_order=4),
            Option("90s", "90 Seconds", "Extended short", "📱", sort_order=5),
            Option("2m", "2 Minutes", "Standard video", "📺", sort_order=6),
            Option("5m", "5 Minutes", "Short educational", "📺", sort_order=7),
            Option("10m", "10 Minutes", "Standard YouTube", "📺", sort_order=8),
            Option("15m", "15 Minutes", "Deep dive", "📺", sort_order=9),
            Option("30m", "30 Minutes", "TV episode", "📺", sort_order=10),
            Option("60m", "60 Minutes", "Full episode", "📺", sort_order=11),
        ]
    )
    
    # ============================================================
    # FPS OPTIONS
    # ============================================================
    FPS_OPTIONS = OptionGroup(
        name="fps_options",
        label="Frame Rates",
        description="Video frame rate options",
        icon="🎞️",
        sort_order=27,
        options=[
            Option("12", "12 FPS", "Animation standard", "🎬", sort_order=1),
            Option("15", "15 FPS", "Low motion", "🎬", sort_order=2),
            Option("24", "24 FPS", "Cinematic film", "🎬", sort_order=3),
            Option("25", "25 FPS", "PAL broadcast", "📺", sort_order=4),
            Option("30", "30 FPS", "NTSC broadcast", "📺", sort_order=5),
            Option("48", "48 FPS", "High frame rate film", "🎬", sort_order=6),
            Option("60", "60 FPS", "Smooth motion", "🎮", sort_order=7),
            Option("120", "120 FPS", "Slow motion capture", "🎮", sort_order=8),
        ]
    )
    
    # ============================================================
    # TRANSITIONS
    # ============================================================
    TRANSITIONS = OptionGroup(
        name="transitions",
        label="Transitions",
        description="Video transition effects",
        icon="✂️",
        sort_order=28,
        options=[
            Option("cut", "Hard Cut", "Instant switch", "✂️", sort_order=1),
            Option("fade", "Fade", "Dissolve to/from black", "🌑", sort_order=2),
            Option("crossfade", "Crossfade", "Blend between clips", "🔀", sort_order=3),
            Option("wipe", "Wipe", "Directional reveal", "🧹", sort_order=4),
            Option("slide", "Slide", "Pan transition", "➡️", sort_order=5),
            Option("zoom", "Zoom", "Scale transition", "🔍", sort_order=6),
            Option("spin", "Spin", "Rotation transition", "🔄", sort_order=7),
            Option("flip", "Flip", "3D card flip", "🔄", sort_order=8),
            Option("morph", "Morph", "Shape transformation", "🦋", sort_order=9),
            Option("glitch", "Glitch", "Digital distortion", "📺", sort_order=10),
            Option("burn", "Film Burn", "Light leak transition", "🔥", sort_order=11),
            Option("whip", "Whip Pan", "Fast blur pan", "💨", sort_order=12),
        ]
    )
    
    # ============================================================
    # CAMERA MOVEMENTS
    # ============================================================
    CAMERA_MOVEMENTS = OptionGroup(
        name="camera_movements",
        label="Camera Movements",
        description="Cinematic camera movements",
        icon="🎥",
        sort_order=29,
        options=[
            Option("static", "Static/Locked", "No movement", "📷", sort_order=1),
            Option("pan", "Pan", "Horizontal rotation", "➡️", sort_order=2),
            Option("tilt", "Tilt", "Vertical rotation", "⬆️", sort_order=3),
            Option("dolly", "Dolly", "Forward/backward track", "🚂", sort_order=4),
            Option("truck", "Truck/Pedestal", "Left/right track", "🚛", sort_order=5),
            Option("crane", "Crane/Jib", "Vertical lift", "🏗️", sort_order=6),
            Option("drone", "Drone/Aerial", "Flying camera", "🚁", sort_order=7),
            Option("handheld", "Handheld", "Organic shake", "📹", sort_order=8),
            Option("steadicam", "Steadicam", "Smooth tracking", "🎥", sort_order=9),
            Option("gimbal", "Gimbal", "Motorized stabilization", "🤖", sort_order=10),
            Option("zoom", "Zoom", "Optical focal length", "🔍", sort_order=11),
            Option("focus_pull", "Focus Pull", "Rack focus", "👁️", sort_order=12),
            Option("orbit", "Orbit", "Circle around subject", "🔄", sort_order=13),
            Option("parallax", "Parallax", "Layered depth motion", "🌌", sort_order=14),
        ]
    )
    
    # ============================================================
    # MUSIC STYLES
    # ============================================================
    MUSIC_STYLES = OptionGroup(
        name="music_styles",
        label="Music Styles",
        description="Background music genres",
        icon="🎵",
        sort_order=30,
        options=[
            Option("orchestral", "Orchestral", "Full symphony", "🎻", sort_order=1),
            Option("piano", "Piano", "Solo or accompanied", "🎹", sort_order=2),
            Option("acoustic", "Acoustic", "Guitar/folk", "🎸", sort_order=3),
            Option("electronic", "Electronic", "Synth/EDM", "🎹", sort_order=4),
            Option("ambient", "Ambient", "Atmospheric texture", "☁️", sort_order=5),
            Option("cinematic", "Cinematic", "Film score style", "🎬", sort_order=6),
            Option("corporate", "Corporate", "Upbeat business", "💼", sort_order=7),
            Option("kids", "Kids/Playful", "Child-friendly", "🎈", sort_order=8),
            Option("lofi", "Lo-Fi", "Chill beats", "🎧", sort_order=9),
            Option("jazz", "Jazz", "Swing/bebop", "🎷", sort_order=10),
            Option("classical", "Classical", "Period compositions", "🎻", sort_order=11),
            Option("rock", "Rock", "Guitar-driven", "🎸", sort_order=12),
            Option("pop", "Pop", "Mainstream catchy", "🎤", sort_order=13),
            Option("hip_hop", "Hip Hop", "Beats and flow", "🎤", sort_order=14),
            Option("folk", "Folk", "Traditional acoustic", "🪕", sort_order=15),
            Option("world", "World", "Cultural traditions", "🌍", sort_order=16),
            Option("meditation", "Meditation", "Healing frequencies", "🧘", sort_order=17),
            Option("epic", "Epic/Trailer", "Big dramatic", "🎬", sort_order=18),
            Option("horror", "Horror/Suspense", "Tension building", "👻", sort_order=19),
            Option("comedy", "Comedy", "Light and funny", "😂", sort_order=20),
        ]
    )
    
    # ============================================================
    # VOICE STYLES
    # ============================================================
    VOICE_STYLES = OptionGroup(
        name="voice_styles",
        label="Voice Styles",
        description="Speaking styles for voice generation",
        icon="🎙️",
        sort_order=31,
        options=[
            Option("conversational", "Conversational", "Natural chat", "💬", sort_order=1),
            Option("narrator", "Narrator", "Storytelling voice", "📖", sort_order=2),
            Option("announcer", "Announcer", "Broadcast style", "📢", sort_order=3),
            Option("teacher", "Teacher", "Educational clear", "👩‍🏫", sort_order=4),
            Option("coach", "Coach", "Motivational", "🏋️", sort_order=5),
            Option("friend", "Friend", "Casual buddy", "🤝", sort_order=6),
            Option("parent", "Parent", "Nurturing guide", "👨‍👩‍👧", sort_order=7),
            Option("expert", "Expert", "Authoritative", "🎓", sort_order=8),
            Option("character", "Character", "In-role performance", "🎭", sort_order=9),
            Option("meditation", "Meditation", "Slow and soothing", "🧘", sort_order=10),
            Option("as_m_r", "ASMR", "Tingling triggers", "👂", sort_order=11),
            Option("whisper", "Whisper", "Intimate quiet", "🤫", sort_order=12),
            Option("energetic", "Energetic", "High enthusiasm", "⚡", sort_order=13),
            Option("calm", "Calm", "Steady and measured", "😌", sort_order=14),
            Option("dramatic", "Dramatic", "Theatrical", "🎭", sort_order=15),
            Option("monotone", "Monotone", "Flat affect", "😐", sort_order=16),
            Option("robotic", "Robotic", "Synthetic", "🤖", sort_order=17),
            Option("alien", "Alien", "Otherworldly", "👽", sort_order=18),
            Option("monster", "Monster", "Creature voice", "👹", sort_order=19),
            Option("fairy", "Fairy", "Magical light", "🧚", sort_order=20),
        ]
    )
    
    # ============================================================
    # NARRATION STYLES
    # ============================================================
    NARRATION_STYLES = OptionGroup(
        name="narration_styles",
        label="Narration Styles",
        description="Types of narration for stories",
        icon="📖",
        sort_order=32,
        options=[
            Option("single_narrator", "Single Narrator", "One voice throughout", "🎙️", sort_order=1),
            Option("full_cast", "Full Cast", "Multiple voice actors", "🎭", sort_order=2),
            Option("dual_narrator", "Dual Narrator", "Two perspectives", "👥", sort_order=3),
            Option("author_narrated", "Author Narrated", "Writer reads own work", "✍️", sort_order=4),
            Option("character_pov", "Character POV", "First-person character", "👁️", sort_order=5),
            Option("documentary", "Documentary Style", "Informative narrator", "📺", sort_order=6),
            Option("dramatized", "Dramatized", "Sound effects + voices", "🎬", sort_order=7),
            Option("read_along", "Read-Along", "Page-turn signals", "📖", sort_order=8),
            Option("interactive", "Interactive", "Choose your path", "🎮", sort_order=9),
            Option("musical", "Musical Narration", "Songs integrated", "🎵", sort_order=10),
        ]
    )
    
    # ============================================================
    # LEARNING LEVELS
    # ============================================================
    LEARNING_LEVELS = OptionGroup(
        name="learning_levels",
        label="Learning Levels",
        description="Educational difficulty levels",
        icon="📚",
        sort_order=33,
        options=[
            Option("beginner", "Beginner", "Just starting out", "🌱", sort_order=1),
            Option("elementary", "Elementary", "Basic foundations", "🏫", sort_order=2),
            Option("intermediate", "Intermediate", "Building skills", "📈", sort_order=3),
            Option("advanced", "Advanced", "Complex concepts", "🎓", sort_order=4),
            Option("expert", "Expert", "Mastery level", "🏆", sort_order=5),
        ]
    )
    
    # ============================================================
    # WORKSHEET TYPES
    # ============================================================
    WORKSHEET_TYPES = OptionGroup(
        name="worksheet_types",
        label="Worksheet Types",
        description="Types of educational worksheets",
        icon="📝",
        sort_order=34,
        options=[
            Option("tracing", "Tracing", "Letter/number tracing", "✏️", sort_order=1),
            Option("matching", "Matching", "Connect related items", "🔗", sort_order=2),
            Option("coloring", "Coloring", "Color by number/letter", "🎨", sort_order=3),
            Option("counting", "Counting", "Number practice", "🔢", sort_order=4),
            Option("writing", "Writing Practice", "Handwriting sheets", "✍️", sort_order=5),
            Option("puzzle", "Puzzle", "Maze/crossword/word search", "🧩", sort_order=6),
            Option("cutting", "Cutting Practice", "Scissor skills", "✂️", sort_order=7),
            Option("sorting", "Sorting", "Categorize items", "📦", sort_order=8),
            Option("pattern", "Patterns", "Complete the sequence", "🔄", sort_order=9),
            Option("math", "Math Problems", "Arithmetic practice", "➕", sort_order=10),
        ]
    )
    
    # ============================================================
    # QUIZ TYPES
    # ============================================================
    QUIZ_TYPES = OptionGroup(
        name="quiz_types",
        label="Quiz Types",
        description="Quiz formats for education",
        icon="❓",
        sort_order=35,
        options=[
            Option("multiple_choice", "Multiple Choice", "Select from options", "☑️", sort_order=1),
            Option("true_false", "True/False", "Binary choice", "✅❌", sort_order=2),
            Option("fill_blank", "Fill in the Blank", "Complete the sentence", "⬜", sort_order=3),
            Option("matching", "Matching", "Pair items", "🔗", sort_order=4),
            Option("ordering", "Ordering", "Sequence items", "1️⃣2️⃣3️⃣", sort_order=5),
            Option("short_answer", "Short Answer", "Write response", "✏️", sort_order=6),
            Option("picture", "Picture Quiz", "Visual identification", "🖼️", sort_order=7),
            Option("audio", "Audio Quiz", "Listening comprehension", "🔊", sort_order=8),
        ]
    )
    
    # ============================================================
    # REWARD TYPES
    # ============================================================
    REWARD_TYPES = OptionGroup(
        name="reward_types",
        label="Reward Types",
        description="Rewards for educational completion",
        icon="🏆",
        sort_order=36,
        options=[
            Option("sticker", "Sticker", "Digital sticker", "🏷️", sort_order=1),
            Option("badge", "Badge", "Achievement badge", "🏅", sort_order=2),
            Option("certificate", "Certificate", "Completion certificate", "📜", sort_order=3),
            Option("trophy", "Trophy", "Winner's trophy", "🏆", sort_order=4),
            Option("medal", "Medal", "Gold/silver/bronze", "🥇", sort_order=5),
            Option("stars", "Stars", "Star rating", "⭐", sort_order=6),
            Option("points", "Points", "Score points", "💯", sort_order=7),
            Option("coins", "Coins", "Virtual currency", "🪙", sort_order=8),
            Option("unlock", "Unlock Content", "New level/character", "🔓", sort_order=9),
            Option("celebration", "Celebration", "Confetti/animation", "🎉", sort_order=10),
        ]
    )
    
    # ============================================================
    # ALPHABET STYLES
    # ============================================================
    ALPHABET_STYLES = OptionGroup(
        name="alphabet_styles",
        label="Alphabet Styles",
        description="Letter presentation styles",
        icon="🔤",
        sort_order=37,
        options=[
            Option("uppercase", "Uppercase (A-Z)", "Capital letters", "🔠", sort_order=1),
            Option("lowercase", "Lowercase (a-z)", "Small letters", "🔡", sort_order=2),
            Option("both", "Both Cases (Aa-Zz)", "Upper and lower", "🔠🔡", sort_order=3),
            Option("cursive", "Cursive", "Connected script", "✍️", sort_order=4),
            Option("print", "Print/Manuscript", "Standard block letters", "🔤", sort_order=5),
            Option("phonetic", "Phonetic", "With sound guides", "🔊", sort_order=6),
            Option("sign_language", "Sign Language (ASL)", "Hand signs", "🤟", sort_order=7),
            Option("braille", "Braille", "Tactile dots", "⠃⠗⠁⠊⠇⠇⠑", sort_order=8),
        ]
    )
    
    # ============================================================
    # CURRICULUM STANDARDS
    # ============================================================
    CURRICULUM_STANDARDS = OptionGroup(
        name="curriculum_standards",
        label="Curriculum Standards",
        description="Educational curriculum frameworks",
        icon="📋",
        sort_order=38,
        options=[
            Option("common_core", "Common Core (US)", "US national standards", "🇺🇸", sort_order=1),
            Option("ngss", "NGSS (Science)", "Next Gen Science Standards", "🔬", sort_order=2),
            Option("eyfs", "EYFS (UK)", "Early Years Foundation Stage", "🇬🇧", sort_order=3),
            Option("national_curriculum_uk", "National Curriculum UK", "UK standards", "🇬🇧", sort_order=4),
            Option("australian", "Australian Curriculum", "Australia standards", "🇦🇺", sort_order=5),
            Option("canadian", "Canadian Curriculum", "Provincial standards", "🇨🇦", sort_order=6),
            Option("ib_pyp", "IB PYP", "International Baccalaureate Primary", "🌍", sort_order=7),
            Option("montessori", "Montessori", "Child-led learning", "🏫", sort_order=8),
            Option("waldorf", "Waldorf/Steiner", "Holistic development", "🌳", sort_order=9),
            Option("reggio", "Reggio Emilia", "Project-based", "🎨", sort_order=10),
            Option("custom", "Custom/Homeschool", "Personalized curriculum", "🏠", sort_order=11),
        ]
    )
    
    # ============================================================
    # READING LEVELS
    # ============================================================
    READING_LEVELS = OptionGroup(
        name="reading_levels",
        label="Reading Levels",
        description="Reading difficulty levels",
        icon="📖",
        sort_order=39,
        options=[
            Option("pre_reading", "Pre-Reading", "Letters and sounds", "🔤", sort_order=1),
            Option("emergent", "Emergent Reader", "Simple words/sentences", "📖", sort_order=2),
            Option("early", "Early Reader", "Short books, repetition", "📚", sort_order=3),
            Option("transitional", "Transitional Reader", "Chapter books beginning", "📚", sort_order=4),
            Option("fluent", "Fluent Reader", "Independent reading", "📚📚", sort_order=5),
            Option("advanced", "Advanced Reader", "Complex texts", "📚📚📚", sort_order=6),
        ]
    )
    
    # ============================================================
    # BODY PARTS
    # ============================================================
    BODY_PARTS = OptionGroup(
        name="body_parts",
        label="Body Parts",
        description="Human body parts for education",
        icon="👋",
        sort_order=40,
        options=[
            Option("head", "Head", "Top of body", "👤", sort_order=1),
            Option("face", "Face", "Front of head", "😊", sort_order=2),
            Option("eyes", "Eyes", "Seeing organs", "👁️", sort_order=3),
            Option("ears", "Ears", "Hearing organs", "👂", sort_order=4),
            Option("nose", "Nose", "Smelling organ", "👃", sort_order=5),
            Option("mouth", "Mouth", "Eating/speaking", "👄", sort_order=6),
            Option("teeth", "Teeth", "Chewing tools", "🦷", sort_order=7),
            Option("hair", "Hair", "Head covering", "💇", sort_order=8),
            Option("neck", "Neck", "Head connector", "🦒", sort_order=9),
            Option("shoulders", "Shoulders", "Arm connectors", "💪", sort_order=10),
            Option("arms", "Arms", "Upper limbs", "💪", sort_order=11),
            Option("elbows", "Elbows", "Arm joints", "💪", sort_order=12),
            Option("hands", "Hands", "Grasping tools", "✋", sort_order=13),
            Option("fingers", "Fingers", "Digits", "☝️", sort_order=14),
            Option("chest", "Chest", "Upper torso", "🫁", sort_order=15),
            Option("stomach", "Stomach", "Digestion", "🍽️", sort_order=16),
            Option("back", "Back", "Spine area", "🔙", sort_order=17),
            Option("hips", "Hips", "Pelvis", "🦴", sort_order=18),
            Option("legs", "Legs", "Lower limbs", "🦵", sort_order=19),
            Option("knees", "Knees", "Leg joints", "🦵", sort_order=20),
            Option("feet", "Feet", "Walking base", "🦶", sort_order=21),
            Option("toes", "Toes", "Foot digits", "🦶", sort_order=22),
        ]
    )
    
    # ============================================================
    # WEATHER CONDITIONS
    # ============================================================
    WEATHER_CONDITIONS = OptionGroup(
        name="weather_conditions",
        label="Weather Conditions",
        description="Weather types for educational content",
        icon="🌤️",
        sort_order=41,
        options=[
            Option("sunny", "Sunny", "Clear bright skies", "☀️", sort_order=1),
            Option("cloudy", "Cloudy", "Overcast", "☁️", sort_order=2),
            Option("partly_cloudy", "Partly Cloudy", "Sun and clouds", "⛅", sort_order=3),
            Option("rainy", "Rainy", "Precipitation", "🌧️", sort_order=4),
            Option("stormy", "Stormy", "Thunder and lightning", "⛈️", sort_order=5),
            Option("snowy", "Snowy", "Snow falling", "❄️", sort_order=6),
            Option("foggy", "Foggy", "Low visibility", "🌫️", sort_order=7),
            Option("windy", "Windy", "Strong air movement", "💨", sort_order=8),
            Option("hot", "Hot", "High temperature", "🔥", sort_order=9),
            Option("cold", "Cold", "Low temperature", "🧊", sort_order=10),
            Option("humid", "Humid", "Moist air", "💦", sort_order=11),
            Option("rainbow", "Rainbow", "After rain colors", "🌈", sort_order=12),
        ]
    )
    
    # ============================================================
    # SEASONS
    # ============================================================
    SEASONS = OptionGroup(
        name="seasons",
        label="Seasons",
        description="Four seasons plus regional variations",
        icon="🌍",
        sort_order=42,
        options=[
            Option("spring", "Spring", "March-May (North)", "🌱", sort_order=1),
            Option("summer", "Summer", "June-August (North)", "☀️", sort_order=2),
            Option("autumn", "Autumn/Fall", "September-November (North)", "🍂", sort_order=3),
            Option("winter", "Winter", "December-February (North)", "❄️", sort_order=4),
            Option("rainy", "Rainy/Monsoon", "Tropical wet season", "🌧️", sort_order=5),
            Option("dry", "Dry Season", "Tropical dry season", "☀️", sort_order=6),
        ]
    )
    
    # ============================================================
    # MONTHS
    # ============================================================
    MONTHS = OptionGroup(
        name="months",
        label="Months",
        description="Months of the year",
        icon="📅",
        sort_order=43,
        options=[
            Option("january", "January", "First month", "❄️", sort_order=1),
            Option("february", "February", "Second month", "❤️", sort_order=2),
            Option("march", "March", "Third month", "🌱", sort_order=3),
            Option("april", "April", "Fourth month", "🌧️", sort_order=4),
            Option("may", "May", "Fifth month", "🌸", sort_order=5),
            Option("june", "June", "Sixth month", "☀️", sort_order=6),
            Option("july", "July", "Seventh month", "🇺🇸", sort_order=7),
            Option("august", "August", "Eighth month", "🏖️", sort_order=8),
            Option("september", "September", "Ninth month", "🍂", sort_order=9),
            Option("october", "October", "Tenth month", "🎃", sort_order=10),
            Option("november", "November", "Eleventh month", "🦃", sort_order=11),
            Option("december", "December", "Twelfth month", "🎄", sort_order=12),
        ]
    )
    
    # ============================================================
    # DAYS OF WEEK
    # ============================================================
    DAYS_OF_WEEK = OptionGroup(
        name="days_of_week",
        label="Days of the Week",
        description="Seven days",
        icon="📅",
        sort_order=44,
        options=[
            Option("monday", "Monday", "Week start (ISO)", "1️⃣", sort_order=1),
            Option("tuesday", "Tuesday", "Second day", "2️⃣", sort_order=2),
            Option("wednesday", "Wednesday", "Hump day", "3️⃣", sort_order=3),
            Option("thursday", "Thursday", "Fourth day", "4️⃣", sort_order=4),
            Option("friday", "Friday", "Week end", "5️⃣", sort_order=5),
            Option("saturday", "Saturday", "Weekend", "6️⃣", sort_order=6),
            Option("sunday", "Sunday", "Week end (US)", "7️⃣", sort_order=7),
        ]
    )
    
    # ============================================================
    # SHAPES
    # ============================================================
    SHAPES = OptionGroup(
        name="shapes",
        label="Shapes",
        description="Geometric shapes for education",
        icon="🔷",
        sort_order=45,
        options=[
            Option("circle", "Circle", "Round shape", "⭕", sort_order=1),
            Option("square", "Square", "Four equal sides", "⬜", sort_order=2),
            Option("triangle", "Triangle", "Three sides", "🔺", sort_order=3),
            Option("rectangle", "Rectangle", "Four sides, two pairs", "🟦", sort_order=4),
            Option("oval", "Oval", "Stretched circle", "🥚", sort_order=5),
            Option("diamond", "Diamond/Rhombus", "Tilted square", "💎", sort_order=6),
            Option("pentagon", "Pentagon", "Five sides", "🏠", sort_order=7),
            Option("hexagon", "Hexagon", "Six sides", "🐝", sort_order=8),
            Option("octagon", "Octagon", "Eight sides", "🛑", sort_order=9),
            Option("star", "Star", "Pointed shape", "⭐", sort_order=10),
            Option("heart", "Heart", "Love shape", "❤️", sort_order=11),
            Option("crescent", "Crescent", "Moon shape", "🌙", sort_order=12),
            Option("semi_circle", "Semi-circle", "Half circle", "🌗", sort_order=13),
            Option("trapezoid", "Trapezoid", "One parallel pair", "📐", sort_order=14),
            Option("parallelogram", "Parallelogram", "Opposite parallel", "📐", sort_order=15),
        ]
    )
    
    # ============================================================
    # PLANETS
    # ============================================================
    PLANETS = OptionGroup(
        name="planets",
        label="Planets",
        description="Solar system planets",
        icon="🪐",
        sort_order=46,
        options=[
            Option("mercury", "Mercury", "Closest to Sun", "☿️", sort_order=1),
            Option("venus", "Venus", "Hottest planet", "♀️", sort_order=2),
            Option("earth", "Earth", "Our home", "🌍", sort_order=3),
            Option("mars", "Mars", "Red planet", "♂️", sort_order=4),
            Option("jupiter", "Jupiter", "Largest planet", "🪐", sort_order=5),
            Option("saturn", "Saturn", "Ringed planet", "🪐", sort_order=6),
            Option("uranus", "Uranus", "Sideways planet", "🪐", sort_order=7),
            Option("neptune", "Neptune", "Windiest planet", "🪐", sort_order=8),
            Option("pluto", "Pluto", "Dwarf planet", "🪨", sort_order=9),
            Option("sun", "Sun", "Our star", "☀️", sort_order=10),
            Option("moon", "Moon", "Earth's satellite", "🌙", sort_order=11),
        ]
    )
    
    # ============================================================
    # CONTINENTS
    # ============================================================
    CONTINENTS = OptionGroup(
        name="continents",
        label="Continents",
        description="World continents",
        icon="🌍",
        sort_order=47,
        options=[
            Option("africa", "Africa", "54 countries", "🌍", sort_order=1),
            Option("antarctica", "Antarctica", "Frozen continent", "🇦🇶", sort_order=2),
            Option("asia", "Asia", "Largest continent", "🌏", sort_order=3),
            Option("europe", "Europe", "44 countries", "🇪🇺", sort_order=4),
            Option("north_america", "North America", "23 countries", "🌎", sort_order=5),
            Option("south_america", "South America", "12 countries", "🌎", sort_order=6),
            Option("oceania", "Oceania", "14 countries", "🌏", sort_order=7),
        ]
    )
    
    # ============================================================
    # HABITATS (30+)
    # ============================================================
    HABITATS = OptionGroup(
        name="habitats",
        label="Habitats",
        description="Animal habitats and ecosystems",
        icon="🏞️",
        sort_order=48,
        options=[
            Option("forest", "Forest", "Tree-covered land", "🌳", sort_order=1),
            Option("rainforest", "Rainforest", "Tropical dense forest", "🌴", sort_order=2),
            Option("desert", "Desert", "Arid dry land", "🏜️", sort_order=3),
            Option("ocean", "Ocean", "Salt water", "🌊", sort_order=4),
            Option("freshwater", "Freshwater", "Rivers/lakes", "🏞️", sort_order=5),
            Option("grassland", "Grassland/Savanna", "Open plains", "🌾", sort_order=6),
            Option("tundra", "Tundra", "Frozen treeless", "❄️", sort_order=7),
            Option("mountain", "Mountain", "High elevation", "⛰️", sort_order=8),
            Option("wetland", "Wetland", "Marshy land", "🐊", sort_order=9),
            Option("coral_reef", "Coral Reef", "Underwater city", "🐠", sort_order=10),
            Option("arctic", "Arctic", "North pole region", "🧊", sort_order=11),
            Option("antarctic", "Antarctic", "South pole region", "🧊", sort_order=12),
            Option("urban", "Urban", "City environment", "🏙️", sort_order=13),
            Option("farm", "Farm", "Agricultural land", "🚜", sort_order=14),
            Option("jungle", "Jungle", "Dense tropical forest", "🌿", sort_order=15),
            Option("savannah", "Savannah", "African grasslands", "🌾", sort_order=16),
            Option("taiga", "Taiga", "Boreal forest", "🌲", sort_order=17),
            Option("chaparral", "Chaparral", "Mediterranean shrubland", "🌿", sort_order=18),
            Option("alpine", "Alpine", "High mountain", "🏔️", sort_order=19),
            Option("estuary", "Estuary", "River meets sea", "🌊", sort_order=20),
            Option("mangrove", "Mangrove", "Coastal tidal forest", "🌿", sort_order=21),
            Option("kelp_forest", "Kelp Forest", "Underwater forest", "🌊", sort_order=22),
            Option("deep_sea", "Deep Sea", "Ocean depths", "🌊", sort_order=23),
            Option("cave", "Cave", "Underground cavern", "🕳️", sort_order=24),
            Option("pond", "Pond", "Small freshwater body", "🏞️", sort_order=25),
            Option("stream", "Stream", "Flowing freshwater", "🏞️", sort_order=26),
            Option("lake", "Lake", "Large freshwater body", "🏞️", sort_order=27),
            Option("river", "River", "Major waterway", "🏞️", sort_order=28),
            Option("beach", "Beach", "Sandy shore", "🏖️", sort_order=29),
            Option("dunes", "Sand Dunes", "Wind-shaped sand", "🏜️", sort_order=30),
            Option("cliff", "Cliff", "Steep rock face", "🏔️", sort_order=31),
            Option("island", "Island", "Land in water", "🏝️", sort_order=32),
        ]
    )
    
    # ============================================================
    # TRANSPORT TYPES
    # ============================================================
    TRANSPORT_TYPES = OptionGroup(
        name="transport_types",
        label="Transport Types",
        description="Categories of transportation",
        icon="🚌",
        sort_order=49,
        options=[
            Option("land", "Land", "Road/rail vehicles", "🛣️", sort_order=1),
            Option("air", "Air", "Aircraft", "✈️", sort_order=2),
            Option("water", "Water", "Boats/ships", "🚢", sort_order=3),
            Option("space", "Space", "Rockets/satellites", "🚀", sort_order=4),
            Option("pipeline", "Pipeline", "Fluid transport", "🛢️", sort_order=5),
            Option("cable", "Cable", "Gondolas/cable cars", "🚠", sort_order=6),
        ]
    )
    
    # ============================================================
    # RENDER ENGINES
    # ============================================================
    RENDER_ENGINES = OptionGroup(
        name="render_engines",
        label="Render Engines",
        description="3D rendering engines",
        icon="🎮",
        sort_order=50,
        options=[
            Option("cycles", "Cycles (Blender)", "Path tracer", "🎨", sort_order=1),
            Option("eevee", "Eevee (Blender)", "Real-time", "⚡", sort_order=2),
            Option("octane", "Octane Render", "GPU biased", "🚀", sort_order=3),
            Option("redshift", "Redshift", "GPU biased", "🔴", sort_order=4),
            Option("arnold", "Arnold", "Production path tracer", "🎬", sort_order=5),
            Option("vray", "V-Ray", "Hybrid renderer", "🎨", sort_order=6),
            Option("corona", "Corona Renderer", "Unbiased", "👑", sort_order=7),
            Option("unreal", "Unreal Engine", "Real-time game engine", "🎮", sort_order=8),
            Option("unity", "Unity HDRP", "Real-time game engine", "🎮", sort_order=9),
            Option("keyshot", "KeyShot", "Real-time ray tracing", "🔑", sort_order=10),
            Option("lumion", "Lumion", "Architectural real-time", "🏗️", sort_order=11),
            Option("twinmotion", "Twinmotion", "ArchViz real-time", "🏗️", sort_order=12),
        ]
    )
    
    # ============================================================
    # TEXTURES
    # ============================================================
    TEXTURES = OptionGroup(
        name="textures",
        label="Textures",
        description="Surface texture types",
        icon="🧱",
        sort_order=51,
        options=[
            Option("smooth", "Smooth", "Glossy flat", "🪞", sort_order=1),
            Option("rough", "Rough", "Matte uneven", "🪨", sort_order=2),
            Option("metallic", "Metallic", "Metal surface", "🤖", sort_order=3),
            Option("glass", "Glass", "Transparent refractive", "🔍", sort_order=4),
            Option("plastic", "Plastic", "Synthetic polymer", "🧱", sort_order=5),
            Option("fabric", "Fabric", "Woven cloth", "🧵", sort_order=6),
            Option("leather", "Leather", "Animal hide", "👜", sort_order=7),
            Option("wood", "Wood", "Natural grain", "🪵", sort_order=8),
            Option("stone", "Stone", "Rock surface", "🪨", sort_order=9),
            Option("concrete", "Concrete", "Cement aggregate", "🏗️", sort_order=10),
            Option("brick", "Brick", "Fired clay blocks", "🧱", sort_order=11),
            Option("fur", "Fur", "Animal hair", "🦁", sort_order=12),
            Option("feathers", "Feathers", "Bird plumage", "🦜", sort_order=13),
            Option("scales", "Scales", "Reptile/fish skin", "🐍", sort_order=14),
            Option("skin", "Skin", "Human/organic", "👤", sort_order=15),
            Option("water", "Water", "Liquid surface", "💧", sort_order=16),
            Option("fire", "Fire", "Flames", "🔥", sort_order=17),
            Option("smoke", "Smoke", "Particulate", "💨", sort_order=18),
            Option("clouds", "Clouds", "Atmospheric", "☁️", sort_order=19),
            Option("grass", "Grass", "Vegetation blades", "🌱", sort_order=20),
        ]
    )
    
    # ============================================================
    # COMPOSITION RULES
    # ============================================================
    COMPOSITION_RULES = OptionGroup(
        name="composition_rules",
        label="Composition Rules",
        description="Photographic composition guidelines",
        icon="📐",
        sort_order=52,
        options=[
            Option("rule_of_thirds", "Rule of Thirds", "3x3 grid placement", "📐", sort_order=1),
            Option("golden_ratio", "Golden Ratio", "1.618 spiral", "🌀", sort_order=2),
            Option("centered", "Centered", "Symmetrical balance", "🎯", sort_order=3),
            Option("leading_lines", "Leading Lines", "Lines guide eye", "➡️", sort_order=4),
            Option("framing", "Framing", "Frame within frame", "🖼️", sort_order=5),
            Option("symmetry", "Symmetry", "Mirror balance", "⚖️", sort_order=6),
            Option("asymmetry", "Asymmetry", "Dynamic imbalance", "⚖️", sort_order=7),
            Option("negative_space", "Negative Space", "Empty area focus", "⚪", sort_order=8),
            Option("fill_frame", "Fill the Frame", "Subject dominates", "🔍", sort_order=9),
            Option("layering", "Layering", "Foreground/mid/background", "🏔️", sort_order=10),
            Option("patterns", "Patterns/Repetition", "Repeating elements", "🔄", sort_order=11),
            Option("contrast", "Contrast", "Light/dark/color pop", "🌓", sort_order=12),
        ]
    )
    
    # ============================================================
    # COLOR PALETTES
    # ============================================================
    COLOR_PALETTES = OptionGroup(
        name="color_palettes",
        label="Color Palettes",
        description="Curated color schemes",
        icon="🎨",
        sort_order=53,
        options=[
            Option("warm", "Warm", "Reds, oranges, yellows", "🔥", sort_order=1),
            Option("cool", "Cool", "Blues, greens, purples", "❄️", sort_order=2),
            Option("monochromatic", "Monochromatic", "Single hue variations", "🎨", sort_order=3),
            Option("complementary", "Complementary", "Opposite wheel colors", "🌈", sort_order=4),
            Option("analogous", "Analogous", "Adjacent wheel colors", "🌈", sort_order=5),
            Option("triadic", "Triadic", "Three equidistant colors", "🔺", sort_order=6),
            Option("split_complementary", "Split Complementary", "Base + two adjacent to complement", "🎨", sort_order=7),
            Option("tetradic", "Tetradic", "Two complementary pairs", "🎨", sort_order=8),
            Option("pastel", "Pastel", "Soft muted tones", "🍦", sort_order=9),
            Option("neon", "Neon", "Bright saturated", "🌈", sort_order=10),
            Option("earth", "Earth Tones", "Natural browns/greens", "🌍", sort_order=11),
            Option("jewel", "Jewel Tones", "Rich saturated", "💎", sort_order=12),
            Option("primary", "Primary Colors", "Red, blue, yellow", "🎨", sort_order=13),
            Option("secondary", "Secondary Colors", "Green, orange, purple", "🎨", sort_order=14),
            Option("rainbow", "Rainbow", "Full spectrum", "🌈", sort_order=15),
            Option("black_white", "Black & White", "Monochrome", "⚫⚪", sort_order=16),
            Option("sepia", "Sepia", "Vintage brown", "📜", sort_order=17),
            Option("cyberpunk", "Cyberpunk", "Neon pink/blue", "🌃", sort_order=18),
            Option("vaporwave", "Vaporwave", "Pink/teal/purple", "🌊", sort_order=19),
            Option("autumn", "Autumn", "Orange/red/gold", "🍂", sort_order=20),
        ]
    )
    
    # ============================================================
    # MOODS
    # ============================================================
    MOODS = OptionGroup(
        name="moods",
        label="Moods",
        description="Atmospheric moods for content",
        icon="🌈",
        sort_order=54,
        options=[
            Option("cheerful", "Cheerful", "Bright and happy", "😊", sort_order=1),
            Option("peaceful", "Peaceful", "Calm and serene", "🕊️", sort_order=2),
            Option("magical", "Magical", "Wonder and enchantment", "✨", sort_order=3),
            Option("adventurous", "Adventurous", "Exciting journey", "🗺️", sort_order=4),
            Option("cozy", "Cozy", "Warm and comfortable", "☕", sort_order=5),
            Option("mysterious", "Mysterious", "Intriguing unknown", "🔮", sort_order=6),
            Option("epic", "Epic", "Grand and heroic", "🏔️", sort_order=7),
            Option("whimsical", "Whimsical", "Playfully quaint", "🦄", sort_order=8),
            Option("nostalgic", "Nostalgic", "Sentimental past", "📜", sort_order=9),
            Option("futuristic", "Futuristic", "Advanced tomorrow", "🚀", sort_order=10),
            Option("dark", "Dark", "Gloomy and serious", "🌑", sort_order=11),
            Option("romantic", "Romantic", "Love and passion", "💕", sort_order=12),
            Option("humorous", "Humorous", "Funny and light", "😂", sort_order=13),
            Option("inspiring", "Inspiring", "Motivating", "💫", sort_order=14),
            Option("dreamy", "Dreamy", "Surreal soft", "☁️", sort_order=15),
            Option("energetic", "Energetic", "High energy and active", "⚡", sort_order=16),
            Option("calm", "Calm", "Peaceful and relaxed", "😌", sort_order=17),
            Option("sleepy", "Sleepy", "Tired and drowsy", "😴", sort_order=18),
        ]
    )
    
    # ============================================================
    # EXPRESSIONS
    # ============================================================
    EXPRESSIONS = OptionGroup(
        name="expressions",
        label="Facial Expressions",
        description="Character facial expressions",
        icon="😊",
        sort_order=55,
        options=[
            Option("smile", "Smile", "Happy expression", "😄", sort_order=1),
            Option("laugh", "Laugh", "Joyful open mouth", "😂", sort_order=2),
            Option("wink", "Wink", "Playful one eye", "😉", sort_order=3),
            Option("surprise", "Surprise", "Wide eyes open mouth", "😲", sort_order=4),
            Option("wonder", "Wonder", "Awe and amazement", "🤩", sort_order=5),
            Option("curious", "Curious", "Head tilt questioning", "🤔", sort_order=6),
            Option("thinking", "Thinking", "Contemplative", "💭", sort_order=7),
            Option("sleepy", "Sleepy", "Droopy eyes", "😴", sort_order=8),
            Option("sad", "Sad", "Downcast", "😢", sort_order=9),
            Option("angry", "Angry", "Furious", "😠", sort_order=10),
            Option("scared", "Scared", "Fearful", "😨", sort_order=11),
            Option("confused", "Confused", "Puzzled", "😕", sort_order=12),
            Option("proud", "Proud", "Chest out confident", "😤", sort_order=13),
            Option("shy", "Shy", "Blushing hidden", "😳", sort_order=14),
            Option("cool", "Cool", "Sunglasses swagger", "😎", sort_order=15),
            Option("silly", "Silly", "Goofy face", "🤪", sort_order=16),
            Option("determined", "Determined", "Focused intense", "💪", sort_order=17),
            Option("relaxed", "Relaxed", "Chill content", "😌", sort_order=18),
        ]
    )
    
    # ============================================================
    # HAIR STYLES
    # ============================================================
    HAIR_STYLES = OptionGroup(
        name="hair_styles",
        label="Hair Styles",
        description="Character hair styles",
        icon="💇",
        sort_order=56,
        options=[
            Option("short", "Short", "Above shoulders", "💇", sort_order=1),
            Option("medium", "Medium", "Shoulder length", "💇", sort_order=2),
            Option("long", "Long", "Below shoulders", "💇", sort_order=3),
            Option("very_long", "Very Long", "Waist or longer", "💇", sort_order=4),
            Option("bob", "Bob", "Chin-length blunt", "💇", sort_order=5),
            Option("pixie", "Pixie", "Very short cropped", "💇", sort_order=6),
            Option("ponytail", "Ponytail", "Pulled back", "💇", sort_order=7),
            Option("pigtails", "Pigtails", "Two side tails", "👧", sort_order=8),
            Option("braid", "Braid", "Woven strands", "👧", sort_order=9),
            Option("bun", "Bun", "Coiled updo", "💇", sort_order=10),
            Option("curly", "Curly", "Natural curls", "👱", sort_order=11),
            Option("wavy", "Wavy", "Loose waves", "👱", sort_order=12),
            Option("straight", "Straight", "Sleek smooth", "👱", sort_order=13),
            Option("afro", "Afro", "Natural volume", "👱", sort_order=14),
            Option("dreadlocks", "Dreadlocks", "Roped locks", "👱", sort_order=15),
            Option("mohawk", "Mohawk", "Center strip", "🤘", sort_order=16),
            Option("undercut", "Undercut", "Shaved sides", "💇", sort_order=17),
            Option("bald", "Bald", "No hair", "👨", sort_order=18),
        ]
    )
    
    # ============================================================
    # HAIR COLORS
    # ============================================================
    HAIR_COLORS = OptionGroup(
        name="hair_colors",
        label="Hair Colors",
        description="Natural and fantasy hair colors",
        icon="🎨",
        sort_order=57,
        options=[
            Option("black", "Black", "Darkest natural", "⚫", sort_order=1),
            Option("dark_brown", "Dark Brown", "Deep brunette", "🤎", sort_order=2),
            Option("brown", "Brown", "Medium brunette", "🤎", sort_order=3),
            Option("light_brown", "Light Brown", "Golden brown", "🤎", sort_order=4),
            Option("blonde", "Blonde", "Golden yellow", "💛", sort_order=5),
            Option("platinum", "Platinum Blonde", "Near white", "🤍", sort_order=6),
            Option("strawberry", "Strawberry Blonde", "Red-gold", "🧡", sort_order=7),
            Option("red", "Red", "Vibrant copper", "❤️", sort_order=8),
            Option("auburn", "Auburn", "Red-brown", "🤎", sort_order=9),
            Option("gray", "Gray/Silver", "Natural aging", "⚪", sort_order=10),
            Option("white", "White", "Pure white", "⚪", sort_order=11),
            Option("blue", "Blue", "Fantasy color", "💙", sort_order=12),
            Option("pink", "Pink", "Fantasy color", "🩷", sort_order=13),
            Option("purple", "Purple", "Fantasy color", "💜", sort_order=14),
            Option("green", "Green", "Fantasy color", "💚", sort_order=15),
            Option("rainbow", "Rainbow", "Multi-colored", "🌈", sort_order=16),
            Option("pastel", "Pastel", "Soft fantasy", "🍦", sort_order=17),
        ]
    )
    
    # ============================================================
    # EYE COLORS
    # ============================================================
    EYE_COLORS = OptionGroup(
        name="eye_colors",
        label="Eye Colors",
        description="Character eye colors",
        icon="👁️",
        sort_order=58,
        options=[
            Option("brown", "Brown", "Most common", "🤎", sort_order=1),
            Option("blue", "Blue", "Clear sky", "💙", sort_order=2),
            Option("green", "Green", "Emerald", "💚", sort_order=3),
            Option("hazel", "Hazel", "Brown-green mix", "🤎", sort_order=4),
            Option("amber", "Amber", "Golden copper", "🧡", sort_order=5),
            Option("gray", "Gray", "Steel grey", "⚪", sort_order=6),
            Option("violet", "Violet", "Rare purple", "💜", sort_order=7),
            Option("heterochromia", "Heterochromia", "Two different colors", "👁️👁️", sort_order=8),
        ]
    )
    
    # ============================================================
    # ACCESSORIES
    # ============================================================
    ACCESSORIES = OptionGroup(
        name="accessories",
        label="Accessories",
        description="Character accessories",
        icon="🎒",
        sort_order=59,
        options=[
            Option("glasses", "Glasses", "Prescription eyewear", "👓", sort_order=1),
            Option("sunglasses", "Sunglasses", "Sun protection", "🕶️", sort_order=2),
            Option("hat", "Hat", "Headwear", "🧢", sort_order=3),
            Option("cap", "Baseball Cap", "Sporty headwear", "🧢", sort_order=4),
            Option("beanie", "Beanie", "Knit cap", "🧶", sort_order=5),
            Option("headband", "Headband", "Hair accessory", "🎀", sort_order=6),
            Option("bow", "Bow", "Decorative bow", "🎀", sort_order=7),
            Option("earrings", "Earrings", "Ear jewelry", "💎", sort_order=8),
            Option("necklace", "Necklace", "Neck jewelry", "📿", sort_order=9),
            Option("bracelet", "Bracelet", "Wrist jewelry", "📿", sort_order=10),
            Option("watch", "Watch", "Timepiece", "⌚", sort_order=11),
            Option("backpack", "Backpack", "School bag", "🎒", sort_order=12),
            Option("purse", "Purse", "Handbag", "👜", sort_order=13),
            Option("scarf", "Scarf", "Neck wrap", "🧣", sort_order=14),
            Option("gloves", "Gloves", "Hand coverings", "🧤", sort_order=15),
            Option("mask", "Mask", "Face covering", "😷", sort_order=16),
            Option("wings", "Wings", "Fairy/angel wings", "🪽", sort_order=17),
            Option("halo", "Halo", "Angel ring", "😇", sort_order=18),
            Option("crown", "Crown", "Royal headpiece", "👑", sort_order=19),
            Option("tiara", "Tiara", "Princess crown", "👸", sort_order=20),
        ]
    )
    
    # ============================================================
    # CLOTHING
    # ============================================================
    CLOTHING = OptionGroup(
        name="clothing",
        label="Clothing",
        description="Character clothing options",
        icon="👕",
        sort_order=60,
        options=[
            Option("t_shirt", "T-Shirt", "Casual top", "👕", sort_order=1),
            Option("shirt", "Button Shirt", "Collared shirt", "👔", sort_order=2),
            Option("dress", "Dress", "One-piece outfit", "👗", sort_order=3),
            Option("skirt", "Skirt", "Lower garment", "👗", sort_order=4),
            Option("pants", "Pants", "Long trousers", "👖", sort_order=5),
            Option("shorts", "Shorts", "Short trousers", "🩳", sort_order=6),
            Option("jeans", "Jeans", "Denim pants", "👖", sort_order=7),
            Option("sweater", "Sweater", "Knit top", "🧶", sort_order=8),
            Option("hoodie", "Hoodie", "Hooded sweatshirt", "🧥", sort_order=9),
            Option("jacket", "Jacket", "Outer layer", "🧥", sort_order=10),
            Option("coat", "Coat", "Heavy outerwear", "🧥", sort_order=11),
            Option("raincoat", "Raincoat", "Waterproof coat", "🧥", sort_order=12),
            Option("uniform", "Uniform", "School/work outfit", "👔", sort_order=13),
            Option("costume", "Costume", "Dress-up outfit", "🎭", sort_order=14),
            Option("pajamas", "Pajamas", "Sleepwear", "🛌", sort_order=15),
            Option("swimsuit", "Swimsuit", "Swimwear", "🩱", sort_order=16),
            Option("overalls", "Overalls", "Dungarees", "👖", sort_order=17),
            Option("romper", "Romper", "One-piece short", "👶", sort_order=18),
            Option("onesie", "Onesie", "Full body suit", "👶", sort_order=19),
            Option("apron", "Apron", "Protective overlay", "🧥", sort_order=20),
        ]
    )
    
    # ============================================================
    # FOODS
    # ============================================================
    FOODS = OptionGroup(
        name="foods",
        label="Foods",
        description="Food items for educational content",
        icon="🍎",
        sort_order=61,
        options=[
            Option("apple", "Apple", "Crisp fruit", "🍎", sort_order=1),
            Option("banana", "Banana", "Curved fruit", "🍌", sort_order=2),
            Option("bread", "Bread", "Baked staple", "🍞", sort_order=3),
            Option("cheese", "Cheese", "Dairy product", "🧀", sort_order=4),
            Option("egg", "Egg", "Protein source", "🥚", sort_order=5),
            Option("milk", "Milk", "Dairy drink", "🥛", sort_order=6),
            Option("chicken", "Chicken", "Poultry meat", "🍗", sort_order=7),
            Option("fish", "Fish", "Seafood", "🐟", sort_order=8),
            Option("rice", "Rice", "Grain staple", "🍚", sort_order=9),
            Option("pasta", "Pasta", "Noodles", "🍝", sort_order=10),
            Option("pizza", "Pizza", "Italian dish", "🍕", sort_order=11),
            Option("burger", "Burger", "Sandwich", "🍔", sort_order=12),
            Option("salad", "Salad", "Mixed vegetables", "🥗", sort_order=13),
            Option("soup", "Soup", "Liquid meal", "🍲", sort_order=14),
            Option("sandwich", "Sandwich", "Bread with filling", "🥪", sort_order=15),
            Option("cake", "Cake", "Sweet dessert", "🎂", sort_order=16),
            Option("cookie", "Cookie", "Baked treat", "🍪", sort_order=17),
            Option("ice_cream", "Ice Cream", "Frozen dessert", "🍦", sort_order=18),
            Option("yogurt", "Yogurt", "Fermented dairy", "🥛", sort_order=19),
            Option("nuts", "Nuts", "Healthy snacks", "🥜", sort_order=20),
        ]
    )
    
    # ============================================================
    # DRINKS
    # ============================================================
    DRINKS = OptionGroup(
        name="drinks",
        label="Drinks",
        description="Beverages for educational content",
        icon="🥤",
        sort_order=62,
        options=[
            Option("water", "Water", "Essential liquid", "💧", sort_order=1),
            Option("milk", "Milk", "Dairy beverage", "🥛", sort_order=2),
            Option("juice", "Juice", "Fruit drink", "🧃", sort_order=3),
            Option("orange_juice", "Orange Juice", "Citrus drink", "🍊", sort_order=4),
            Option("apple_juice", "Apple Juice", "Sweet fruit drink", "🍎", sort_order=5),
            Option("smoothie", "Smoothie", "Blended fruit", "🥤", sort_order=6),
            Option("tea", "Tea", "Hot beverage", "🍵", sort_order=7),
            Option("hot_chocolate", "Hot Chocolate", "Warm cocoa", "☕", sort_order=8),
            Option("lemonade", "Lemonade", "Lemon drink", "🍋", sort_order=9),
            Option("coconut_water", "Coconut Water", "Natural electrolyte", "🥥", sort_order=10),
        ]
    )
    
    # ============================================================
    # INSTRUMENTS
    # ============================================================
    INSTRUMENTS = OptionGroup(
        name="instruments",
        label="Musical Instruments",
        description="Instruments for music education",
        icon="🎵",
        sort_order=63,
        options=[
            Option("piano", "Piano", "Keyboard instrument", "🎹", sort_order=1),
            Option("guitar", "Guitar", "String instrument", "🎸", sort_order=2),
            Option("violin", "Violin", "Bowed string", "🎻", sort_order=3),
            Option("drums", "Drums", "Percussion set", "🥁", sort_order=4),
            Option("flute", "Flute", "Woodwind", "🎵", sort_order=5),
            Option("trumpet", "Trumpet", "Brass instrument", "🎺", sort_order=6),
            Option("saxophone", "Saxophone", "Jazz woodwind", "🎷", sort_order=7),
            Option("cello", "Cello", "Large bowed string", "🎻", sort_order=8),
            Option("harp", "Harp", "Plucked strings", "🎵", sort_order=9),
            Option("xylophone", "Xylophone", "Percussion bars", "🎵", sort_order=10),
            Option("tambourine", "Tambourine", "Hand percussion", "🎵", sort_order=11),
            Option("maracas", "Maracas", "Shakers", "🎵", sort_order=12),
            Option("triangle", "Triangle", "Metal percussion", "🎵", sort_order=13),
            Option("recorder", "Recorder", "Beginner wind", "🎵", sort_order=14),
            Option("ukulele", "Ukulele", "Small guitar", "🎸", sort_order=15),
            Option("keyboard", "Keyboard", "Electronic piano", "🎹", sort_order=16),
            Option("accordion", "Accordion", "Squeeze box", "🎵", sort_order=17),
            Option("harmonica", "Harmonica", "Mouth organ", "🎵", sort_order=18),
            Option("banjo", "Banjo", "Folk string", "🪕", sort_order=19),
            Option("mandolin", "Mandolin", "Small lute", "🎵", sort_order=20),
        ]
    )
    
    # ============================================================
    # FESTIVALS (20+)
    # ============================================================
    FESTIVALS = OptionGroup(
        name="festivals",
        label="Festivals & Holidays",
        description="Cultural festivals and holidays worldwide",
        icon="🎉",
        sort_order=64,
        options=[
            Option("christmas", "Christmas", "Dec 25 - Jesus birth", "🎄", sort_order=1),
            Option("new_year", "New Year", "Jan 1 - Fresh start", "🎆", sort_order=2),
            Option("eid", "Eid al-Fitr", "End of Ramadan", "🌙", sort_order=3),
            Option("eid_adha", "Eid al-Adha", "Festival of Sacrifice", "🐑", sort_order=4),
            Option("ramadan", "Ramadan", "Holy month fasting", "🌙", sort_order=5),
            Option("diwali", "Diwali", "Festival of Lights", "🪔", sort_order=6),
            Option("holi", "Holi", "Festival of Colors", "🌈", sort_order=7),
            Option("chinese_new_year", "Chinese New Year", "Lunar New Year", "🐉", sort_order=8),
            Option("thanksgiving", "Thanksgiving", "Gratitude feast", "🦃", sort_order=9),
            Option("halloween", "Halloween", "Spooky fun", "🎃", sort_order=10),
            Option("easter", "Easter", "Spring resurrection", "🐰", sort_order=11),
            Option("valentines", "Valentine's Day", "Love day", "💕", sort_order=12),
            Option("independence_day", "Independence Day", "National freedom", "🎆", sort_order=13),
            Option("kwanzaa", "Kwanzaa", "African heritage", "🕎", sort_order=14),
            Option("vesak", "Vesak", "Buddha's birthday", "🕉️", sort_order=15),
            Option("songkran", "Songkran", "Thai New Year water", "💦", sort_order=16),
            Option("carnival", "Carnival", "Pre-Lent festival", "🎭", sort_order=17),
            Option("oktoberfest", "Oktoberfest", "German beer festival", "🍺", sort_order=18),
            Option("day_of_dead", "Día de los Muertos", "Honor ancestors", "💀", sort_order=19),
            Option("mothers_day", "Mother's Day", "Honor mothers", "👩", sort_order=20),
            Option("fathers_day", "Father's Day", "Honor fathers", "👨", sort_order=21),
            Option("earth_day", "Earth Day", "Environmental awareness", "🌍", sort_order=22),
            Option("childrens_day", "Children's Day", "Celebrate children", "👶", sort_order=23),
            Option("teachers_day", "Teachers' Day", "Honor educators", "👩‍🏫", sort_order=24),
        ]
    )
    
    # ============================================================
    # RELIGIONS
    # ============================================================
    RELIGIONS = OptionGroup(
        name="religions",
        label="Religions",
        description="World religions for cultural education",
        icon="🕊️",
        sort_order=65,
        options=[
            Option("christianity", "Christianity", "Jesus Christ teachings", "✝️", sort_order=1),
            Option("islam", "Islam", "Quran and Prophet Muhammad", "☪️", sort_order=2),
            Option("hinduism", "Hinduism", "Dharma and karma", "🕉️", sort_order=3),
            Option("buddhism", "Buddhism", "Four Noble Truths", "☸️", sort_order=4),
            Option("judaism", "Judaism", "Torah and covenant", "✡️", sort_order=5),
            Option("sikhism", "Sikhism", "Guru Granth Sahib", "☬", sort_order=6),
            Option("taoism", "Taoism", "Tao Te Ching", "☯️", sort_order=7),
            Option("shinto", "Shinto", "Kami spirits", "⛩️", sort_order=8),
            Option("confucianism", "Confucianism", "Ethics and harmony", "📜", sort_order=9),
            Option("bahai", "Bahá'í Faith", "Unity of humanity", "✨", sort_order=10),
            Option("jainism", "Jainism", "Non-violence", "🕊️", sort_order=11),
            Option("zoroastrianism", "Zoroastrianism", "Good vs evil", "🔥", sort_order=12),
            Option("indigenous", "Indigenous Spirituality", "Nature-based", "🌿", sort_order=13),
            Option("secular", "Secular/Non-religious", "No religious affiliation", "🌍", sort_order=14),
        ]
    )
    
    # ============================================================
    # PROFESSIONS (Extended)
    # ============================================================
    PROFESSIONS = OptionGroup(
        name="professions",
        label="Professions",
        description="Extended profession list",
        icon="💼",
        sort_order=66,
        options=[
            Option("astronomer", "Astronomer", "Studies space", "🔭", sort_order=1),
            Option("biologist", "Biologist", "Studies life", "🔬", sort_order=2),
            Option("chemist", "Chemist", "Studies chemicals", "⚗️", sort_order=3),
            Option("physicist", "Physicist", "Studies matter/energy", "⚛️", sort_order=4),
            Option("geologist", "Geologist", "Studies Earth", "🪨", sort_order=5),
            Option("meteorologist", "Meteorologist", "Studies weather", "🌤️", sort_order=6),
            Option("paleontologist", "Paleontologist", "Studies fossils", "🦴", sort_order=7),
            Option("archaeologist", "Archaeologist", "Studies ancient humans", "🏺", sort_order=8),
            Option("anthropologist", "Anthropologist", "Studies cultures", "🌍", sort_order=9),
            Option("psychologist", "Psychologist", "Studies mind", "🧠", sort_order=10),
            Option("sociologist", "Sociologist", "Studies society", "👥", sort_order=11),
            Option("economist", "Economist", "Studies economy", "📊", sort_order=12),
            Option("historian", "Historian", "Studies past", "📜", sort_order=13),
            Option("philosopher", "Philosopher", "Studies wisdom", "🤔", sort_order=14),
            Option("mathematician", "Mathematician", "Studies numbers", "🔢", sort_order=15),
            Option("statistician", "Statistician", "Studies data", "📈", sort_order=16),
            Option("linguist", "Linguist", "Studies language", "🗣️", sort_order=17),
            Option("architect", "Architect", "Designs buildings", "🏗️", sort_order=18),
            Option("civil_engineer", "Civil Engineer", "Builds infrastructure", "🌉", sort_order=19),
            Option("mechanical_engineer", "Mechanical Engineer", "Designs machines", "⚙️", sort_order=20),
            Option("electrical_engineer", "Electrical Engineer", "Works with electricity", "⚡", sort_order=21),
            Option("software_engineer", "Software Engineer", "Writes code", "💻", sort_order=22),
            Option("data_scientist", "Data Scientist", "Analyzes data", "📊", sort_order=23),
            Option("ai_researcher", "AI Researcher", "Develops AI", "🤖", sort_order=24),
            Option("robotics_engineer", "Robotics Engineer", "Builds robots", "🤖", sort_order=25),
            Option("biomedical_engineer", "Biomedical Engineer", "Medical devices", "🏥", sort_order=26),
            Option("environmental_scientist", "Environmental Scientist", "Protects nature", "🌿", sort_order=27),
            Option("marine_biologist", "Marine Biologist", "Ocean life", "🌊", sort_order=28),
            Option("wildlife_biologist", "Wildlife Biologist", "Animal conservation", "🦁", sort_order=29),
            Option("veterinarian", "Veterinarian", "Animal doctor", "🐾", sort_order=30),
            Option("zoologist", "Zoologist", "Studies animals", "🦓", sort_order=31),
            Option("botanist", "Botanist", "Studies plants", "🌱", sort_order=32),
            Option("ecologist", "Ecologist", "Studies ecosystems", "🌍", sort_order=33),
            Option("geneticist", "Geneticist", "Studies DNA", "🧬", sort_order=34),
            Option("neuroscientist", "Neuroscientist", "Studies brain", "🧠", sort_order=35),
            Option("immunologist", "Immunologist", "Studies immunity", "🦠", sort_order=36),
            Option("pharmacist", "Pharmacist", "Medicines expert", "💊", sort_order=37),
            Option("surgeon", "Surgeon", "Operates", "🏥", sort_order=38),
            Option("pediatrician", "Pediatrician", "Children's doctor", "👶", sort_order=39),
            Option("cardiologist", "Cardiologist", "Heart doctor", "❤️", sort_order=40),
            Option("neurologist", "Neurologist", "Brain doctor", "🧠", sort_order=41),
        ]
    )
    
    # ============================================================
    # NEW EDUCATION SUPPORT OPTION GROUPS
    # ============================================================
    
    # COUNTING_OBJECTS (40+)
    COUNTING_OBJECTS = OptionGroup(
        name="counting_objects",
        label="Counting Objects",
        description="Objects for counting activities",
        icon="🔢",
        sort_order=67,
        options=[
            Option("apples", "Apples", "Red or green fruit", "🍎", sort_order=1),
            Option("balls", "Balls", "Round play objects", "⚽", sort_order=2),
            Option("stars", "Stars", "Twinkling night lights", "⭐", sort_order=3),
            Option("flowers", "Flowers", "Blooming plants", "🌸", sort_order=4),
            Option("cars", "Cars", "Toy vehicles", "🚗", sort_order=5),
            Option("birds", "Birds", "Flying creatures", "🐦", sort_order=6),
            Option("fish", "Fish", "Swimming creatures", "🐟", sort_order=7),
            Option("butterflies", "Butterflies", "Colorful insects", "🦋", sort_order=8),
            Option("balloons", "Balloons", "Floating decorations", "🎈", sort_order=9),
            Option("pencils", "Pencils", "Writing tools", "✏️", sort_order=10),
            Option("books", "Books", "Reading materials", "📚", sort_order=11),
            Option("trees", "Trees", "Tall plants", "🌳", sort_order=12),
            Option("candies", "Candies", "Sweet treats", "🍬", sort_order=13),
            Option("coins", "Coins", "Money pieces", "🪙", sort_order=14),
            Option("toys", "Toys", "Play things", "🧸", sort_order=15),
            Option("blocks", "Blocks", "Building pieces", "🧱", sort_order=16),
            Option("cookies", "Cookies", "Baked treats", "🍪", sort_order=17),
            Option("eggs", "Eggs", "Oval food items", "🥚", sort_order=18),
            Option("bananas", "Bananas", "Curved yellow fruit", "🍌", sort_order=19),
            Option("oranges", "Oranges", "Round citrus fruit", "🍊", sort_order=20),
            Option("cups", "Cups", "Drinking vessels", "🥤", sort_order=21),
            Option("hats", "Hats", "Head wear", "🧢", sort_order=22),
            Option("shoes", "Shoes", "Footwear", "👟", sort_order=23),
            Option("kites", "Kites", "Flying toys", "🪁", sort_order=24),
            Option("planets", "Planets", "Space worlds", "🪐", sort_order=25),
            Option("clouds", "Clouds", "Sky puffs", "☁️", sort_order=26),
            Option("hearts", "Hearts", "Love symbols", "❤️", sort_order=27),
            Option("smiley_faces", "Smiley Faces", "Happy faces", "😊", sort_order=28),
            Option("ice_creams", "Ice Creams", "Frozen treats", "🍦", sort_order=29),
            Option("buses", "Buses", "Big vehicles", "🚌", sort_order=30),
            Option("trains", "Trains", "Rail vehicles", "🚂", sort_order=31),
            Option("robots", "Robots", "Mechanical friends", "🤖", sort_order=32),
            Option("dinosaurs", "Dinosaurs", "Prehistoric creatures", "🦕", sort_order=33),
            Option("rockets", "Rockets", "Space vehicles", "🚀", sort_order=34),
            Option("gifts", "Gifts", "Wrapped presents", "🎁", sort_order=35),
            Option("umbrellas", "Umbrellas", "Rain protection", "☂️", sort_order=36),
            Option("leaves", "Leaves", "Tree parts", "🍃", sort_order=37),
            Option("shells", "Shells", "Beach treasures", "🐚", sort_order=38),
            Option("snowflakes", "Snowflakes", "Ice crystals", "❄️", sort_order=39),
            Option("gems", "Gems", "Sparkly stones", "💎", sort_order=40),
            Option("mushrooms", "Mushrooms", "Fungi", "🍄", sort_order=41),
            Option("acorns", "Acorns", "Oak seeds", "🌰", sort_order=42),
            Option("pebbles", "Pebbles", "Small stones", "🪨", sort_order=43),
            Option("feathers", "Feathers", "Bird plumage", "🪶", sort_order=44),
        ]
    )
    
    # COUNTING_STYLES
    COUNTING_STYLES = OptionGroup(
        name="counting_styles",
        label="Counting Styles",
        description="Methods of counting",
        icon="🔢",
        sort_order=68,
        options=[
            Option("count_forward", "Count Forward", "1, 2, 3, 4, 5...", "➡️", sort_order=1),
            Option("count_backward", "Count Backward", "10, 9, 8, 7, 6...", "⬅️", sort_order=2),
            Option("skip_counting", "Skip Counting", "2, 4, 6, 8... or 5, 10, 15...", "⏭️", sort_order=3),
            Option("interactive_counting", "Interactive Counting", "Touch and count", "👆", sort_order=4),
            Option("visual_counting", "Visual Counting", "See groups and count", "👁️", sort_order=5),
            Option("group_counting", "Group Counting", "Count by 2s, 5s, 10s", "📦", sort_order=6),
            Option("finger_counting", "Finger Counting", "Use fingers to count", "🖐️", sort_order=7),
        ]
    )
    
    # NUMBER_TYPES
    NUMBER_TYPES = OptionGroup(
        name="number_types",
        label="Number Types",
        description="Types of numbers for math education",
        icon="🔢",
        sort_order=69,
        options=[
            Option("cardinal", "Cardinal", "Counting numbers: 1, 2, 3", "1️⃣", sort_order=1),
            Option("ordinal", "Ordinal", "Position numbers: 1st, 2nd, 3rd", "🥇", sort_order=2),
            Option("even", "Even Numbers", "Divisible by 2: 2, 4, 6", "2️⃣", sort_order=3),
            Option("odd", "Odd Numbers", "Not divisible by 2: 1, 3, 5", "1️⃣", sort_order=4),
        ]
    )
    
    # MATH_OPERATIONS
    MATH_OPERATIONS = OptionGroup(
        name="math_operations",
        label="Math Operations",
        description="Basic arithmetic operations",
        icon="➕",
        sort_order=70,
        options=[
            Option("counting", "Counting", "Count objects", "🔢", sort_order=1),
            Option("addition", "Addition", "Add numbers together", "➕", sort_order=2),
            Option("subtraction", "Subtraction", "Take away", "➖", sort_order=3),
            Option("multiplication", "Multiplication", "Repeated addition", "✖️", sort_order=4),
            Option("division", "Division", "Share equally", "➗", sort_order=5),
            Option("comparison", "Comparison", "More, less, equal", "⚖️", sort_order=6),
        ]
    )
    
    # TEACHING_STYLES
    TEACHING_STYLES = OptionGroup(
        name="teaching_styles",
        label="Teaching Styles",
        description="Pedagogical approaches for education",
        icon="👩‍🏫",
        sort_order=71,
        options=[
            Option("fun_teacher", "Fun Teacher", "Engaging and entertaining", "🎉", sort_order=1),
            Option("friendly_panda", "Friendly Panda", "Gentle guide character", "🐼", sort_order=2),
            Option("cartoon_teacher", "Cartoon Teacher", "Animated instructor", "🎭", sort_order=3),
            Option("classroom", "Classroom Setting", "Traditional school environment", "🏫", sort_order=4),
            Option("storytelling", "Storytelling", "Learn through narrative", "📖", sort_order=5),
            Option("interactive_quiz", "Interactive Quiz", "Question-based learning", "❓", sort_order=6),
            Option("montessori", "Montessori", "Child-led exploration", "🏫", sort_order=7),
            Option("play_based", "Play Based", "Learning through play", "🎮", sort_order=8),
            Option("flash_cards", "Flash Cards", "Quick visual recall", "🃏", sort_order=9),
            Option("adventure_learning", "Adventure Learning", "Quest-based education", "🗺️", sort_order=10),
        ]
    )
    
    # VOCABULARY_LEVELS
    VOCABULARY_LEVELS = OptionGroup(
        name="vocabulary_levels",
        label="Vocabulary Levels",
        description="Word difficulty levels",
        icon="📚",
        sort_order=72,
        options=[
            Option("beginner", "Beginner", "First words, basic", "🌱", sort_order=1),
            Option("easy", "Easy", "Simple common words", "🌿", sort_order=2),
            Option("intermediate", "Intermediate", "Growing vocabulary", "🌳", sort_order=3),
            Option("advanced", "Advanced", "Complex words", "🌲", sort_order=4),
        ]
    )
    
    # DIETS
    DIETS = OptionGroup(
        name="diets",
        label="Animal Diets",
        description="What animals eat",
        icon="🍽️",
        sort_order=73,
        options=[
            Option("herbivore", "Herbivore", "Eats plants only", "🌱", sort_order=1),
            Option("carnivore", "Carnivore", "Eats meat only", "🥩", sort_order=2),
            Option("omnivore", "Omnivore", "Eats plants and meat", "🌱🥩", sort_order=3),
            Option("insectivore", "Insectivore", "Eats insects", "🐜", sort_order=4),
            Option("nectar", "Nectar Feeder", "Drinks flower nectar", "🌸", sort_order=5),
            Option("fruits", "Frugivore", "Eats fruits", "🍎", sort_order=6),
            Option("seeds", "Granivore", "Eats seeds", "🌰", sort_order=7),
            Option("grass", "Grazing", "Eats grass", "🌾", sort_order=8),
            Option("fish", "Piscivore", "Eats fish", "🐟", sort_order=9),
        ]
    )
    
    # ANIMAL_TYPES
    ANIMAL_TYPES = OptionGroup(
        name="animal_types",
        label="Animal Types",
        description="Classification of animals",
        icon="🦁",
        sort_order=74,
        options=[
            Option("mammal", "Mammal", "Warm-blooded, fur/hair, milk", "🦁", sort_order=1),
            Option("bird", "Bird", "Feathers, wings, lays eggs", "🐦", sort_order=2),
            Option("fish", "Fish", "Gills, fins, lives in water", "🐟", sort_order=3),
            Option("reptile", "Reptile", "Scales, cold-blooded, lays eggs", "🐍", sort_order=4),
            Option("amphibian", "Amphibian", "Moist skin, metamorphosis", "🐸", sort_order=5),
            Option("insect", "Insect", "Six legs, three body parts", "🐜", sort_order=6),
        ]
    )
    
    # NEST_TYPES
    NEST_TYPES = OptionGroup(
        name="nest_types",
        label="Nest Types",
        description="Types of animal nests",
        icon="🪺",
        sort_order=75,
        options=[
            Option("tree_nest", "Tree Nest", "Built in tree branches", "🌳", sort_order=1),
            Option("ground_nest", "Ground Nest", "Hidden on the ground", "🌿", sort_order=2),
            Option("hole_nest", "Hole Nest", "In tree cavity or burrow", "🕳️", sort_order=3),
            Option("floating_nest", "Floating Nest", "On water surface", "🌊", sort_order=4),
            Option("cliff_nest", "Cliff Nest", "On rocky ledge", "🏔️", sort_order=5),
        ]
    )
    
    # FLYING_STYLES
    FLYING_STYLES = OptionGroup(
        name="flying_styles",
        label="Flying Styles",
        description="How birds and insects fly",
        icon="🕊️",
        sort_order=76,
        options=[
            Option("gliding", "Gliding", "Soaring without flapping", "🦅", sort_order=1),
            Option("soaring", "Soaring", "Rising on thermal currents", "🦅", sort_order=2),
            Option("hovering", "Hovering", "Staying in one place", "🐦", sort_order=3),
            Option("fast_flying", "Fast Flying", "Speed flight", "⚡", sort_order=4),
            Option("slow_flying", "Slow Flying", "Gentle flight", "🦋", sort_order=5),
            Option("flapping", "Flapping", "Powered wing beats", "🐦", sort_order=6),
        ]
    )
    
    # FUEL_TYPES
    FUEL_TYPES = OptionGroup(
        name="fuel_types",
        label="Fuel Types",
        description="Energy sources for vehicles",
        icon="⛽",
        sort_order=77,
        options=[
            Option("petrol", "Petrol/Gasoline", "Traditional fuel", "⛽", sort_order=1),
            Option("diesel", "Diesel", "Heavy vehicle fuel", "⛽", sort_order=2),
            Option("electric", "Electric", "Battery powered", "🔋", sort_order=3),
            Option("hybrid", "Hybrid", "Gas + electric", "🔋⛽", sort_order=4),
            Option("solar", "Solar", "Sun powered", "☀️", sort_order=5),
            Option("human_powered", "Human Powered", "Muscle energy", "💪", sort_order=6),
        ]
    )
    
    # BODY_FUNCTIONS
    BODY_FUNCTIONS = OptionGroup(
        name="body_functions",
        label="Body Functions",
        description="What body parts do",
        icon="🫀",
        sort_order=78,
        options=[
            Option("seeing", "Seeing", "Eyes detect light", "👁️", sort_order=1),
            Option("hearing", "Hearing", "Ears detect sound", "👂", sort_order=2),
            Option("smelling", "Smelling", "Nose detects scents", "👃", sort_order=3),
            Option("tasting", "Tasting", "Tongue detects flavors", "👅", sort_order=4),
            Option("touching", "Touching", "Skin feels textures", "✋", sort_order=5),
            Option("walking", "Walking", "Legs move body", "🦵", sort_order=6),
            Option("holding", "Holding", "Hands grasp objects", "🤲", sort_order=7),
            Option("thinking", "Thinking", "Brain processes", "🧠", sort_order=8),
            Option("speaking", "Speaking", "Mouth makes words", "👄", sort_order=9),
            Option("breathing", "Breathing", "Lungs exchange air", "🫁", sort_order=10),
        ]
    )
    
    # HEALTHY_HABITS
    HEALTHY_HABITS = OptionGroup(
        name="healthy_habits",
        label="Healthy Habits",
        description="Good daily practices for kids",
        icon="🌟",
        sort_order=79,
        options=[
            Option("brush_teeth", "Brush Teeth", "Clean teeth twice daily", "🦷", sort_order=1),
            Option("wash_hands", "Wash Hands", "Clean hands often", "🧼", sort_order=2),
            Option("exercise", "Exercise", "Move body daily", "🏃", sort_order=3),
            Option("sleep_early", "Sleep Early", "Rest at night", "😴", sort_order=4),
            Option("eat_healthy", "Eat Healthy", "Fruits and vegetables", "🍎", sort_order=5),
            Option("drink_water", "Drink Water", "Stay hydrated", "💧", sort_order=6),
        ]
    )
    
    # DAILY_ROUTINES
    DAILY_ROUTINES = OptionGroup(
        name="daily_routines",
        label="Daily Routines",
        description="Parts of a child's day",
        icon="📅",
        sort_order=80,
        options=[
            Option("wake_up", "Wake Up", "Start the day", "🌅", sort_order=1),
            Option("breakfast", "Breakfast", "Morning meal", "🍳", sort_order=2),
            Option("school", "School", "Learning time", "🏫", sort_order=3),
            Option("homework", "Homework", "Practice at home", "📝", sort_order=4),
            Option("play", "Play", "Fun and games", "🎮", sort_order=5),
            Option("dinner", "Dinner", "Evening meal", "🍽️", sort_order=6),
            Option("sleep", "Sleep", "Night rest", "😴", sort_order=7),
        ]
    )
    
    # OPPOSITE_PAIRS (40+)
    OPPOSITE_PAIRS = OptionGroup(
        name="opposite_pairs",
        label="Opposite Pairs",
        description="Contrasting concepts for learning",
        icon="⚖️",
        sort_order=81,
        options=[
            Option("big_small", "Big ↔ Small", "Size comparison", "📏", sort_order=1),
            Option("hot_cold", "Hot ↔ Cold", "Temperature", "🌡️", sort_order=2),
            Option("fast_slow", "Fast ↔ Slow", "Speed", "⚡🐢", sort_order=3),
            Option("tall_short", "Tall ↔ Short", "Height", "📐", sort_order=4),
            Option("heavy_light", "Heavy ↔ Light", "Weight", "⚖️", sort_order=5),
            Option("happy_sad", "Happy ↔ Sad", "Emotions", "😊😢", sort_order=6),
            Option("clean_dirty", "Clean ↔ Dirty", "Cleanliness", "✨💩", sort_order=7),
            Option("open_closed", "Open ↔ Closed", "State", "📂📁", sort_order=8),
            Option("day_night", "Day ↔ Night", "Time", "☀️🌙", sort_order=9),
            Option("full_empty", "Full ↔ Empty", "Capacity", "🥤🥛", sort_order=10),
            Option("up_down", "Up ↔ Down", "Direction", "⬆️⬇️", sort_order=11),
            Option("in_out", "In ↔ Out", "Position", "📥📤", sort_order=12),
            Option("on_off", "On ↔ Off", "State", "🔛🔴", sort_order=13),
            Option("wet_dry", "Wet ↔ Dry", "Moisture", "💧☀️", sort_order=14),
            Option("hard_soft", "Hard ↔ Soft", "Texture", "🪨☁️", sort_order=15),
            Option("rough_smooth", "Rough ↔ Smooth", "Surface", "🪨🪞", sort_order=16),
            Option("loud_quiet", "Loud ↔ Quiet", "Volume", "🔊🔇", sort_order=17),
            Option("bright_dark", "Bright ↔ Dark", "Light", "💡🌑", sort_order=18),
            Option("near_far", "Near ↔ Far", "Distance", "📍🗺️", sort_order=19),
            Option("old_new", "Old ↔ New", "Age", "👴👶", sort_order=20),
            Option("young_old", "Young ↔ Old", "Age", "👶👴", sort_order=21),
            Option("long_short", "Long ↔ Short", "Length", "📏✂️", sort_order=22),
            Option("wide_narrow", "Wide ↔ Narrow", "Width", "↔️↕️", sort_order=23),
            Option("thick_thin", "Thick ↔ Thin", "Thickness", "📚📄", sort_order=24),
            Option("strong_weak", "Strong ↔ Weak", "Strength", "💪🤏", sort_order=25),
            Option("rich_poor", "Rich ↔ Poor", "Wealth", "💰🪙", sort_order=26),
            Option("sweet_sour", "Sweet ↔ Sour", "Taste", "🍬🍋", sort_order=27),
            Option("bitter_sweet", "Bitter ↔ Sweet", "Taste", "🍫🍬", sort_order=28),
            Option("fresh_stale", "Fresh ↔ Stale", "Freshness", "🥖🍞", sort_order=29),
            Option("alive_dead", "Alive ↔ Dead", "Life", "🌱💀", sort_order=30),
            Option("awake_asleep", "Awake ↔ Asleep", "Consciousness", "😊😴", sort_order=31),
            Option("start_finish", "Start ↔ Finish", "Progress", "🏁🏁", sort_order=32),
            Option("begin_end", "Begin ↔ End", "Sequence", "▶️⏹️", sort_order=33),
            Option("top_bottom", "Top ↔ Bottom", "Position", "⬆️⬇️", sort_order=34),
            Option("left_right", "Left ↔ Right", "Direction", "⬅️➡️", sort_order=35),
            Option("front_back", "Front ↔ Back", "Position", "⬆️⬇️", sort_order=36),
            Option("inside_outside", "Inside ↔ Outside", "Location", "🏠🌳", sort_order=37),
            Option("above_below", "Above ↔ Below", "Height", "☁️🌍", sort_order=38),
            Option("over_under", "Over ↔ Under", "Position", "🌉🕳️", sort_order=39),
            Option("more_less", "More ↔ Less", "Quantity", "➕➖", sort_order=40),
            Option("same_different", "Same ↔ Different", "Comparison", "🟰❌", sort_order=41),
            Option("together_apart", "Together ↔ Apart", "Proximity", "🤝💔", sort_order=42),
            Option("push_pull", "Push ↔ Pull", "Force", "➡️⬅️", sort_order=43),
            Option("give_take", "Give ↔ Take", "Exchange", "🎁🤲", sort_order=44),
        ]
    )
    
    # PHONICS_SOUNDS (A-Z)
    PHONICS_SOUNDS = OptionGroup(
        name="phonics_sounds",
        label="Phonics Sounds",
        description="Letter sounds A-Z for phonics education",
        icon="🔤",
        sort_order=82,
        options=[
            Option("a_short", "Short A /æ/", "Apple, cat, hat", "🍎", sort_order=1),
            Option("a_long", "Long A /eɪ/", "Cake, rain, day", "🎂", sort_order=2),
            Option("b", "B /b/", "Ball, bat, book", "🏀", sort_order=3),
            Option("c_hard", "Hard C /k/", "Cat, cup, cow", "🐱", sort_order=4),
            Option("c_soft", "Soft C /s/", "City, cent, circle", "🏙️", sort_order=5),
            Option("d", "D /d/", "Dog, duck, door", "🐕", sort_order=6),
            Option("e_short", "Short E /ɛ/", "Egg, bed, red", "🥚", sort_order=7),
            Option("e_long", "Long E /i:/", "Tree, bee, see", "🌳", sort_order=8),
            Option("f", "F /f/", "Fish, fan, foot", "🐟", sort_order=9),
            Option("g_hard", "Hard G /g/", "Goat, girl, pig", "🐐", sort_order=10),
            Option("g_soft", "Soft G /dʒ/", "Giraffe, gem, giant", "🦒", sort_order=11),
            Option("h", "H /h/", "Hat, house, hand", "🎩", sort_order=12),
            Option("i_short", "Short I /ɪ/", "Igloo, pig, sit", "🏠", sort_order=13),
            Option("i_long", "Long I /aɪ/", "Ice, kite, bike", "🧊", sort_order=14),
            Option("j", "J /dʒ/", "Jar, jam, jump", "🫙", sort_order=15),
            Option("k", "K /k/", "Kite, key, kangaroo", "🪁", sort_order=16),
            Option("l", "L /l/", "Lion, leaf, leg", "🦁", sort_order=17),
            Option("m", "M /m/", "Moon, man, map", "🌙", sort_order=18),
            Option("n", "N /n/", "Nest, nose, net", "🪺", sort_order=19),
            Option("o_short", "Short O /ɒ/", "Octopus, pot, dog", "🐙", sort_order=20),
            Option("o_long", "Long O /oʊ/", "Ocean, boat, home", "🌊", sort_order=21),
            Option("p", "P /p/", "Pig, pen, pot", "🐷", sort_order=22),
            Option("q", "Qu /kw/", "Queen, quilt, quiet", "👑", sort_order=23),
            Option("r", "R /r/", "Rabbit, red, run", "🐰", sort_order=24),
            Option("s", "S /s/", "Sun, snake, sock", "☀️", sort_order=25),
            Option("t", "T /t/", "Tiger, top, ten", "🐅", sort_order=26),
            Option("u_short", "Short U /ʌ/", "Umbrella, cup, sun", "☂️", sort_order=27),
            Option("u_long", "Long U /ju:/", "Unicorn, cube, tube", "🦄", sort_order=28),
            Option("v", "V /v/", "Van, vase, violin", "🚐", sort_order=29),
            Option("w", "W /w/", "Whale, web, wagon", "🐋", sort_order=30),
            Option("x", "X /ks/", "Box, fox, six", "📦", sort_order=31),
            Option("y", "Y /j/", "Yellow, yes, yo-yo", "💛", sort_order=32),
            Option("z", "Z /z/", "Zebra, zip, zoo", "🦓", sort_order=33),
            Option("sh", "SH /ʃ/", "Ship, shoe, fish", "🚢", sort_order=34),
            Option("ch", "CH /tʃ/", "Chair, cheese, chicken", "🪑", sort_order=35),
            Option("th_voiced", "TH Voiced /ð/", "This, that, mother", "👆", sort_order=36),
            Option("th_unvoiced", "TH Unvoiced /θ/", "Think, thumb, bath", "🤔", sort_order=37),
            Option("wh", "WH /w/", "Whale, wheel, white", "🐋", sort_order=38),
            Option("ph", "PH /f/", "Phone, photo, elephant", "📞", sort_order=39),
            Option("ck", "CK /k/", "Duck, sock, back", "🦆", sort_order=40),
            Option("ng", "NG /ŋ/", "Sing, ring, king", "💍", sort_order=41),
            Option("nk", "NK /ŋk/", "Sink, pink, tank", "🛁", sort_order=42),
        ]
    )
    
    # QUIZ_TOPICS (40+)
    QUIZ_TOPICS = OptionGroup(
        name="quiz_topics",
        label="Quiz Topics",
        description="Subject areas for educational quizzes",
        icon="❓",
        sort_order=83,
        options=[
            Option("animals", "Animals", "Creatures and habitats", "🦁", sort_order=1),
            Option("birds", "Birds", "Feathered friends", "🐦", sort_order=2),
            Option("space", "Space", "Planets and stars", "🚀", sort_order=3),
            Option("weather", "Weather", "Seasons and climate", "🌤️", sort_order=4),
            Option("science", "Science", "Experiments and facts", "🔬", sort_order=5),
            Option("math", "Math", "Numbers and shapes", "🔢", sort_order=6),
            Option("countries", "Countries", "World nations", "🌍", sort_order=7),
            Option("flags", "Flags", "National symbols", "🏁", sort_order=8),
            Option("shapes", "Shapes", "Geometry basics", "🔷", sort_order=9),
            Option("colors", "Colors", "Color recognition", "🎨", sort_order=10),
            Option("planets", "Planets", "Solar system", "🪐", sort_order=11),
            Option("transport", "Transport", "Vehicles and travel", "🚌", sort_order=12),
            Option("nature", "Nature", "Plants and outdoors", "🌿", sort_order=13),
            Option("ocean", "Ocean", "Sea life", "🌊", sort_order=14),
            Option("human_body", "Human Body", "Anatomy basics", "🫀", sort_order=15),
            Option("food", "Food", "Nutrition and meals", "🍎", sort_order=16),
            Option("history", "History", "Past events", "📜", sort_order=17),
            Option("technology", "Technology", "Gadgets and inventions", "💻", sort_order=18),
            Option("dinosaurs", "Dinosaurs", "Prehistoric creatures", "🦕", sort_order=19),
            Option("insects", "Insects", "Bugs and beetles", "🐜", sort_order=20),
            Option("fruits", "Fruits", "Healthy fruits", "🍓", sort_order=21),
            Option("vegetables", "Vegetables", "Healthy veggies", "🥕", sort_order=22),
            Option("sports", "Sports", "Games and activities", "⚽", sort_order=23),
            Option("music", "Music", "Instruments and songs", "🎵", sort_order=24),
            Option("art", "Art", "Creative expression", "🎨", sort_order=25),
            Option("community_helpers", "Community Helpers", "Jobs people do", "👮", sort_order=26),
            Option("seasons", "Seasons", "Four seasons", "🌍", sort_order=27),
            Option("holidays", "Holidays", "Celebrations", "🎉", sort_order=28),
            Option("alphabet", "Alphabet", "Letters A-Z", "🔤", sort_order=29),
            Option("numbers", "Numbers", "Counting and math", "🔢", sort_order=30),
            Option("phonics", "Phonics", "Letter sounds", "🔤", sort_order=31),
            Option("reading", "Reading", "Words and stories", "📖", sort_order=32),
            Option("spelling", "Spelling", "Word building", "✍️", sort_order=33),
            Option("grammar", "Grammar", "Sentence structure", "📝", sort_order=34),
            Option("vocabulary", "Vocabulary", "Word meanings", "📚", sort_order=35),
            Option("opposites", "Opposites", "Contrasting concepts", "⚖️", sort_order=36),
            Option("rhyming", "Rhyming", "Sound patterns", "🎵", sort_order=37),
            Option("patterns", "Patterns", "Sequences", "🔄", sort_order=38),
            Option("sorting", "Sorting", "Categories", "📦", sort_order=39),
            Option("measurement", "Measurement", "Size and weight", "📏", sort_order=40),
            Option("time", "Time", "Clocks and calendars", "🕐", sort_order=41),
            Option("money", "Money", "Coins and bills", "💰", sort_order=42),
            Option("safety", "Safety", "Staying safe", "🛡️", sort_order=43),
            Option("manners", "Manners", "Polite behavior", "🤝", sort_order=44),
            Option("emotions", "Emotions", "Feelings", "😊", sort_order=45),
            Option("family", "Family", "Relatives", "👨‍👩‍👧‍👦", sort_order=46),
            Option("school", "School", "Classroom life", "🏫", sort_order=47),
            Option("home", "Home", "House and rooms", "🏠", sort_order=48),
        ]
    )
    
    # QUIZ_DIFFICULTY
    QUIZ_DIFFICULTY = OptionGroup(
        name="quiz_difficulty",
        label="Quiz Difficulty",
        description="Difficulty levels for quizzes",
        icon="📊",
        sort_order=84,
        options=[
            Option("beginner", "Beginner", "Very easy questions", "🌱", sort_order=1),
            Option("easy", "Easy", "Simple questions", "🌿", sort_order=2),
            Option("medium", "Medium", "Moderate challenge", "🌳", sort_order=3),
            Option("hard", "Hard", "Challenging questions", "🌲", sort_order=4),
            Option("expert", "Expert", "Very difficult", "🏆", sort_order=5),
        ]
    )
    
    # GROWING_PLACES
    GROWING_PLACES = OptionGroup(
        name="growing_places",
        label="Growing Places",
        description="Where plants grow",
        icon="🌱",
        sort_order=85,
        options=[
            Option("farm", "Farm", "Large scale crops", "🚜", sort_order=1),
            Option("garden", "Garden", "Home growing space", "🏡", sort_order=2),
            Option("greenhouse", "Greenhouse", "Controlled environment", "🏠", sort_order=3),
            Option("field", "Field", "Open land crops", "🌾", sort_order=4),
            Option("orchard", "Orchard", "Fruit trees", "🌳", sort_order=5),
            Option("pot", "Pot/Container", "Small space growing", "🪴", sort_order=6),
            Option("hydroponic", "Hydroponic", "Water-based growing", "💧", sort_order=7),
            Option("windowsill", "Windowsill", "Indoor sunny spot", "🪟", sort_order=8),
            Option("community_garden", "Community Garden", "Shared growing space", "🌿", sort_order=9),
            Option("vertical_farm", "Vertical Farm", "Stacked layers", "🏢", sort_order=10),
        ]
    )
    
    # ENVIRONMENTS
    ENVIRONMENTS = OptionGroup(
        name="environments",
        label="Environments",
        description="Settings for stories and learning",
        icon="🌍",
        sort_order=86,
        options=[
            Option("classroom", "Classroom", "School learning space", "🏫", sort_order=1),
            Option("forest", "Forest", "Trees and wildlife", "🌳", sort_order=2),
            Option("jungle", "Jungle", "Dense tropical forest", "🌿", sort_order=3),
            Option("space", "Space", "Stars and planets", "🚀", sort_order=4),
            Option("ocean", "Ocean", "Under the sea", "🌊", sort_order=5),
            Option("playground", "Playground", "Outdoor play area", "🛝", sort_order=6),
            Option("farm", "Farm", "Animals and crops", "🚜", sort_order=7),
            Option("city", "City", "Urban streets", "🏙️", sort_order=8),
            Option("village", "Village", "Small community", "🏘️", sort_order=9),
            Option("beach", "Beach", "Sand and waves", "🏖️", sort_order=10),
            Option("mountain", "Mountain", "High peaks", "⛰️", sort_order=11),
            Option("desert", "Desert", "Hot dry land", "🏜️", sort_order=12),
            Option("arctic", "Arctic", "Frozen north", "🧊", sort_order=13),
            Option("river", "River", "Flowing water", "🏞️", sort_order=14),
            Option("lake", "Lake", "Still water", "🏞️", sort_order=15),
            Option("cave", "Cave", "Underground", "🕳️", sort_order=16),
            Option("island", "Island", "Land in water", "🏝️", sort_order=17),
            Option("park", "Park", "Green recreation", "🌳", sort_order=18),
            Option("zoo", "Zoo", "Animal park", "🦁", sort_order=19),
            Option("aquarium", "Aquarium", "Underwater zoo", "🐠", sort_order=20),
            Option("museum", "Museum", "History and art", "🏛️", sort_order=21),
            Option("library", "Library", "Books and quiet", "📚", sort_order=22),
            Option("hospital", "Hospital", "Medical care", "🏥", sort_order=23),
            Option("fire_station", "Fire Station", "Emergency base", "🚒", sort_order=24),
            Option("police_station", "Police Station", "Safety center", "🚓", sort_order=25),
            Option("post_office", "Post Office", "Mail center", "📮", sort_order=26),
            Option("bakery", "Bakery", "Fresh bread", "🍞", sort_order=27),
            Option("grocery_store", "Grocery Store", "Food shopping", "🛒", sort_order=28),
            Option("restaurant", "Restaurant", "Eating out", "🍽️", sort_order=29),
            Option("pet_store", "Pet Store", "Animals for sale", "🐾", sort_order=30),
        ]
    )
    
    # ============================================================
    # ALL GROUPS REGISTRY
    # ============================================================
    ALL_GROUPS = [
        LANGUAGES,
        VOICES,
        ACCENTS,
        ANIMALS,
        BIRDS,
        FRUITS,
        VEGETABLES,
        COUNTRIES,
        COLORS,
        OCCUPATIONS,
        SPORTS,
        FLOWERS,
        VEHICLES,
        CAMERA_ANGLES,
        LIGHTING_STYLES,
        ART_STYLES,
        ANIMATION_STYLES,
        ASPECT_RATIOS,
        QUALITY_PRESETS,
        RESOLUTIONS,
        EMOTIONS,
        AGE_GROUPS,
        STORY_GENRES,
        STORY_LENGTHS,
        STORY_STYLES,
        STORY_THEMES,
        STORY_SETTINGS,
        ENDING_STYLES,
        CONFLICT_TYPES,
        REWARDS,
        PROBLEMS,
        SOLUTIONS,
        MAGICAL_ELEMENTS,
        ISLAMIC_VALUES,
        DUAS,
        SPACE_VEHICLES,
        MISSIONS,
        FUNNY_SITUATIONS,
        MYSTERIES,
        CLUES,
        VIDEO_DURATIONS,
        FPS_OPTIONS,
        TRANSITIONS,
        CAMERA_MOVEMENTS,
        MUSIC_STYLES,
        VOICE_STYLES,
        NARRATION_STYLES,
        LEARNING_LEVELS,
        WORKSHEET_TYPES,
        QUIZ_TYPES,
        REWARD_TYPES,
        ALPHABET_STYLES,
        CURRICULUM_STANDARDS,
        READING_LEVELS,
        BODY_PARTS,
        WEATHER_CONDITIONS,
        SEASONS,
        MONTHS,
        DAYS_OF_WEEK,
        SHAPES,
        PLANETS,
        CONTINENTS,
        HABITATS,
        TRANSPORT_TYPES,
        RENDER_ENGINES,
        TEXTURES,
        COMPOSITION_RULES,
        COLOR_PALETTES,
        MOODS,
        EXPRESSIONS,
        HAIR_STYLES,
        HAIR_COLORS,
        EYE_COLORS,
        ACCESSORIES,
        CLOTHING,
        FOODS,
        DRINKS,
        INSTRUMENTS,
        FESTIVALS,
        RELIGIONS,
        PROFESSIONS,
        # New Education Support Groups
        COUNTING_OBJECTS,
        COUNTING_STYLES,
        NUMBER_TYPES,
        MATH_OPERATIONS,
        TEACHING_STYLES,
        VOCABULARY_LEVELS,
        DIETS,
        ANIMAL_TYPES,
        NEST_TYPES,
        FLYING_STYLES,
        FUEL_TYPES,
        BODY_FUNCTIONS,
        HEALTHY_HABITS,
        DAILY_ROUTINES,
        OPPOSITE_PAIRS,
        PHONICS_SOUNDS,
        QUIZ_TOPICS,
        QUIZ_DIFFICULTY,
        GROWING_PLACES,
        ENVIRONMENTS,
    ]
    
    # Build lookup dictionaries
    _GROUP_BY_NAME: Dict[str, OptionGroup] = {g.name: g for g in ALL_GROUPS}
    _OPTION_BY_VALUE: Dict[str, Option] = {}
    for group in ALL_GROUPS:
        for option in group.options:
            _OPTION_BY_VALUE[option.value] = option
    
    @classmethod
    def get_group(cls, name: str) -> Optional[OptionGroup]:
        """Get an option group by name."""
        return cls._GROUP_BY_NAME.get(name)
    
    @classmethod
    def get_option(cls, value: str) -> Optional[Option]:
        """Get an option by its value."""
        return cls._OPTION_BY_VALUE.get(value)
    
    @classmethod
    def get_options_for_group(cls, group_name: str) -> List[Option]:
        """Get all options for a group."""
        group = cls.get_group(group_name)
        return group.options if group else []
    
    @classmethod
    def get_all_groups(cls) -> List[OptionGroup]:
        """Get all option groups."""
        return cls.ALL_GROUPS
    
    @classmethod
    def get_group_names(cls) -> List[str]:
        """Get all group names."""
        return [g.name for g in cls.ALL_GROUPS]
    
    @classmethod
    def search_options(cls, query: str, group_name: Optional[str] = None) -> List[Option]:
        """Search options by label or value."""
        query = query.lower()
        results = []
        groups = [cls.get_group(group_name)] if group_name else cls.ALL_GROUPS
        for group in groups:
            if group:
                for option in group.options:
                    if query in option.value.lower() or query in option.label.lower():
                        results.append(option)
        return results
    
    @classmethod
    def get_dropdown_data(cls, group_name: str) -> List[Dict[str, str]]:
        """Get options formatted for dropdown UI."""
        group = cls.get_group(group_name)
        if not group:
            return []
        return [
            {
                "value": opt.value,
                "label": opt.label,
                "description": opt.description,
                "icon": opt.icon,
            }
            for opt in group.options
        ]


# Convenience function for quick access
def get_options(group_name: str) -> List[Dict[str, str]]:
    """Quick access to dropdown-formatted options."""
    return OptionLibrary.get_dropdown_data(group_name)


def get_all_group_names() -> List[str]:
    """Get all available group names."""
    return OptionLibrary.get_group_names()