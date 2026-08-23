'''Template Registry for AI Kids Studio Pro.

This module provides a registry for prompt templates organized by category.
'''

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.prompt.variable_registry import VariableRegistry, VariableDefinition

logger = logging.getLogger(__name__)


@dataclass
class TemplateDefinition:
    '''Definition of a prompt template.'''
    name: str
    category: str
    description: str
    template: str
    variables: List[str] = field(default_factory=list)
    version: str = "3.0"
    difficulty: str = "medium"
    tags: List[str] = field(default_factory=list)
    output_type: str = "story"


class TemplateRegistry:
    '''Registry for managing prompt templates organized by category.'''

    def __init__(self, variable_registry: Optional[VariableRegistry] = None) -> None:
        self._templates: Dict[str, Dict[str, TemplateDefinition]] = {}
        self._variable_registry = variable_registry or VariableRegistry()
        self._register_builtin_templates()

    def _register_builtin_templates(self) -> None:
        '''Register all built-in professional prompt templates.'''
        # ============================================================
        # EDUCATION CATEGORY (18 templates)
        # ============================================================
        education_templates = [
            TemplateDefinition(
                name='ABC Learning',
                category='Education',
                description='Create a fun educational lesson for children learning the alphabet.',
                template='''Create a fun educational lesson for children learning the alphabet.

Letter: {{letter}}
Animal: {{animal}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the letter and animal
- Learning section with pronunciation
- Interactive activity
- Mini quiz
- Outro with encouragement''',
                variables=['letter', 'animal', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Numbers Learning',
                category='Education',
                description='Create a fun educational lesson for children learning numbers.',
                template='''Create a fun educational lesson for children learning numbers.

Number: {{number}}
Object: {{object}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the number and object
- Counting practice
- Visual counting activity
- Number recognition quiz
- Outro with encouragement''',
                variables=['number', 'object', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Colors Learning',
                category='Education',
                description='Create a fun educational lesson for children learning colors.',
                template='''Create a fun educational lesson for children learning colors.

Color: {{color}}
Object: {{object}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the color and object
- Color recognition activity
- Color mixing fun fact
- Find the color game
- Outro with encouragement''',
                variables=['color', 'object', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Shapes Learning',
                category='Education',
                description='Create a fun educational lesson for children learning shapes.',
                template='''Create a fun educational lesson for children learning shapes.

Shape: {{shape}}
Object: {{object}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the shape and real-world object
- Shape recognition activity
- Shape tracing activity
- Find the shape game
- Outro with encouragement''',
                variables=['shape', 'object', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Animals Learning',
                category='Education',
                description='Create a fun educational lesson for children learning about animals.',
                template='''Create a fun educational lesson for children learning about animals.

Animal: {{animal}}
Habitat: {{habitat}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the animal and habitat
- Fun facts about the animal
- Animal sound activity
- Animal movement game
- Outro with encouragement''',
                variables=['animal', 'habitat', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Birds Learning',
                category='Education',
                description='Create a fun educational lesson for children learning about birds.',
                template='''Create a fun educational lesson for children learning about birds.

Bird: {{bird}}
Habitat: {{habitat}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the bird and habitat
- Bird sound imitation activity
- Feather and beak facts
- Bird watching tip
- Outro with encouragement''',
                variables=['bird', 'habitat', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Fruits Learning',
                category='Education',
                description='Create a fun educational lesson for children learning about fruits.',
                template='''Create a fun educational lesson for children learning about fruits.

Fruit: {{fruit}}
Color: {{color}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the fruit and color
- Taste and texture description
- Healthy eating fact
- Fruit tasting activity
- Outro with encouragement''',
                variables=['fruit', 'color', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Vegetables Learning',
                category='Education',
                description='Create a fun educational lesson for children learning about vegetables.',
                template='''Create a fun educational lesson for children learning about vegetables.

Vegetable: {{vegetable}}
Color: {{color}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the vegetable and color
- How it grows (underground/above ground)
- Healthy eating fact
- Vegetable tasting activity
- Outro with encouragement''',
                variables=['vegetable', 'color', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Vehicles Learning',
                category='Education',
                description='Create a fun educational lesson for children learning about vehicles.',
                template='''Create a fun educational lesson for children learning about vehicles.

Vehicle: {{vehicle}}
Type: {{transport_type}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the vehicle and type
- Sound the vehicle makes
- Where it travels (road, sky, water)
- Vehicle spotting game
- Outro with encouragement''',
                variables=['vehicle', 'transport_type', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Body Parts',
                category='Education',
                description='Create a fun educational lesson for children learning body parts.',
                template='''Create a fun educational lesson for children learning body parts.

Body Part: {{body_part}}
Function: {{function}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the body part and function
- Point and name activity
- Movement activity using that body part
- Fun fact about the body part
- Outro with encouragement''',
                variables=['body_part', 'function', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Months',
                category='Education',
                description='Create a fun educational lesson for children learning the months of the year.',
                template='''Create a fun educational lesson for children learning the months of the year.

Month: {{month}}
Season: {{season}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the month and season
- Special events/holidays in this month
- Weather and clothing for this month
- Month order activity
- Outro with encouragement''',
                variables=['month', 'season', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Days',
                category='Education',
                description='Create a fun educational lesson for children learning the days of the week.',
                template='''Create a fun educational lesson for children learning the days of the week.

Day: {{day}}
Activity: {{activity}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the day and typical activity
- Weekday vs weekend explanation
- Daily routine activity
- Day order game
- Outro with encouragement''',
                variables=['day', 'activity', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Opposites',
                category='Education',
                description='Create a fun educational lesson for children learning opposites.',
                template='''Create a fun educational lesson for children learning opposites.

Opposite Pair: {{opposite_pair}}
Example: {{example}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the opposite pair
- Visual comparison activity
- Real-world examples
- Opposite matching game
- Outro with encouragement''',
                variables=['opposite_pair', 'example', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Phonics',
                category='Education',
                description='Create a fun phonics lesson for children learning letter sounds.',
                template='''Create a fun phonics lesson for children learning letter sounds.

Letter: {{letter}}
Sound: {{sound}}
Word Example: {{word_example}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the letter and sound
- Sound pronunciation practice
- Word building activity
- Rhyming words game
- Outro with encouragement''',
                variables=['letter', 'sound', 'word_example', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Spelling',
                category='Education',
                description='Create a fun spelling lesson for children.',
                template='''Create a fun spelling lesson for children.

Word: {{word}}
Difficulty: {{difficulty}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction with the word
- Letter-by-letter spelling
- Phonetic breakdown
- Spelling practice activity
- Spelling bee challenge
- Outro with encouragement''',
                variables=['word', 'difficulty', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Math Quiz',
                category='Education',
                description='Create a fun math quiz for children.',
                template='''Create a fun math quiz for children.

Topic: {{topic}}
Difficulty: {{difficulty}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction to the math topic
- 3-5 practice problems
- Step-by-step solutions
- Fun math fact
- Encouraging outro''',
                variables=['topic', 'difficulty', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Science Quiz',
                category='Education',
                description='Create a fun science quiz for children.',
                template='''Create a fun science quiz for children.

Topic: {{topic}}
Difficulty: {{difficulty}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction to the science topic
- 3-5 quiz questions with multiple choice
- Explanations for each answer
- Fun science fact
- Encouraging outro''',
                variables=['topic', 'difficulty', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='GK Quiz',
                category='Education',
                description='Create a fun general knowledge quiz for children.',
                template='''Create a fun general knowledge quiz for children.

Topic: {{topic}}
Difficulty: {{difficulty}}
Age Group: {{age_group}}
Language: {{language}}
Voice: {{voice}}
Output Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Introduction to the topic
- 5 quiz questions with multiple choice
- Explanations for each answer
- Fun fact related to the topic
- Encouraging outro''',
                variables=['topic', 'difficulty', 'age_group', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
        ]

        # ============================================================
        # STORIES CATEGORY (10 templates)
        # ============================================================
        stories_templates = [
            TemplateDefinition(
                name="Bedtime Story",
                category="Stories",
                description="Create a soothing bedtime story for children with calm pacing, gentle imagery, and a reassuring moral tone.",
                template='''Create a soothing bedtime story for children.
    
Title: {{bedtime_title}}
Main Character: {{story_main_character}}
Companion: {{story_companion}}
Setting: {{setting}}
Theme: {{theme}}
Story Length: {{story_length}}
Reading Level: {{reading_level}}
Moral Lesson: {{story_moral_lesson}}
Language: {{language}}
Voice: {{voice}}
Age Group: {{age_group}}
Art Style: {{art_style}}
Animation Style: {{animation_style}}
Background: {{story_background}}
Duration: {{duration}}
Quality: {{quality}}
    
Instructions:
- Story objective: craft a calming bedtime narrative that helps children relax and feel safe.
- Beginning: introduce the main character, companion, and setting with gentle detail.
- Middle: build a soothing journey with consistent characters and sensory-rich descriptions.
- Ending: conclude with a peaceful resolution and a bedtime transition.
- Character consistency: keep personalities and actions stable.
- Dialogue guidance: use kind, simple dialogue suited for bedtime.
- Educational value: weave in a gentle lesson about rest, kindness, or courage.
- Age adaptation: match tone and vocabulary to the age group.
- Rich descriptions: describe sounds, colors, and textures softly.
- Natural English: use clear, smooth language.
- AI optimized wording: keep instructions structured and specific.''',
                variables=["bedtime_title", "story_main_character", "story_companion", "setting", "theme", "story_length", "reading_level", "story_moral_lesson", "language", "voice", "age_group", "art_style", "animation_style", "story_background", "duration", "quality"],
                version="3.0",
                difficulty="easy",
                tags=["bedtime", "calm", "sleep", "story", "children"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Moral Story",
                category="Stories",
                description="Create a thought-provoking moral story for children with clear values and a meaningful ending.",
                template='''Create a moral story for children.
    
Title: {{moral_title}}
Main Character: {{story_main_character}}
Supporting Character: {{story_supporting_character}}
Setting: {{setting}}
Theme: {{theme}}
Moral Lesson: {{story_moral_lesson}}
Conflict: {{conflict}}
Ending Style: {{ending_style}}
Language: {{language}}
Voice: {{voice}}
Age Group: {{age_group}}
Quality: {{quality}}
    
Instructions:
- Story objective: deliver a strong moral lesson through a relatable childhood story.
- Beginning: introduce characters, setting, and the moral dilemma.
- Middle: develop the conflict and show character growth with consistency.
- Ending: provide a satisfying resolution that reinforces the lesson.
- Character consistency: keep both main and supporting characters true to their roles.
- Dialogue guidance: use clear, age-appropriate dialogue that reveals motives.
- Educational value: focus on empathy, honesty, or respect.
- Age adaptation: keep tone and vocabulary appropriate to the age group.
- Rich descriptions: describe emotions, actions, and setting vividly.
- Natural English: make the narrative smooth and easy to read.
- AI optimized wording: keep the prompt structured and purpose-driven.''',
                variables=["moral_title", "story_main_character", "story_supporting_character", "setting", "theme", "story_moral_lesson", "conflict", "ending_style", "language", "voice", "age_group", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["moral", "lesson", "values", "story", "children"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Adventure Story",
                category="Stories",
                description="Create an action-packed adventure story for children with an inspiring hero journey and exciting obstacles.",
                template='''Create an adventure story for children.
    
Title: {{adventure_title}}
Hero: {{story_hero}}
Sidekick: {{story_sidekick}}
Villain: {{story_villain}}
Mission: {{mission}}
Setting: {{setting}}
Obstacle: {{story_obstacle}}
Reward: {{reward}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: create an exciting hero adventure with clear stakes and progress.
- Beginning: introduce the hero, sidekick, setting, and mission.
- Middle: build tension through obstacles and consistent character choices.
- Ending: resolve the mission with a satisfying reward.
- Character consistency: keep hero, sidekick, and villain traits stable.
- Dialogue guidance: use adventurous and age-appropriate dialogue.
- Educational value: highlight bravery, teamwork, or problem-solving.
- Age adaptation: choose vocabulary and pacing for young readers.
- Rich descriptions: describe action scenes, settings, and emotions vividly.
- Natural English: maintain readability and flow.
- AI optimized wording: keep the prompt focused and structured.''',
                variables=["adventure_title", "story_hero", "story_sidekick", "story_villain", "mission", "setting", "story_obstacle", "reward", "language", "voice", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["adventure", "hero", "story", "children", "action"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Fairy Tale",
                category="Stories",
                description="Create a magical fairy tale for children with royal characters, enchanted elements, and a joyful ending.",
                template='''Create a fairy tale for children.
    
Title: {{fairy_tale_title}}
Princess: {{story_princess}}
Prince: {{story_prince}}
Magical Character: {{story_magical_character}}
Magical Element: {{magical_element}}
Kingdom: {{story_kingdom}}
Villain: {{story_villain}}
Ending Style: {{ending_style}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: craft a whimsical fairy tale with a magical journey and happy ending.
- Beginning: introduce the royal characters, kingdom, and enchanted element.
- Middle: develop a challenge with the villain and magical support.
- Ending: resolve the story with a joyful, fairy tale conclusion.
- Character consistency: keep royal and magical characters true to their roles.
- Dialogue guidance: use charming, age-appropriate speech.
- Educational value: show kindness, courage, or friendship.
- Age adaptation: keep descriptions simple but enchanting.
- Rich descriptions: portray magical sights, sounds, and settings vividly.
- Natural English: make the narrative flow smoothly.
- AI optimized wording: keep the prompt clear and story-driven.''',
                variables=["fairy_tale_title", "story_princess", "story_prince", "story_magical_character", "magical_element", "story_kingdom", "story_villain", "ending_style", "language", "voice", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["fairy tale", "magic", "princess", "children", "story"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Islamic Story",
                category="Stories",
                description="Create an Islamic story for children that teaches values through a respectful and uplifting narrative.",
                template='''Create an Islamic story for children.
    
Title: {{islamic_title}}
Prophet or Personality: {{story_prophet_or_personality}}
Islamic Value: {{islamic_value}}
Location: {{story_location}}
Lesson: {{story_lesson}}
Dua: {{dua}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: present an Islamic moral story that is respectful and educational.
- Beginning: introduce the character, setting, and the value to explore.
- Middle: show the character applying the Islamic value through a challenge.
- Ending: conclude with a positive lesson and dua or blessing.
- Character consistency: keep the protagonist's behavior aligned with Islamic values.
- Dialogue guidance: use respectful and simple language.
- Educational value: focus on faith, kindness, gratitude, or respect.
- Age adaptation: keep narrative appropriate for the target children.
- Rich descriptions: describe setting, emotions, and actions clearly.
- Natural English: ensure the story reads smoothly.
- AI optimized wording: keep the prompt structured and clear.''',
                variables=["islamic_title", "story_prophet_or_personality", "islamic_value", "story_location", "story_lesson", "dua", "language", "voice", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["Islamic", "moral", "story", "children", "values"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Jungle Story",
                category="Stories",
                description="Create an adventurous jungle story for children with animal friends, nature challenges, and a positive lesson.",
                template='''Create a jungle story for children.
    
Title: {{jungle_title}}
Main Animal: {{main_animal}}
Animal Friend: {{animal_friend}}
Habitat: {{habitat}}
Problem: {{problem}}
Solution: {{solution}}
Lesson: {{story_lesson}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: craft an engaging jungle adventure with a meaningful lesson.
- Beginning: introduce the main animal, friend, and jungle habitat.
- Middle: build the problem and show how teamwork leads to a solution.
- Ending: conclude with a positive lesson and celebration.
- Character consistency: keep animal personalities stable and believable.
- Dialogue guidance: use playful, clear dialogue suitable for children.
- Educational value: highlight friendship, cooperation, or nature respect.
- Age adaptation: keep vocabulary and pacing suitable for young readers.
- Rich descriptions: paint the jungle setting with vivid sensory details.
- Natural English: make the narrative flow naturally.
- AI optimized wording: keep the prompt focused and structured.''',
                variables=["jungle_title", "main_animal", "animal_friend", "habitat", "problem", "solution", "story_lesson", "language", "voice", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["jungle", "animals", "adventure", "story", "children"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Space Story",
                category="Stories",
                description="Create a thrilling space story for children with exploration, alien encounters, and inspiring discoveries.",
                template='''Create a space story for children.
    
Title: {{space_title}}
Astronaut: {{story_astronaut}}
Space Vehicle: {{space_vehicle}}
Planet: {{planet}}
Alien: {{story_alien}}
Mission: {{mission}}
Discovery: {{story_discovery}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: write a space adventure that inspires curiosity and wonder.
- Beginning: introduce the astronaut, spaceship, and mission.
- Middle: show the journey, alien encounter, and discovery.
- Ending: conclude with a safe return or hopeful future.
- Character consistency: keep the astronaut and alien personalities coherent.
- Dialogue guidance: use clear and imaginative dialogue.
- Educational value: incorporate science, teamwork, or exploration themes.
- Age adaptation: adjust language for the target age group.
- Rich descriptions: describe planets, space vehicles, and alien worlds vividly.
- Natural English: ensure the narrative is easy to read.
- AI optimized wording: keep the prompt concise and structured.''',
                variables=["space_title", "story_astronaut", "space_vehicle", "planet", "story_alien", "mission", "story_discovery", "language", "voice", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["space", "adventure", "story", "children", "science"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Funny Story",
                category="Stories",
                description="Create a funny story for children with playful characters, humorous situations, and a light-hearted ending.",
                template='''Create a funny story for children.
    
Title: {{funny_title}}
Main Character: {{story_main_character}}
Funny Friend: {{story_funny_friend}}
Funny Situation: {{funny_situation}}
Setting: {{setting}}
Ending: {{story_ending}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: deliver a playful, amusing story with a gentle lesson.
- Beginning: introduce the characters and the humorous setup.
- Middle: build the funny situation with consistent actions and reactions.
- Ending: wrap up with a cheerful resolution.
- Character consistency: keep characters behaving in believable, funny ways.
- Dialogue guidance: use light, age-appropriate humor.
- Educational value: include a lesson about friendship, kindness, or creativity.
- Age adaptation: choose language suitable for young readers.
- Rich descriptions: describe funny actions and expressions vividly.
- Natural English: keep the narrative clear and readable.
- AI optimized wording: keep the prompt structured and specific.''',
                variables=["funny_title", "story_main_character", "story_funny_friend", "funny_situation", "setting", "story_ending", "language", "voice", "quality"],
                version="3.0",
                difficulty="easy",
                tags=["funny", "humor", "story", "children", "playful"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Mystery Story",
                category="Stories",
                description="Create a suspenseful mystery story for children with clues, investigation, and a clever resolution.",
                template='''Create a mystery story for children.
    
Title: {{mystery_title}}
Detective: {{story_detective}}
Assistant: {{story_assistant}}
Mystery: {{mystery}}
Clues: {{clues}}
Setting: {{setting}}
Ending: {{story_ending}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: write a child-friendly mystery with clues and resolution.
- Beginning: introduce the detective, assistant, and mysterious situation.
- Middle: gather clues and build suspense while keeping characters consistent.
- Ending: resolve the mystery clearly and satisfyingly.
- Character consistency: keep the detective and assistant roles steady.
- Dialogue guidance: use clear, curious dialogue appropriate for children.
- Educational value: emphasize observation, reasoning, or honesty.
- Age adaptation: keep vocabulary and pacing suitable for the target age.
- Rich descriptions: describe settings, clues, and emotions vividly.
- Natural English: make the story flow naturally.
- AI optimized wording: keep the prompt focused and structured.''',
                variables=["mystery_title", "story_detective", "story_assistant", "mystery", "clues", "setting", "story_ending", "language", "voice", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["mystery", "detective", "story", "children", "puzzle"],
                output_type="story"
            ),
            TemplateDefinition(
                name="Custom Story",
                category="Stories",
                description="Create a custom story for children with the desired characters, theme, and story length.",
                template='''Create a custom story for children.
    
Title: {{story_title}}
Main Character: {{story_main_character}}
Supporting Character: {{story_supporting_character}}
Setting: {{setting}}
Theme: {{theme}}
Genre: {{genre}}
Story Length: {{story_length}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
    
Instructions:
- Story objective: craft a personalized story using the provided elements.
- Beginning: introduce the main and supporting characters in the setting.
- Middle: develop the plot with consistent character actions.
- Ending: deliver a satisfying conclusion that fits the genre.
- Character consistency: keep main and supporting characters coherent.
- Dialogue guidance: use natural, expressive, and age-appropriate dialogue.
- Educational value: include a lesson or positive takeaway if possible.
- Age adaptation: tailor tone and vocabulary to the age group.
- Rich descriptions: describe settings, emotions, and key moments vividly.
- Natural English: ensure the narrative reads smoothly.
- AI optimized wording: keep the prompt clear and structured.''',
                variables=["story_title", "story_main_character", "story_supporting_character", "setting", "theme", "genre", "story_length", "language", "voice", "quality"],
                version="3.0",
                difficulty="medium",
                tags=["custom", "story", "children", "creative"],
                output_type="story"
            ),
        ]

        # ============================================================
        # IMAGES CATEGORY (11 templates) - PRODUCTION REWRITE v3.0
        # ============================================================
        images_templates = [
            TemplateDefinition(
                name='Image Prompt',
                category='Images',
                description='Create a professional, production-ready image generation prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.',
                template='''Create a professional image generation prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Subject: {{subject}}
Environment: {{environment}}
Art Style: {{art_style}}
Lighting: {{lighting}}
Camera Angle: {{camera_angle}}
Mood: {{mood}}
Color Palette: {{color_palette}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}
Background: {{background}}
Negative Prompt: {{negative_prompt}}

Instructions:
- Generate a highly detailed, production-ready prompt with professional composition
- Include rich descriptive details for subject, environment, and atmosphere
- Specify professional lighting setup (key, fill, rim, ambient)
- Define camera perspective with technical precision (lens, focal length, aperture)
- Apply color theory for harmonious palette with mood alignment
- Include quality modifiers for maximum sharpness, detail, and resolution
- Add negative prompt for artifact prevention and quality control
- Optimize wording for all major image generation models (DALL·E, Midjourney, SD, Flux, Ideogram)
- Ensure visual storytelling through composition, depth, and narrative elements''',
                variables=['subject', 'environment', 'art_style', 'lighting', 'camera_angle', 'mood', 'color_palette', 'quality', 'aspect_ratio', 'background', 'negative_prompt'],
                version="3.0",
                difficulty="medium",
                tags=["image", "prompt", "generation", "professional", "dalle", "midjourney", "stable-diffusion", "flux", "ideogram"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Disney Style',
                category='Images',
                description='Create a Disney-style character or scene prompt with classic animation aesthetics, magical atmosphere, and production-quality detail.',
                template='''Create a Disney-style character or scene prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Character: {{character}}
Environment: {{environment}}
Expression: {{expression}}
Pose: {{pose}}
Lighting: {{lighting}}
Color Palette: {{color_palette}}
Background: {{background}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- Large, expressive eyes with catchlights and depth
- Rounded, soft facial features with subtle cheek definition
- Vibrant, saturated color palette with magical glow accents
- Sparkle and pixie dust particle effects
- Whimsical, storybook background with atmospheric perspective
- Classic Disney Renaissance animation style (1989-1999 aesthetic)
- Hand-drawn cel animation texture with clean linework
- Expressive silhouette and clear character staging
- Emotional storytelling through pose and expression
- Professional composition with rule of thirds and depth layers

Instructions:
- Generate a production-ready Disney-style prompt with professional composition
- Include rich character design details: anatomy, costume, personality
- Specify magical lighting: warm key light, cool fill, rim highlights, sparkle accents
- Define color harmony: analogous palette with complementary accents
- Add atmospheric depth: foreground, midground, background separation
- Include quality modifiers: 8K, masterpiece, Disney animation style, clean lines
- Optimize for all major image models with structured, descriptive language''',
                variables=['character', 'environment', 'expression', 'pose', 'lighting', 'color_palette', 'background', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="medium",
                tags=["disney", "animation", "character", "magical", "whimsical", "cel-animation", "renaissance"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Pixar Style',
                category='Images',
                description='Create a Pixar-style character or scene prompt with cinematic rendering, emotional storytelling, and production-quality 3D aesthetics.',
                template='''Create a Pixar-style character or scene prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Character: {{character}}
Emotion: {{emotion}}
Environment: {{environment}}
Camera Angle: {{camera_angle}}
Lighting: {{lighting}}
Animation Style: {{animation_style}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- Subsurface scattering (SSS) for realistic skin/fur translucency
- Expressive facial rigging with micro-expressions and eye detail
- Cinematic lighting: three-point setup with volumetric atmosphere
- Detailed material textures: fur grooming, fabric weave, metal wear
- Emotional storytelling pose with clear silhouette and weight
- Volumetric fog, dust motes, and atmospheric perspective
- Stylized proportions with appeal: exaggerated features, readable shapes
- RenderMan/Arnold/Octane quality: global illumination, caustics, DOF
- Color scripting for emotional beats: warm/cool contrast
- Composition: rule of thirds, leading lines, depth of field

Instructions:
- Generate a production-ready Pixar-style prompt with cinematic quality
- Include technical render specs: SSS, displacement, groom, shading networks
- Specify emotional acting: facial action coding, body language, timing
- Define lighting mood: key-to-fill ratio, color temperature, motivation
- Add material fidelity: specular roughness, anisotropy, clearcoat
- Include quality modifiers: 8K, masterpiece, Pixar render style, cinematic
- Optimize for all major image models with structured, technical language''',
                variables=['character', 'emotion', 'environment', 'camera_angle', 'lighting', 'animation_style', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="hard",
                tags=["pixar", "3d", "animation", "cinematic", "subsurface-scattering", "rendering", "emotional"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Realistic Portrait',
                category='Images',
                description='Create a photorealistic portrait prompt with professional photography specifications, accurate lighting, and camera technical details.',
                template='''Create a photorealistic portrait prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Person: {{person}}
Age: {{age}}
Gender: {{gender}}
Ethnicity: {{ethnicity}}
Hairstyle: {{hairstyle}}
Clothing: {{clothing}}
Lighting: {{lighting}}
Camera Angle: {{camera_angle}}
Lens: {{lens}}
Background: {{background}}
Mood: {{mood}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- 8K/16K resolution with extreme detail fidelity
- Photorealistic skin texture: pores, fine hairs, subsurface scattering
- Accurate physics-based rendering: specular, roughness, anisotropy
- Professional lighting setup: Rembrandt, butterfly, split, loop, clamshell
- Camera specifications: full-frame sensor, prime lens (85mm/135mm), f/1.2-f/2.8
- Natural depth of field with creamy bokeh and precise focus plane
- Color grading: cinematic LUT, skin tone accuracy, highlight rolloff
- Raw photo aesthetic: film grain, dynamic range, highlight preservation
- Sharp focus on eyes with catchlight detail
- Composition: rule of thirds, negative space, environmental storytelling

Instructions:
- Generate a production-ready photorealistic portrait prompt
- Include technical camera specs: sensor, lens, aperture, ISO, shutter
- Specify lighting diagram: key/fill/rim ratios, modifiers, color gels
- Define skin rendering: SSS, micro-detail, specular response
- Add post-processing: color grade, film emulation, sharpening
- Include negative prompt: artifacts, distortion, plastic skin, oversharpening
- Optimize for all major image models with photography terminology''',
                variables=['person', 'age', 'gender', 'ethnicity', 'hairstyle', 'clothing', 'lighting', 'camera_angle', 'lens', 'background', 'mood', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="hard",
                tags=["portrait", "photorealistic", "photography", "professional", "camera", "lighting", "skin"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Anime Style',
                category='Images',
                description='Create an anime-style image prompt with authentic Japanese animation aesthetics, cel shading, and dynamic composition.',
                template='''Create an anime-style image prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Character: {{character}}
Anime Style: {{anime_style}}
Pose: {{pose}}
Expression: {{expression}}
Background: {{background}}
Lighting: {{lighting}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- Large expressive eyes with detailed iris, highlights, and gradient
- Stylized hair with defined strands, shine, and movement lines
- Cel shading with hard shadows and 2-3 tone values
- Dynamic action pose with speed lines or impact frames
- Japanese anime aesthetic: 1990s/2000s or modern digital style
- Line art: clean, variable weight, tapered ends
- Color palette: vibrant saturated hues with cel-shaded shadows
- Effects: speed lines, motion blur, glow, particles, screen tones
- Composition: dramatic angles, Dutch tilt, perspective distortion

Instructions:
- Generate a production-ready anime-style prompt with authentic aesthetics
- Specify anime sub-style: shonen, shojo, seinen, isekai, mecha, slice of life
- Define shading technique: cel, soft cel, watercolor, hybrid
- Include line art quality: vector clean, hand-drawn texture, variable width
- Add effects: rim light, bloom, chromatic aberration, film grain
- Specify studio reference for quality benchmark
- Include negative prompt: 3D render, realistic, western cartoon, bad anatomy
- Optimize for all major image models with anime-specific terminology''',
                variables=['character', 'anime_style', 'pose', 'expression', 'background', 'lighting', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="medium",
                tags=["anime", "manga", "japanese", "cel-shading", "animation", "stylized", "dynamic"],
                output_type="image"
            ),
            TemplateDefinition(
                name='3D Cartoon',
                category='Images',
                description='Create a 3D cartoon style image prompt with stylized rendering, vibrant materials, and professional studio quality.',
                template='''Create a 3D cartoon style image prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Character: {{character}}
Animation Style: {{animation_style}}
Environment: {{environment}}
Lighting: {{lighting}}
Camera Angle: {{camera_angle}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- Smooth subdivision surfaces with clean topology
- Vibrant PBR materials: stylized shaders, toon ramp, matte finish
- Subsurface scattering for organic forms (skin, fruit, wax)
- Rim lighting and fresnel highlights for shape definition
- Stylized proportions: exaggerated features, appealing silhouettes
- Studio render quality: Octane, Redshift, Arnold, Blender Cycles, Unreal Engine 5
- Volumetric lighting: god rays, fog, atmospheric scattering
- Color grading: saturated palette, complementary harmony, mood lighting
- Depth of field: cinematic bokeh, focus pulling
- Composition: dynamic camera, rule of thirds, leading lines

Instructions:
- Generate a production-ready 3D cartoon prompt with studio render quality
- Specify render engine and shader setup: toon, PBR stylized, matte
- Define lighting rig: HDRI, area lights, gobos, light linking
- Include material details: roughness maps, normal maps, displacement
- Add post-processing: bloom, color grade, vignette, chromatic aberration
- Specify studio style: Pixar, DreamWorks, Illumination, Blue Sky, Sony
- Include negative prompt: photorealistic, gritty, low poly, jagged edges
- Optimize for all major image models with 3D rendering terminology''',
                variables=['character', 'animation_style', 'environment', 'lighting', 'camera_angle', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="medium",
                tags=["3d", "cartoon", "stylized", "render", "octane", "blender", "unreal", "animation"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Watercolor Painting',
                category='Images',
                description='Create a watercolor painting style prompt with authentic traditional media techniques, paper texture, and artistic composition.',
                template='''Create a watercolor painting style prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Subject: {{subject}}
Environment: {{environment}}
Watercolor Style: {{watercolor_style}}
Color Palette: {{color_palette}}
Paper Texture: {{paper_texture}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- Wet-on-wet blending: soft edges, color bleeding, organic diffusion
- Wet-on-dry technique: controlled edges, glazing, layering
- Paper texture visible: cold press, hot press, rough grain
- Transparent pigment layers: luminosity, depth, glazing effects
- Blooming and cauliflower effects: water margins, pigment separation
- Granulating pigments: sedimentary texture, mineral separation
- Dry brush technique: texture, scumbling, broken color
- Salt/alcohol effects: crystalline patterns, organic textures
- Hand-painted aesthetic: brushstroke visibility, artist's hand
- Composition: negative space, rule of thirds, golden ratio

Instructions:
- Generate a production-ready watercolor prompt with traditional media authenticity
- Specify technique: wet-on-wet, wet-on-dry, dry brush, glazing, lifting
- Define paper: Arches, Fabriano, Saunders Waterford, cold/hot/rough press
- Include pigment behavior: staining, granulating, transparent, opaque
- Add water effects: blooms, backruns, watermarks, hard edges
- Specify color palette: limited palette, split primary, earth tones, jewel tones
- Include negative prompt: digital, vector, flat, plastic, oversaturated, AI artifacts
- Optimize for all major image models with watercolor terminology''',
                variables=['subject', 'environment', 'watercolor_style', 'color_palette', 'paper_texture', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="medium",
                tags=["watercolor", "painting", "traditional", "art", "wet-on-wet", "paper-texture", "hand-painted"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Oil Painting',
                category='Images',
                description='Create an oil painting style prompt with classical techniques, impasto texture, and masterpiece-level composition.',
                template='''Create an oil painting style prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Subject: {{subject}}
Oil Style: {{oil_style}}
Lighting: {{lighting}}
Brush Style: {{brush_style}}
Background: {{background}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- Thick impasto brushstrokes: visible texture, 3D paint relief
- Rich color depth: glazing, scumbling, alla prima, indirect painting
- Canvas texture: linen weave, priming tooth, absorbency
- Layered glazing: transparent layers, luminous color, optical mixing
- Masterpiece quality: museum-grade, archival, timeless
- Brushwork variety: flat, filbert, round, fan, palette knife
- Color temperature: warm/cool contrast, chromatic grays, harmony
- Varnish finish: gloss, satin, matte, regional variation
- Aging effects: craquelure, patina, yellowed varnish (optional)

Instructions:
- Generate a production-ready oil painting prompt with classical technique
- Specify painting method: alla prima (direct), indirect (glazing), mixed
- Define brushwork: expressive, controlled, palette knife, finger blending
- Include underpainting: grisaille, verdaccio, imprimatura, tonal ground
- Add medium: linseed, walnut, poppy, alkyd, stand oil, damar varnish
- Specify art historical reference: Renaissance, Baroque, Impressionism, Realism
- Include negative prompt: digital, flat, plastic, smooth, airbrush, AI artifacts
- Optimize for all major image models with oil painting terminology''',
                variables=['subject', 'oil_style', 'lighting', 'brush_style', 'background', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="hard",
                tags=["oil", "painting", "classical", "impasto", "glazing", "canvas", "masterpiece", "traditional"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Coloring Page',
                category='Images',
                description='Create a professional coloring page prompt with clean line art, age-appropriate complexity, and print-ready quality.',
                template='''Create a professional coloring page prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Object: {{object}}
Theme: {{theme}}
Difficulty: {{difficulty}}
Line Style: {{line_style}}
Page Size: {{page_size}}
Age Group: {{age_group}}

Style Elements:
- Clean, crisp black outlines: consistent weight, no gaps, closed shapes
- Pure white background: no shading, no color, no gradients
- Print-ready line art: 300 DPI, vector-quality edges
- Age-appropriate complexity: simple/medium/intricate detail levels
- Clear distinct shapes: easy color separation, no ambiguous areas
- Balanced composition: focal point, negative space, visual flow
- Educational value: labeled elements, learning opportunity
- Therapeutic design: mindfulness patterns, mandala elements (optional)
- Bleed margin: safe print area, no edge cutoff
- File format ready: PNG transparent, PDF vector, SVG scalable

Instructions:
- Generate a production-ready coloring page prompt for print publication
- Specify line weight: uniform (coloring book) or varied (artistic)
- Define complexity: toddler (large shapes), child (medium), adult (intricate)
- Include theme integration: seasonal, educational, character, abstract
- Add quality modifiers: high contrast, sharp lines, no anti-aliasing artifacts
- Specify page format: US Letter, A4, square, custom dimensions
- Include negative prompt: color, shading, gradient, texture, noise, watermark, text
- Optimize for all major image models with line art terminology''',
                variables=['object', 'theme', 'difficulty', 'line_style', 'page_size', 'age_group'],
                version="3.0",
                difficulty="easy",
                tags=["coloring", "page", "line-art", "print-ready", "children", "educational", "therapeutic"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Sticker Design',
                category='Images',
                description='Create a professional sticker design prompt with die-cut ready outlines, vibrant colors, and production-ready specifications.',
                template='''Create a professional sticker design prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Object: {{object}}
Style: {{style}}
Outline: {{outline}}
Background: {{background}}
Quality: {{quality}}

Style Elements:
- Thick white/colored outline: die-cut ready, 3-5mm bleed margin
- Transparent background: PNG alpha channel, no artifacts
- Cute/chibi proportions: oversized head, small body, appealing silhouette
- Vibrant saturated colors: high contrast, print-friendly CMYK safe
- High contrast design: readable at small sizes (25mm minimum)
- Clean vector-style edges: no feathering, crisp boundaries
- Sticker finish options: matte, glossy, holographic, clear, vinyl
- Character appeal: expressive face, dynamic pose, clear silhouette
- Commercial quality: print production ready, no copyright issues
- Packaging consideration: kiss-cut, die-cut, sheet layout ready

Instructions:
- Generate a production-ready sticker design prompt for commercial printing
- Specify outline color: white, black, colored, holographic, none (clear)
- Define style: kawaii, chibi, minimal, retro, aesthetic, character, logo
- Include bleed specifications: 3mm standard, 5mm for complex shapes
- Add material specs: vinyl, paper, holographic, clear, metallic, kraft
- Specify cut type: kiss-cut (sticker stays on backing), die-cut (individual)
- Include negative prompt: background, watermark, text, signature, gradient mesh
- Optimize for all major image models with sticker production terminology''',
                variables=['object', 'style', 'outline', 'background', 'quality'],
                version="3.0",
                difficulty="medium",
                tags=["sticker", "design", "die-cut", "vinyl", "kawaii", "chibi", "print-ready", "commercial"],
                output_type="image"
            ),
            TemplateDefinition(
                name='Book Illustration',
                category='Images',
                description='Create a children\'s book illustration prompt with narrative composition, text-space consideration, and storybook aesthetic.',
                template='''Create a children's book illustration prompt optimized for DALL·E, Midjourney, Stable Diffusion, Flux, and Ideogram.

Scene: {{scene}}
Character: {{character}}
Environment: {{environment}}
Art Style: {{art_style}}
Lighting: {{lighting}}
Mood: {{mood}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Style Elements:
- Storybook illustration style: narrative composition, page-turn momentum
- Child-friendly characters: appealing, expressive, diverse representation
- Warm inviting atmosphere: emotional connection, comfort, wonder
- Text space consideration: negative space for copy, bleed margins
- Print-ready quality: CMYK color space, 300 DPI, gutter awareness
- Visual storytelling: clear focal point, supporting details, narrative clues
- Consistent style: series cohesion, character model sheets, color script
- Age-appropriate: board book (0-3), picture book (3-7), early reader (6-9)
- Composition: rule of thirds, golden spiral, dynamic symmetry
- Traditional media feel: watercolor, gouache, colored pencil, mixed media

Instructions:
- Generate a production-ready book illustration prompt for publishing
- Specify book format: board book, picture book, chapter book, graphic novel
- Define illustration placement: full bleed, spot, vignette, double-page spread
- Include text integration: header space, footer space, sidebar, overlay areas
- Add style consistency: series bible, character sheets, color palette
- Specify printing: offset, digital, POD, color profile (FOGRA39, SWOP)
- Include negative prompt: photorealistic, dark, scary, cluttered, illegible, watermark
- Optimize for all major image models with publishing terminology''',
                variables=['scene', 'character', 'environment', 'art_style', 'lighting', 'mood', 'quality', 'aspect_ratio'],
                version="3.0",
                difficulty="medium",
                tags=["book", "illustration", "children", "storybook", "publishing", "narrative", "print-ready"],
                output_type="image"
            ),
        ]

        # ============================================================
        # VIDEOS CATEGORY (8 templates)
        # ============================================================
        videos_templates = [
            TemplateDefinition(
                name='Storyboard',
                category='Videos',
                description='Create a storyboard for a video project.',
                template='''Create a storyboard for a video project.

Title: {{title}}
Concept: {{concept}}
Scenes: {{scenes}}
Duration: {{duration}}
Style: {{style}}
Target Audience: {{target_audience}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Storyboard Structure:
- Scene 1: Establishing shot
- Scene 2: Introduction
- Scene 3: Conflict/Action
- Scene 4: Climax
- Scene 5: Resolution
- Scene 6: Call to action/Ending''',
                variables=['title', 'concept', 'scenes', 'duration', 'style', 'target_audience', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Animation Prompt',
                category='Videos',
                description='Create an animation video generation prompt.',
                template='''Create an animation video generation prompt.

Subject: {{subject}}
Action: {{action}}
Style: {{style}}
Duration: {{duration}}
Frame Rate: {{frame_rate}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Animation Details:
- Character movement
- Camera movement
- Transitions
- Effects
- Lighting changes
- Loop considerations''',
                variables=['subject', 'action', 'style', 'duration', 'frame_rate', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Scene Generator',
                category='Videos',
                description='Generate a detailed scene description for video.',
                template='''Generate a detailed scene description for video production.

Scene: {{scene}}
Location: {{location}}
Time: {{time}}
Characters: {{characters}}
Action: {{action}}
Mood: {{mood}}
Lighting: {{lighting}}
Camera: {{camera}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Include:
- Wide establishing shot
- Medium shots
- Close-ups
- Camera movements
- Lighting setup
- Sound cues''',
                variables=['scene', 'location', 'time', 'characters', 'action', 'mood', 'lighting', 'camera', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Camera Shot List',
                category='Videos',
                description='Create a detailed camera shot list for video production.',
                template='''Create a detailed camera shot list for video production.

Project: {{project}}
Scene: {{scene}}
Shots: {{shots}}
Style: {{style}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Shot List Format:
1. Shot Number
2. Shot Type (Wide/Medium/Close-up/Extreme Close-up)
3. Camera Angle (Eye-level/High/Low/Dutch)
4. Camera Movement (Static/Pan/Tilt/Dolly/Tracking)
5. Duration
6. Description
7. Audio Cues''',
                variables=['project', 'scene', 'shots', 'style', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='YouTube Video',
                category='Videos',
                description='Create a YouTube video script and structure.',
                template='''Create a YouTube video script and structure.

Title: {{title}}
Topic: {{topic}}
Target Audience: {{target_audience}}
Duration: {{duration}}
Style: {{style}}
Hook: {{hook}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Video Structure:
- Hook (0-15s): {{hook}}
- Introduction (15-30s)
- Main Content (30s - {{duration}})
- Call to Action
- End Screen Elements''',
                variables=['title', 'topic', 'target_audience', 'duration', 'style', 'hook', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Short Video',
                category='Videos',
                description='Create a short-form video script (TikTok/Reels/Shorts).',
                template='''Create a short-form video script (TikTok/Reels/Shorts).

Topic: {{topic}}
Hook: {{hook}}
Format: {{format}}
Duration: {{duration}}
Style: {{style}}
Trend: {{trend}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Structure:
- Hook (0-3s): {{hook}}
- Value/Entertainment (3-{{duration}}s)
- Call to Action (last 3s)
- Hashtags: {{hashtags}}''',
                variables=['topic', 'hook', 'format', 'duration', 'style', 'trend', 'quality', 'aspect_ratio', 'hashtags']
            ),
            TemplateDefinition(
                name='Kids Lesson',
                category='Videos',
                description='Create an educational video lesson for kids.',
                template='''Create an educational video lesson for kids.

Topic: {{topic}}
Age Group: {{age_group}}
Learning Objective: {{learning_objective}}
Duration: {{duration}}
Style: {{style}}
Language: {{language}}
Voice: {{voice}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Lesson Structure:
- Hook/Attention Grabber
- Learning Objective Statement
- Main Teaching Segment
- Interactive Activity
- Review/Quiz
- Summary & Encouragement''',
                variables=['topic', 'age_group', 'learning_objective', 'duration', 'style', 'language', 'voice', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='AI Video Prompt',
                category='Videos',
                description='Create a prompt for AI video generation (Sora, Runway, Pika, etc.).',
                template='''Create a prompt for AI video generation (Sora, Runway, Pika, etc.).

Subject: {{subject}}
Action: {{action}}
Environment: {{environment}}
Style: {{style}}
Camera: {{camera}}
Lighting: {{lighting}}
Duration: {{duration}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Prompt Structure:
- Subject description
- Action/movement
- Environment/setting
- Cinematic style
- Camera specifications
- Lighting mood
- Technical parameters''',
                variables=['subject', 'action', 'environment', 'style', 'camera', 'lighting', 'duration', 'quality', 'aspect_ratio']
            ),
        ]

        # ============================================================
        # VOICES CATEGORY (7 templates)
        # ============================================================
        voices_templates = [
            TemplateDefinition(
                name='Narration',
                category='Voices',
                description='Create a narration voiceover script.',
                template='''Create a narration voiceover script.

Content: {{content}}
Tone: {{tone}}
Pace: {{pace}}
Language: {{language}}
Voice: {{voice}}
Duration: {{duration}}
Quality: {{quality}}

Narration Style:
- Clear articulation
- Appropriate pacing
- Emotional connection
- Professional delivery
- Consistent tone''',
                variables=['content', 'tone', 'pace', 'language', 'voice', 'duration', 'quality']
            ),
            TemplateDefinition(
                name='Kids Voice',
                category='Voices',
                description='Create a child-friendly voiceover script.',
                template='''Create a child-friendly voiceover script.

Content: {{content}}
Character: {{character}}
Age: {{age}}
Language: {{language}}
Voice: {{voice}}
Tone: {{tone}}
Duration: {{duration}}
Quality: {{quality}}

Kids Voice Style:
- Warm and friendly
- Clear pronunciation
- Engaging energy
- Age-appropriate vocabulary
- Encouraging tone''',
                variables=['content', 'character', 'age', 'language', 'voice', 'tone', 'duration', 'quality']
            ),
            TemplateDefinition(
                name='Teacher Voice',
                category='Voices',
                description='Create an educational teacher voiceover script.',
                template='''Create an educational teacher voiceover script.

Topic: {{topic}}
Grade Level: {{grade_level}}
Language: {{language}}
Voice: {{voice}}
Tone: {{tone}}
Duration: {{duration}}
Quality: {{quality}}

Teacher Voice Style:
- Authoritative yet warm
- Clear explanations
- Encouraging feedback
- Paced for comprehension
- Interactive questioning''',
                variables=['topic', 'grade_level', 'language', 'voice', 'tone', 'duration', 'quality']
            ),
            TemplateDefinition(
                name='Story Voice',
                category='Voices',
                description='Create a storytelling voiceover script.',
                template='''Create a storytelling voiceover script.

Story: {{story}}
Character Voices: {{character_voices}}
Narrator Style: {{narrator_style}}
Language: {{language}}
Voice: {{voice}}
Duration: {{duration}}
Quality: {{quality}}

Storytelling Style:
- Expressive narration
- Character differentiation
- Emotional range
- Pacing for tension
- Immersive atmosphere''',
                variables=['story', 'character_voices', 'narrator_style', 'language', 'voice', 'duration', 'quality']
            ),
            TemplateDefinition(
                name='Podcast',
                category='Voices',
                description='Create a podcast episode script.',
                template='''Create a podcast episode script.

Title: {{title}}
Topic: {{topic}}
Host: {{host}}
Guest: {{guest}}
Format: {{format}}
Language: {{language}}
Voice: {{voice}}
Duration: {{duration}}
Quality: {{quality}}

Podcast Structure:
- Intro music & hook
- Host introduction
- Main discussion/Interview
- Key takeaways
- Call to action
- Outro music''',
                variables=['title', 'topic', 'host', 'guest', 'format', 'language', 'voice', 'duration', 'quality']
            ),
            TemplateDefinition(
                name='Audiobook',
                category='Voices',
                description='Create an audiobook narration script.',
                template='''Create an audiobook narration script.

Book Title: {{book_title}}
Chapter: {{chapter}}
Genre: {{genre}}
Narrator: {{narrator}}
Language: {{language}}
Voice: {{voice}}
Duration: {{duration}}
Quality: {{quality}}

Audiobook Style:
- Consistent narrator voice
- Character voice differentiation
- Proper pacing
- Chapter transitions
- Emotional nuance''',
                variables=['book_title', 'chapter', 'genre', 'narrator', 'language', 'voice', 'duration', 'quality']
            ),
            TemplateDefinition(
                name='Commercial',
                category='Voices',
                description='Create a commercial voiceover script.',
                template='''Create a commercial voiceover script.

Product: {{product}}
Target Audience: {{target_audience}}
Key Benefit: {{key_benefit}}
Call to Action: {{call_to_action}}
Language: {{language}}
Voice: {{voice}}
Tone: {{tone}}
Duration: {{duration}}
Quality: {{quality}}

Commercial Structure:
- Hook (attention)
- Problem/Need
- Solution (product)
- Benefits
- Social proof
- Call to action
- Tagline''',
                variables=['product', 'target_audience', 'key_benefit', 'call_to_action', 'language', 'voice', 'tone', 'duration', 'quality']
            ),
        ]

        # ============================================================
        # YOUTUBE CATEGORY (7 templates)
        # ============================================================
        youtube_templates = [
            TemplateDefinition(
                name='Script Generator',
                category='YouTube',
                description='Generate a complete YouTube video script.',
                template='''Generate a complete YouTube video script.

Title: {{title}}
Topic: {{topic}}
Target Audience: {{target_audience}}
Duration: {{duration}}
Style: {{style}}
Hook: {{hook}}
Quality: {{quality}}

Script Structure:
1. HOOK (0:00-0:15) - {{hook}}
2. INTRO (0:15-1:00) - Channel intro, topic preview
3. MAIN CONTENT (1:00-{{duration}})
    - Point 1 with B-roll suggestions
    - Point 2 with examples
    - Point 3 with tips
4. CALL TO ACTION ({{duration}}-{{duration}}+1:00)
5. END SCREEN (last 20s)''',
                variables=['title', 'topic', 'target_audience', 'duration', 'style', 'hook', 'quality']
            ),
            TemplateDefinition(
                name='Title Generator',
                category='YouTube',
                description='Generate click-worthy YouTube video titles.',
                template='''Generate click-worthy YouTube video titles.

Topic: {{topic}}
Target Audience: {{target_audience}}
Style: {{style}}
Keywords: {{keywords}}
Tone: {{tone}}
Count: {{count}}

Generate {{count}} titles with:
- High CTR potential
- SEO optimized
- Curiosity gap
- Clear value proposition
- {{tone}} tone''',
                variables=['topic', 'target_audience', 'style', 'keywords', 'tone', 'count']
            ),
            TemplateDefinition(
                name='Description Generator',
                category='YouTube',
                description='Generate an SEO-optimized YouTube video description.',
                template='''Generate an SEO-optimized YouTube video description.

Title: {{title}}
Topic: {{topic}}
Keywords: {{keywords}}
Links: {{links}}
Chapters: {{chapters}}
Hashtags: {{hashtags}}
Language: {{language}}

Description Structure:
- First 2 lines: Hook + keywords
- Summary paragraph
- Timestamps/Chapters
- Links & Resources
- Social media
- Hashtags
- Disclaimer (if needed)''',
                variables=['title', 'topic', 'keywords', 'links', 'chapters', 'hashtags', 'language']
            ),
            TemplateDefinition(
                name='SEO Tags',
                category='YouTube',
                description='Generate SEO tags for YouTube videos.',
                template='''Generate SEO tags for YouTube videos.

Topic: {{topic}}
Niche: {{niche}}
Target Audience: {{target_audience}}
Language: {{language}}
Tag Count: {{tag_count}}

Generate {{tag_count}} tags:
- Broad match keywords
- Long-tail keywords
- Related terms
- Trending tags
- Competitor tags
- Branded tags''',
                variables=['topic', 'niche', 'target_audience', 'language', 'tag_count']
            ),
            TemplateDefinition(
                name='Thumbnail Prompt',
                category='YouTube',
                description='Create a prompt for YouTube thumbnail design.',
                template='''Create a prompt for YouTube thumbnail design.

Video Title: {{video_title}}
Main Subject: {{main_subject}}
Expression: {{expression}}
Background: {{background}}
Text: {{text}}
Color Scheme: {{color_scheme}}
Style: {{style}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Thumbnail Elements:
- High contrast
- Expressive face
- Minimal text (3-4 words max)
- Bright colors
- Clear focal point
- Brand consistency''',
                variables=['video_title', 'main_subject', 'expression', 'background', 'text', 'color_scheme', 'style', 'quality', 'aspect_ratio']
            ),
            TemplateDefinition(
                name='Hook Generator',
                category='YouTube',
                description='Generate engaging hooks for YouTube videos.',
                template='''Generate engaging hooks for YouTube videos.

Topic: {{topic}}
Target Audience: {{target_audience}}
Style: {{style}}
Hook Type: {{hook_type}}
Count: {{count}}

Generate {{count}} hooks of type {{hook_type}}:
- Question hook
- Statement hook
- Story hook
- Statistic hook
- Visual hook
- Promise hook''',
                variables=['topic', 'target_audience', 'style', 'hook_type', 'count']
            ),
            TemplateDefinition(
                name='Shorts Script',
                category='YouTube',
                description='Create a YouTube Shorts script.',
                template='''Create a YouTube Shorts script.

Topic: {{topic}}
Hook: {{hook}}
Format: {{format}}
Duration: {{duration}}
Style: {{style}}
Trend: {{trend}}
Quality: {{quality}}
Aspect Ratio: {{aspect_ratio}}

Shorts Structure:
- HOOK (0-3s): {{hook}}
- VALUE (3-{{duration}}s): Quick tip/demo/story
- CTA (last 3s): Subscribe/Follow/Comment
- Hashtags: #Shorts #{{topic}} #{{trend}}''',
                variables=['topic', 'hook', 'format', 'duration', 'style', 'trend', 'quality', 'aspect_ratio']
            ),
        ]

        # ============================================================
        # SOCIAL MEDIA CATEGORY (5 templates)
        # ============================================================
        social_media_templates = [
            TemplateDefinition(
                name='Instagram Caption',
                category='Social Media',
                description='Create an engaging Instagram caption.',
                template='''Create an engaging Instagram caption.

Topic: {{topic}}
Mood: {{mood}}
Target Audience: {{target_audience}}
Call to Action: {{call_to_action}}
Hashtags: {{hashtags}}
Language: {{language}}
Length: {{length}}

Caption Structure:
- Hook (first line)
- Value/Story
- Engagement question
- Call to action
- Hashtags (max 30)''',
                variables=['topic', 'mood', 'target_audience', 'call_to_action', 'hashtags', 'language', 'length']
            ),
            TemplateDefinition(
                name='Facebook Post',
                category='Social Media',
                description='Create an engaging Facebook post.',
                template='''Create an engaging Facebook post.

Topic: {{topic}}
Target Audience: {{target_audience}}
Goal: {{goal}}
Tone: {{tone}}
Language: {{language}}
Hashtags: {{hashtags}}
Link: {{link}}

Post Structure:
- Attention-grabbing opening
- Valuable content/story
- Visual description
- Question for engagement
- Call to action
- Hashtags (3-5)
- Link (if applicable)''',
                variables=['topic', 'target_audience', 'goal', 'tone', 'language', 'hashtags', 'link']
            ),
            TemplateDefinition(
                name='LinkedIn Post',
                category='Social Media',
                description='Create a professional LinkedIn post.',
                template='''Create a professional LinkedIn post.

Topic: {{topic}}
Industry: {{industry}}
Target Audience: {{target_audience}}
Goal: {{goal}}
Tone: {{tone}}
Language: {{language}}
Hashtags: {{hashtags}}

Post Structure:
- Hook (professional insight)
- Personal experience/story
- Key takeaway/lesson
- Actionable advice
- Question for engagement
- Relevant hashtags (3-5)''',
                variables=['topic', 'industry', 'target_audience', 'goal', 'tone', 'language', 'hashtags']
            ),
            TemplateDefinition(
                name='Twitter Post',
                category='Social Media',
                description='Create an engaging Twitter/X post.',
                template='''Create an engaging Twitter/X post.

Topic: {{topic}}
Goal: {{goal}}
Tone: {{tone}}
Language: {{language}}
Hashtags: {{hashtags}}
Thread: {{thread}}

{{#if thread}}
Thread Structure:
1/ Hook tweet
2/ Context
3/ Main point
4/ Example/Proof
5/ Takeaway
6/ Call to action
{{else}}
Single Tweet Structure:
- Hook
- Value
- CTA
- Hashtags (1-2)
{{/if}}''',
                variables=['topic', 'goal', 'tone', 'language', 'hashtags', 'thread']
            ),
            TemplateDefinition(
                name='TikTok Script',
                category='Social Media',
                description='Create a TikTok video script.',
                template='''Create a TikTok video script.

Topic: {{topic}}
Hook: {{hook}}
Format: {{format}}
Duration: {{duration}}
Trend: {{trend}}
Music: {{music}}
Hashtags: {{hashtags}}
Language: {{language}}

TikTok Structure:
- HOOK (0-3s): {{hook}}
- CONTENT (3-{{duration}}s): {{format}}
- TREND INTEGRATION: {{trend}}
- MUSIC CUE: {{music}}
- CTA: Follow for more!
- HASHTAGS: {{hashtags}}''',
                variables=['topic', 'hook', 'format', 'duration', 'trend', 'music', 'hashtags', 'language']
            ),
        ]

        # ============================================================
        # PRODUCTIVITY CATEGORY (8 templates)
        # ============================================================
        productivity_templates = [
            TemplateDefinition(
                name='Email',
                category='Productivity',
                description='Write a professional email.',
                template='''Write a professional email.

Recipient: {{recipient}}
Subject: {{subject}}
Purpose: {{purpose}}
Tone: {{tone}}
Key Points: {{key_points}}
Call to Action: {{call_to_action}}
Language: {{language}}
Length: {{length}}

Email Structure:
- Subject line
- Professional greeting
- Context/purpose
- Key points (bulleted)
- Call to action
- Professional closing
- Signature''',
                variables=['recipient', 'subject', 'purpose', 'tone', 'key_points', 'call_to_action', 'language', 'length']
            ),
            TemplateDefinition(
                name='Blog',
                category='Productivity',
                description='Write a blog post.',
                template='''Write a blog post.

Topic: {{topic}}
Target Audience: {{target_audience}}
Tone: {{tone}}
Length: {{length}}
Keywords: {{keywords}}
Language: {{language}}
Format: {{format}}

Blog Structure:
- Catchy headline
- Introduction with hook
- Main body with subheadings
- Examples/case studies
- Actionable takeaways
- Conclusion with CTA
- SEO meta description''',
                variables=['topic', 'target_audience', 'tone', 'length', 'keywords', 'language', 'format']
            ),
            TemplateDefinition(
                name='Article',
                category='Productivity',
                description='Write an informative article.',
                template='''Write an informative article.

Topic: {{topic}}
Target Audience: {{target_audience}}
Tone: {{tone}}
Length: {{length}}
Keywords: {{keywords}}
Language: {{language}}
Structure: {{structure}}

Article Structure:
- Compelling headline
- Lead paragraph (who, what, when, where, why)
- Body with subheadings
- Expert quotes/data
- Counterarguments
- Conclusion
- References/sources''',
                variables=['topic', 'target_audience', 'tone', 'length', 'keywords', 'language', 'structure']
            ),
            TemplateDefinition(
                name='Lesson Plan',
                category='Productivity',
                description='Create a structured lesson plan.',
                template='''Create a structured lesson plan.

Subject: {{subject}}
Grade Level: {{grade_level}}
Topic: {{topic}}
Duration: {{duration}}
Learning Objectives: {{learning_objectives}}
Materials: {{materials}}
Standards: {{standards}}
Language: {{language}}

Lesson Plan Structure:
- Grade/Subject/Topic
- Learning Objectives
- Standards Alignment
- Materials Needed
- Introduction (Hook)
- Direct Instruction
- Guided Practice
- Independent Practice
- Assessment
- Differentiation
- Closure''',
                variables=['subject', 'grade_level', 'topic', 'duration', 'learning_objectives', 'materials', 'standards', 'language']
            ),
            TemplateDefinition(
                name='Presentation',
                category='Productivity',
                description='Create a presentation outline.',
                template='''Create a presentation outline.

Topic: {{topic}}
Audience: {{audience}}
Goal: {{goal}}
Slides: {{slides}}
Duration: {{duration}}
Tone: {{tone}}
Language: {{language}}
Style: {{style}}

Presentation Structure:
- Title Slide
- Agenda/Overview
- Problem/Context
- Solution/Main Points ({{slides}} slides)
- Evidence/Examples
- Conclusion
- Q&A
- Thank You/Contact''',
                variables=['topic', 'audience', 'goal', 'slides', 'duration', 'tone', 'language', 'style']
            ),
            TemplateDefinition(
                name='Meeting Notes',
                category='Productivity',
                description='Create structured meeting notes.',
                template='''Create structured meeting notes.

Meeting Title: {{meeting_title}}
Date: {{date}}
Attendees: {{attendees}}
Agenda: {{agenda}}
Language: {{language}}

Meeting Notes Structure:
- Meeting Info (title, date, time, attendees)
- Agenda Items
- Key Discussion Points
- Decisions Made
- Action Items (Owner, Due Date)
- Next Steps
- Next Meeting Info''',
                variables=['meeting_title', 'date', 'attendees', 'agenda', 'language']
            ),
            TemplateDefinition(
                name='Summarizer',
                category='Productivity',
                description='Summarize long content into key points.',
                template='''Summarize long content into key points.

Content: {{content}}
Length: {{length}}
Focus: {{focus}}
Format: {{format}}
Language: {{language}}
Tone: {{tone}}

Summary Structure:
- Executive Summary (2-3 sentences)
- Key Points (bulleted)
- Important Details
- Action Items (if applicable)
- Conclusion''',
                variables=['content', 'length', 'focus', 'format', 'language', 'tone']
            ),
            TemplateDefinition(
                name='Translator',
                category='Productivity',
                description='Translate content between languages.',
                template='''Translate content between languages.

Source Text: {{source_text}}
Source Language: {{source_language}}
Target Language: {{target_language}}
Tone: {{tone}}
Context: {{context}}
Formality: {{formality}}

Translation Notes:
- Preserve meaning and nuance
- Adapt cultural references
- Maintain {{tone}} tone
- {{formality}} register
- Context: {{context}}''',
                variables=['source_text', 'source_language', 'target_language', 'tone', 'context', 'formality']
            ),
        ]

        # ============================================================
        # AI ASSISTANT CATEGORY (6 templates)
        # ============================================================
        ai_assistant_templates = [
            TemplateDefinition(
                name='General ChatGPT',
                category='AI Assistant',
                description='General purpose ChatGPT prompt template.',
                template='''General purpose ChatGPT prompt template.

Role: {{role}}
Task: {{task}}
Context: {{context}}
Constraints: {{constraints}}
Output Format: {{output_format}}
Tone: {{tone}}
Language: {{language}}
Examples: {{examples}}

Prompt Structure:
- System prompt (role definition)
- Task description
- Context & background
- Constraints & guidelines
- Output format specification
- Examples (few-shot)
- Tone & style instructions''',
                variables=['role', 'task', 'context', 'constraints', 'output_format', 'tone', 'language', 'examples']
            ),
            TemplateDefinition(
                name='Claude',
                category='AI Assistant',
                description='Optimized prompt template for Claude.',
                template='''Optimized prompt template for Claude.

Role: {{role}}
Task: {{task}}
Context: {{context}}
Instructions: {{instructions}}
Constraints: {{constraints}}
Output Format: {{output_format}}
Tone: {{tone}}
Language: {{language}}
Examples: {{examples}}

Claude-Optimized Structure:
- Clear role definition
- Step-by-step instructions
- Explicit constraints
- XML tags for structure
- Chain-of-thought prompting
- Example-driven guidance''',
                variables=['role', 'task', 'context', 'instructions', 'constraints', 'output_format', 'tone', 'language', 'examples']
            ),
            TemplateDefinition(
                name='Gemini',
                category='AI Assistant',
                description='Optimized prompt template for Google Gemini.',
                template='''Optimized prompt template for Google Gemini.

Role: {{role}}
Task: {{task}}
Context: {{context}}
Instructions: {{instructions}}
Constraints: {{constraints}}
Output Format: {{output_format}}
Tone: {{tone}}
Language: {{language}}
Examples: {{examples}}
Multimodal: {{multimodal}}

Gemini-Optimized Structure:
- Clear role and task definition
- Structured instructions with bullet points
- Explicit output format
- Multimodal input handling
- Safety guideline awareness
- Few-shot examples with formatting''',
                variables=['role', 'task', 'context', 'instructions', 'constraints', 'output_format', 'tone', 'language', 'examples', 'multimodal']
            ),
            TemplateDefinition(
                name='System Prompt',
                category='AI Assistant',
                description='Create a system prompt for AI assistants.',
                template='''Create a system prompt for AI assistants.

Role: {{role}}
Personality: {{personality}}
Guidelines: {{guidelines}}
Constraints: {{constraints}}
Output Style: {{output_style}}
Language: {{language}}
Special Instructions: {{special_instructions}}

System Prompt Structure:
- Identity and role definition
- Personality traits and tone
- Behavioral guidelines
- Hard constraints and boundaries
- Output formatting rules
- Language preferences
- Special capabilities or limitations''',
                variables=['role', 'personality', 'guidelines', 'constraints', 'output_style', 'language', 'special_instructions']
            ),
            TemplateDefinition(
                name='Few-Shot Prompt',
                category='AI Assistant',
                description='Create a few-shot prompt with examples.',
                template='''Create a few-shot prompt with examples.

Task: {{task}}
Context: {{context}}
Examples: {{examples}}
Input: {{input}}
Output Format: {{output_format}}
Constraints: {{constraints}}
Language: {{language}}

Few-Shot Structure:
- Task description
- Context and background
- Example 1 (input -> output)
- Example 2 (input -> output)
- Example 3 (input -> output)
- Actual input to process
- Output format specification''',
                variables=['task', 'context', 'examples', 'input', 'output_format', 'constraints', 'language']
            ),
            TemplateDefinition(
                name='Chain of Thought',
                category='AI Assistant',
                description='Create a chain-of-thought reasoning prompt.',
                template='''Create a chain-of-thought reasoning prompt.

Problem: {{problem}}
Context: {{context}}
Reasoning Steps: {{reasoning_steps}}
Final Answer Format: {{final_answer_format}}
Language: {{language}}
Show Work: {{show_work}}

Chain-of-Thought Structure:
- Problem statement
- Given information
- Step-by-step reasoning
- Intermediate conclusions
- Final answer with confidence
- Verification (if applicable)''',
                variables=['problem', 'context', 'reasoning_steps', 'final_answer_format', 'language', 'show_work']
            ),
        ]

        # Register all templates
        all_templates = [
            education_templates,
            stories_templates,
            images_templates,
            videos_templates,
            voices_templates,
            youtube_templates,
            social_media_templates,
            productivity_templates,
            ai_assistant_templates,
        ]

        for template_list in all_templates:
            for template in template_list:
                self.register(template)

    def register(self, template: TemplateDefinition) -> None:
        '''Register a template definition.'''
        if template.category not in self._templates:
            self._templates[template.category] = {}
        self._templates[template.category][template.name] = template
        logger.debug(f"Registered template: {template.name} in category: {template.category}")

    def get(self, category: str, name: str) -> Optional[TemplateDefinition]:
        '''Get a template by category and name.'''
        return self._templates.get(category, {}).get(name)

    def get_all(self, category: str) -> Dict[str, TemplateDefinition]:
        '''Get all templates in a category.'''
        return self._templates.get(category, {})

    def get_categories(self) -> List[str]:
        '''Get all registered categories.'''
        return list(self._templates.keys())

    def get_template_names(self, category: str) -> List[str]:
        '''Get all template names in a category.'''
        return list(self._templates.get(category, {}).keys())

    def get_templates(self, category: str) -> List[TemplateDefinition]:
        """
        Backward compatibility wrapper.
        Returns all TemplateDefinition objects belonging to the requested category.
        """
        # Case-insensitive category matching
        category_lower = category.lower()
        for cat_key, templates_dict in self._templates.items():
            if cat_key.lower() == category_lower:
                return list(templates_dict.values())
        return []

    def get_template(self, name: str) -> Optional[TemplateDefinition]:
        """
        Backward compatibility wrapper.
        Returns a TemplateDefinition by name.
        """
        # Search across all categories for the template name
        for templates_dict in self._templates.values():
            if name in templates_dict:
                return templates_dict[name]
        return None

    def search(self, query: str) -> List[TemplateDefinition]:
        '''Search templates by name, description, or tags.'''
        query = query.lower()
        results = []
        for category_templates in self._templates.values():
            for template in category_templates.values():
                if (query in template.name.lower() or
                    query in template.description.lower() or
                    any(query in tag.lower() for tag in template.tags)):
                    results.append(template)
        return results

    def render(self, category: str, name: str, variables: Dict[str, str]) -> str:
        '''Render a template with provided variables.'''
        template = self.get(category, name)
        if not template:
            raise ValueError(f"Template not found: {category}/{name}")
         
        result = template.template
        for key, value in variables.items():
            result = result.replace(f"{{{{{key}}}}}", value)
        return result

    def validate_variables(self, category: str, name: str, variables: Dict[str, str]) -> List[str]:
        '''Validate variables against template requirements.'''
        template = self.get(category, name)
        if not template:
            return [f"Template not found: {category}/{name}"]
         
        errors = []
        for var_name in template.variables:
            if var_name not in variables:
                errors.append(f"Missing required variable: {var_name}")
            else:
                var_def = self._variable_registry.get(var_name)
                if var_def:
                    var_errors = var_def.validate(variables[var_name])
                    errors.extend(var_errors)
        return errors