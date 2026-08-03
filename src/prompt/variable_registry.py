"""Variable Registry for AI Kids Studio Pro.

Production-grade variable registry with professional option libraries,
validation metadata, variable groups, and full backward compatibility.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Union

from src.prompt.option_library import OptionLibrary, OptionGroup

logger = logging.getLogger(__name__)


class VariableType(str, Enum):
    """Supported variable input types."""
    TEXT = "text"
    NUMBER = "number"
    DROPDOWN = "dropdown"
    MULTISELECT = "multiselect"
    BOOLEAN = "boolean"
    COLOR = "color"
    DATE = "date"
    TIME = "time"
    SLIDER = "slider"
    TEXTAREA = "textarea"
    PASSWORD = "password"
    EMAIL = "email"
    URL = "url"
    FILE = "file"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class VariableGroup(str, Enum):
    """Logical variable groups for organization."""
    EDUCATION = "Education"
    STORIES = "Stories"
    IMAGES = "Images"
    VIDEOS = "Videos"
    VOICES = "Voices"
    YOUTUBE = "YouTube"
    SOCIAL_MEDIA = "Social Media"
    PRODUCTIVITY = "Productivity"
    AI_ASSISTANT = "AI Assistant"
    CUSTOM = "Custom"


@dataclass(frozen=True)
class ValidationRule:
    """Validation rule for variable values."""
    rule_type: str  # "min", "max", "regex", "required", "custom"
    value: Any
    message: str = ""
    validator: Optional[Callable[[Any], bool]] = None


@dataclass(frozen=True)
class VariableDefinition:
    """Enhanced variable definition with rich metadata.
    
    Backward compatible with existing VariableDefinition fields.
    All new fields are optional with sensible defaults.
    """
    # Core fields (backward compatible)
    name: str
    display_name: str
    type: str = "text"
    default_value: Optional[str] = None
    options: List[str] = field(default_factory=list)
    required: bool = False
    placeholder: Optional[str] = None
    
    # Enhanced metadata fields (all optional)
    description: str = ""
    group: str = VariableGroup.CUSTOM.value
    icon: str = ""
    tooltip: str = ""
    sort_order: int = 0
    advanced: bool = False
    validation: List[ValidationRule] = field(default_factory=list)
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    regex: Optional[str] = None
    allow_custom: bool = False
    searchable: bool = False
    example: str = ""
    unit: str = ""
    visible_if: Optional[str] = None  # Expression for conditional visibility
    
    # Option library reference (for large datasets)
    option_library: Optional[str] = None  # References OptionLibrary group name
    
    def __post_init__(self) -> None:
        """Validate and normalize after initialization."""
        # Ensure type is valid
        if self.type not in [t.value for t in VariableType]:
            object.__setattr__(self, 'type', VariableType.TEXT.value)
        
        # Ensure group is valid
        if self.group not in [g.value for g in VariableGroup]:
            object.__setattr__(self, 'group', VariableGroup.CUSTOM.value)
        
        # Auto-enable searchable for large option sets
        if self.options and len(self.options) > 20:
            object.__setattr__(self, 'searchable', True)
        
        # Auto-enable searchable if using option library
        if self.option_library:
            object.__setattr__(self, 'searchable', True)

        if self.type == VariableType.DROPDOWN.value and not self.options and self.option_library:
            resolved_options = self._coerce_option_values(OptionLibrary.get_group(self.option_library))
            if resolved_options:
                object.__setattr__(self, 'options', resolved_options)

    @staticmethod
    def _coerce_option_value(item: Any) -> Optional[str]:
        """Normalize an option-like item into a plain display string."""
        if item is None:
            return None

        if isinstance(item, str):
            return item

        for attr in ("label", "display", "name", "text", "value"):
            if hasattr(item, attr):
                attr_value = getattr(item, attr)
                if isinstance(attr_value, str) and attr_value:
                    return attr_value

        if isinstance(item, dict):
            for key in ("label", "display", "name", "text", "value"):
                if key in item and isinstance(item[key], str) and item[key]:
                    return item[key]

        if isinstance(item, (list, tuple)) and len(item) >= 2 and isinstance(item[1], str):
            return item[1]

        return None

    @classmethod
    def _coerce_option_values(cls, value: Any) -> List[str]:
        """Convert option groups or option objects into a plain list of labels."""
        if value is None:
            return []

        if isinstance(value, str):
            return [value]

        if hasattr(value, "options"):
            return cls._coerce_option_values(getattr(value, "options"))

        if isinstance(value, (list, tuple)):
            resolved: List[str] = []
            for item in value:
                normalized = cls._coerce_option_value(item)
                if normalized:
                    resolved.append(normalized)
            return resolved

        normalized = cls._coerce_option_value(value)
        return [normalized] if normalized else []

    def get_options(self) -> List[str]:
        """Get options, resolving from option library if specified."""
        if self.option_library:
            group = OptionLibrary.get_group(self.option_library)
            if group:
                return self._coerce_option_values(group)
        if self.options:
            return self.options
        return []
    
    def get_dropdown_options(self) -> List[Dict[str, str]]:
        """Get options formatted for dropdown UI."""
        if self.option_library:
            return OptionLibrary.get_dropdown_data(self.option_library)
        return [
            {"value": opt, "label": opt.replace("_", " ").title()}
            for opt in self.options
        ]
    
    def validate(self, value: Any) -> List[str]:
        """Validate a value against all rules. Returns list of error messages."""
        errors = []
        
        # Required check
        if self.required and (value is None or value == ""):
            errors.append(f"{self.display_name} is required")
            return errors
        
        # Skip further validation if empty and not required
        if value is None or value == "":
            return errors
        
        # Type-specific validation
        if self.type == VariableType.NUMBER.value:
            try:
                num_val = float(value)
                if self.min_value is not None and num_val < self.min_value:
                    errors.append(f"{self.display_name} must be at least {self.min_value}")
                if self.max_value is not None and num_val > self.max_value:
                    errors.append(f"{self.display_name} must be at most {self.max_value}")
            except (ValueError, TypeError):
                errors.append(f"{self.display_name} must be a valid number")
        
        elif self.type == VariableType.TEXT.value or self.type == VariableType.TEXTAREA.value:
            str_val = str(value)
            if self.min_value is not None and len(str_val) < self.min_value:
                errors.append(f"{self.display_name} must be at least {self.min_value} characters")
            if self.max_value is not None and len(str_val) > self.max_value:
                errors.append(f"{self.display_name} must be at most {self.max_value} characters")
        
        # Regex validation
        if self.regex:
            try:
                if not re.match(self.regex, str(value)):
                    errors.append(self.message or f"{self.display_name} format is invalid")
            except re.error:
                logger.warning(f"Invalid regex in variable {self.name}: {self.regex}")
        
        # Custom validation rules
        for rule in self.validation:
            if rule.rule_type == "custom" and rule.validator:
                if not rule.validator(value):
                    errors.append(rule.message or f"{self.display_name} validation failed")
            elif rule.rule_type == "regex":
                try:
                    if not re.match(str(rule.value), str(value)):
                        errors.append(rule.message or f"{self.display_name} format is invalid")
                except re.error:
                    pass
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "type": self.type,
            "default_value": self.default_value,
            "options": self.options,
            "required": self.required,
            "placeholder": self.placeholder,
            "description": self.description,
            "group": self.group,
            "icon": self.icon,
            "tooltip": self.tooltip,
            "sort_order": self.sort_order,
            "advanced": self.advanced,
            "validation": [
                {"rule_type": r.rule_type, "value": r.value, "message": r.message}
                for r in self.validation
            ],
            "min_value": self.min_value,
            "max_value": self.max_value,
            "regex": self.regex,
            "allow_custom": self.allow_custom,
            "searchable": self.searchable,
            "example": self.example,
            "unit": self.unit,
            "visible_if": self.visible_if,
            "option_library": self.option_library,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VariableDefinition:
        """Create from dictionary."""
        validation_rules = []
        for v in data.get("validation", []):
            validation_rules.append(ValidationRule(
                rule_type=v.get("rule_type", ""),
                value=v.get("value"),
                message=v.get("message", "")
            ))
        
        return cls(
            name=data["name"],
            display_name=data["display_name"],
            type=data.get("type", "text"),
            default_value=data.get("default_value"),
            options=data.get("options", []),
            required=data.get("required", False),
            placeholder=data.get("placeholder"),
            description=data.get("description", ""),
            group=data.get("group", VariableGroup.CUSTOM.value),
            icon=data.get("icon", ""),
            tooltip=data.get("tooltip", ""),
            sort_order=data.get("sort_order", 0),
            advanced=data.get("advanced", False),
            validation=validation_rules,
            min_value=data.get("min_value"),
            max_value=data.get("max_value"),
            regex=data.get("regex"),
            allow_custom=data.get("allow_custom", False),
            searchable=data.get("searchable", False),
            example=data.get("example", ""),
            unit=data.get("unit", ""),
            visible_if=data.get("visible_if"),
            option_library=data.get("option_library"),
        )


class VariableRegistry:
    """Production-grade variable registry with groups, validation, and scalability.
    
    Maintains full backward compatibility with existing VariableRegistry API.
    """
    
    def __init__(self) -> None:
        self._variables: Dict[str, VariableDefinition] = {}
        self._groups: Dict[str, List[str]] = {g.value: [] for g in VariableGroup}
        self._register_builtin_variables()
    
    def _register_builtin_variables(self) -> None:
        """Register all built-in professional variables."""
        builtin_variables = self._create_builtin_variables()
        for variable in builtin_variables:
            self.register(self._resolve_definition_options(variable))

        # Backward compatibility: ensure legacy variable names exist
        for name in [
            "language",
            "animal",
            "voice",
            "fruit",
            "vegetable",
            "country",
            "vehicle",
            "flower",
            "bird",
            "emotion",
            "weather",
            "camera_angle",
            "art_style",
            "lighting",
            "animation_style",
            "aspect_ratio",
            "quality",
        ]:
            if name not in self._variables:
                self.register(
                    self._resolve_definition_options(
                        VariableDefinition(
                            name=name,
                            display_name=name.replace("_", " ").title(),
                            type=VariableType.DROPDOWN.value,
                        )
                    )
                )

    def _resolve_definition_options(self, variable: VariableDefinition) -> VariableDefinition:
        """Populate dropdown options from an option library when available."""
        if variable.type != VariableType.DROPDOWN.value or variable.options:
            return variable

        if variable.option_library:
            resolved_options = VariableDefinition._coerce_option_values(OptionLibrary.get_group(variable.option_library))
            if resolved_options:
                variable.options = resolved_options
                return variable

        mapping = {
            "language": "languages",
            "animal": "animals",
            "voice": "voices",
            "fruit": "fruits",
            "vegetable": "vegetables",
            "country": "countries",
            "vehicle": "vehicles",
            "flower": "flowers",
            "bird": "birds",
            "emotion": "emotions",
            "weather": "weather_conditions",
            "camera_angle": "camera_angles",
            "art_style": "art_styles",
            "lighting": "lighting_styles",
            "animation_style": "animation_styles",
            "aspect_ratio": "aspect_ratios",
            "quality": "quality_presets",
        }

        group_name = mapping.get(variable.name)
        if not group_name:
            return variable

        resolved_options = VariableDefinition._coerce_option_values(OptionLibrary.get_group(group_name))
        if resolved_options:
            variable.options = resolved_options

        return variable
    
    def _create_builtin_variables(self) -> List[VariableDefinition]:
        """Create the complete library of 80-100 professional variables."""
        return [
            # ============================================================
            # EDUCATION GROUP (50+ variables)
            # ============================================================
            VariableDefinition(
                name="letter",
                display_name="Letter",
                type=VariableType.DROPDOWN.value,
                default_value="A",
                option_library="alphabet_styles",
                required=False,
                placeholder="Select a letter",
                description="Alphabet letter for learning activities",
                group=VariableGroup.EDUCATION.value,
                icon="🔤",
                tooltip="Choose a letter from A-Z",
                sort_order=1,
                searchable=True,
                example="A",
            ),
            VariableDefinition(
                name="number",
                display_name="Number",
                type=VariableType.NUMBER.value,
                default_value="1",
                required=False,
                placeholder="Enter a number 1-100",
                description="Number for counting and math activities",
                group=VariableGroup.EDUCATION.value,
                icon="🔢",
                tooltip="Enter a number between 1 and 100",
                sort_order=2,
                min_value=1,
                max_value=100,
                example="5",
                unit="count",
            ),
            VariableDefinition(
                name="color",
                display_name="Color",
                type=VariableType.DROPDOWN.value,
                default_value="blue",
                option_library="colors",
                required=False,
                placeholder="Select a color",
                description="Color for art and recognition activities",
                group=VariableGroup.EDUCATION.value,
                icon="🎨",
                tooltip="Choose a color",
                sort_order=3,
                searchable=True,
                example="red",
            ),
            VariableDefinition(
                name="shape",
                display_name="Shape",
                type=VariableType.DROPDOWN.value,
                default_value="circle",
                option_library="shapes",
                required=False,
                placeholder="Select a shape",
                description="Geometric shape for recognition",
                group=VariableGroup.EDUCATION.value,
                icon="🔷",
                tooltip="Choose a geometric shape",
                sort_order=4,
                searchable=True,
                example="triangle",
            ),
            VariableDefinition(
                name="animal",
                display_name="Animal",
                type=VariableType.DROPDOWN.value,
                default_value="lion",
                option_library="animals",
                required=False,
                placeholder="Select an animal",
                description="Animal for learning and stories",
                group=VariableGroup.EDUCATION.value,
                icon="🦁",
                tooltip="Choose an animal",
                sort_order=5,
                searchable=True,
                example="elephant",
            ),
            VariableDefinition(
                name="bird",
                display_name="Bird",
                type=VariableType.DROPDOWN.value,
                default_value="eagle",
                option_library="birds",
                required=False,
                placeholder="Select a bird",
                description="Bird for nature education",
                group=VariableGroup.EDUCATION.value,
                icon="🦅",
                tooltip="Choose a bird species",
                sort_order=6,
                searchable=True,
                example="parrot",
            ),
            VariableDefinition(
                name="fruit",
                display_name="Fruit",
                type=VariableType.DROPDOWN.value,
                default_value="apple",
                option_library="fruits",
                required=False,
                placeholder="Select a fruit",
                description="Fruit for nutrition education",
                group=VariableGroup.EDUCATION.value,
                icon="🍎",
                tooltip="Choose a fruit",
                sort_order=7,
                searchable=True,
                example="banana",
            ),
            VariableDefinition(
                name="vegetable",
                display_name="Vegetable",
                type=VariableType.DROPDOWN.value,
                default_value="carrot",
                option_library="vegetables",
                required=False,
                placeholder="Select a vegetable",
                description="Vegetable for healthy eating education",
                group=VariableGroup.EDUCATION.value,
                icon="🥕",
                tooltip="Choose a vegetable",
                sort_order=8,
                searchable=True,
                example="broccoli",
            ),
            VariableDefinition(
                name="vehicle",
                display_name="Vehicle",
                type=VariableType.DROPDOWN.value,
                default_value="car",
                option_library="vehicles",
                required=False,
                placeholder="Select a vehicle",
                description="Vehicle for transportation learning",
                group=VariableGroup.EDUCATION.value,
                icon="🚗",
                tooltip="Choose a vehicle type",
                sort_order=9,
                searchable=True,
                example="airplane",
            ),
            VariableDefinition(
                name="flower",
                display_name="Flower",
                type=VariableType.DROPDOWN.value,
                default_value="rose",
                option_library="flowers",
                required=False,
                placeholder="Select a flower",
                description="Flower for nature education",
                group=VariableGroup.EDUCATION.value,
                icon="🌸",
                tooltip="Choose a flower",
                sort_order=10,
                searchable=True,
                example="sunflower",
            ),
            VariableDefinition(
                name="country",
                display_name="Country",
                type=VariableType.DROPDOWN.value,
                default_value="united_states",
                option_library="countries",
                required=False,
                placeholder="Select a country",
                description="Country for geography lessons",
                group=VariableGroup.EDUCATION.value,
                icon="🌍",
                tooltip="Choose a country",
                sort_order=11,
                searchable=True,
                example="japan",
            ),
            VariableDefinition(
                name="planet",
                display_name="Planet",
                type=VariableType.DROPDOWN.value,
                default_value="earth",
                option_library="planets",
                required=False,
                placeholder="Select a planet",
                description="Planet for space education",
                group=VariableGroup.EDUCATION.value,
                icon="🪐",
                tooltip="Choose a planet",
                sort_order=12,
                searchable=True,
                example="mars",
            ),
            VariableDefinition(
                name="body_part",
                display_name="Body Part",
                type=VariableType.DROPDOWN.value,
                default_value="head",
                option_library="body_parts",
                required=False,
                placeholder="Select a body part",
                description="Body part for anatomy education",
                group=VariableGroup.EDUCATION.value,
                icon="👋",
                tooltip="Choose a body part",
                sort_order=13,
                searchable=True,
                example="hands",
            ),
            VariableDefinition(
                name="weather",
                display_name="Weather",
                type=VariableType.DROPDOWN.value,
                default_value="sunny",
                option_library="weather_conditions",
                required=False,
                placeholder="Select weather",
                description="Weather condition for science lessons",
                group=VariableGroup.EDUCATION.value,
                icon="🌤️",
                tooltip="Choose a weather type",
                sort_order=14,
                searchable=True,
                example="rainy",
            ),
            VariableDefinition(
                name="emotion",
                display_name="Emotion",
                type=VariableType.DROPDOWN.value,
                default_value="happy",
                option_library="emotions",
                required=False,
                placeholder="Select an emotion",
                description="Emotion for social-emotional learning",
                group=VariableGroup.EDUCATION.value,
                icon="😊",
                tooltip="Choose an emotion",
                sort_order=15,
                searchable=True,
                example="excited",
            ),
            VariableDefinition(
                name="profession",
                display_name="Profession",
                type=VariableType.DROPDOWN.value,
                default_value="teacher",
                option_library="professions",
                required=False,
                placeholder="Select a profession",
                description="Profession for career education",
                group=VariableGroup.EDUCATION.value,
                icon="💼",
                tooltip="Choose a profession",
                sort_order=16,
                searchable=True,
                example="doctor",
            ),
            VariableDefinition(
                name="instrument",
                display_name="Instrument",
                type=VariableType.DROPDOWN.value,
                default_value="piano",
                option_library="instruments",
                required=False,
                placeholder="Select an instrument",
                description="Musical instrument for music education",
                group=VariableGroup.EDUCATION.value,
                icon="🎵",
                tooltip="Choose an instrument",
                sort_order=17,
                searchable=True,
                example="guitar",
            ),
            VariableDefinition(
                name="sport",
                display_name="Sport",
                type=VariableType.DROPDOWN.value,
                default_value="soccer",
                option_library="sports",
                required=False,
                placeholder="Select a sport",
                description="Sport for physical education",
                group=VariableGroup.EDUCATION.value,
                icon="⚽",
                tooltip="Choose a sport",
                sort_order=18,
                searchable=True,
                example="basketball",
            ),
            VariableDefinition(
                name="food",
                display_name="Food",
                type=VariableType.DROPDOWN.value,
                default_value="pizza",
                option_library="foods",
                required=False,
                placeholder="Select a food",
                description="Food item for nutrition education",
                group=VariableGroup.EDUCATION.value,
                icon="🍕",
                tooltip="Choose a food",
                sort_order=19,
                searchable=True,
                example="sushi",
            ),
            VariableDefinition(
                name="drink",
                display_name="Drink",
                type=VariableType.DROPDOWN.value,
                default_value="water",
                option_library="drinks",
                required=False,
                placeholder="Select a drink",
                description="Beverage for nutrition education",
                group=VariableGroup.EDUCATION.value,
                icon="🥤",
                tooltip="Choose a drink",
                sort_order=20,
                searchable=True,
                example="milk",
            ),
            VariableDefinition(
                name="month",
                display_name="Month",
                type=VariableType.DROPDOWN.value,
                default_value="january",
                option_library="months",
                required=False,
                placeholder="Select a month",
                description="Month for calendar education",
                group=VariableGroup.EDUCATION.value,
                icon="📅",
                tooltip="Choose a month",
                sort_order=21,
                searchable=True,
                example="july",
            ),
            VariableDefinition(
                name="day",
                display_name="Day of Week",
                type=VariableType.DROPDOWN.value,
                default_value="monday",
                option_library="days_of_week",
                required=False,
                placeholder="Select a day",
                description="Day of the week for schedule learning",
                group=VariableGroup.EDUCATION.value,
                icon="📅",
                tooltip="Choose a day",
                sort_order=22,
                searchable=True,
                example="friday",
            ),
            VariableDefinition(
                name="alphabet_style",
                display_name="Alphabet Style",
                type=VariableType.DROPDOWN.value,
                default_value="uppercase",
                option_library="alphabet_styles",
                required=False,
                placeholder="Select alphabet style",
                description="Letter presentation style",
                group=VariableGroup.EDUCATION.value,
                icon="🔤",
                tooltip="Choose how letters are displayed",
                sort_order=23,
                example="cursive",
            ),
            VariableDefinition(
                name="learning_level",
                display_name="Learning Level",
                type=VariableType.DROPDOWN.value,
                default_value="beginner",
                option_library="learning_levels",
                required=False,
                placeholder="Select learning level",
                description="Educational difficulty level",
                group=VariableGroup.EDUCATION.value,
                icon="📚",
                tooltip="Choose difficulty level",
                sort_order=24,
                example="intermediate",
            ),
            VariableDefinition(
                name="worksheet_type",
                display_name="Worksheet Type",
                type=VariableType.DROPDOWN.value,
                default_value="tracing",
                option_library="worksheet_types",
                required=False,
                placeholder="Select worksheet type",
                description="Type of educational worksheet",
                group=VariableGroup.EDUCATION.value,
                icon="📝",
                tooltip="Choose worksheet format",
                sort_order=25,
                example="matching",
            ),
            VariableDefinition(
                name="quiz_type",
                display_name="Quiz Type",
                type=VariableType.DROPDOWN.value,
                default_value="multiple_choice",
                option_library="quiz_types",
                required=False,
                placeholder="Select quiz type",
                description="Quiz format for assessment",
                group=VariableGroup.EDUCATION.value,
                icon="❓",
                tooltip="Choose quiz format",
                sort_order=26,
                example="true_false",
            ),
            VariableDefinition(
                name="reward_type",
                display_name="Reward Type",
                type=VariableType.DROPDOWN.value,
                default_value="sticker",
                option_library="reward_types",
                required=False,
                placeholder="Select reward",
                description="Reward for completing activities",
                group=VariableGroup.EDUCATION.value,
                icon="🏆",
                tooltip="Choose reward type",
                sort_order=27,
                example="badge",
            ),
            VariableDefinition(
                name="teacher_name",
                display_name="Teacher Name",
                type=VariableType.TEXT.value,
                default_value="Ms. Smith",
                required=False,
                placeholder="Enter teacher name",
                description="Teacher name for personalized content",
                group=VariableGroup.EDUCATION.value,
                icon="👩‍🏫",
                tooltip="Teacher's name",
                sort_order=28,
                example="Mr. Johnson",
            ),
            VariableDefinition(
                name="mascot",
                display_name="Class Mascot",
                type=VariableType.TEXT.value,
                default_value="Buddy the Bear",
                required=False,
                placeholder="Enter mascot name",
                description="Classroom mascot character",
                group=VariableGroup.EDUCATION.value,
                icon="🧸",
                tooltip="Mascot name",
                sort_order=29,
                example="Sammy the Squirrel",
            ),
            VariableDefinition(
                name="reading_level",
                display_name="Reading Level",
                type=VariableType.DROPDOWN.value,
                default_value="early",
                option_library="reading_levels",
                required=False,
                placeholder="Select reading level",
                description="Reading difficulty level",
                group=VariableGroup.EDUCATION.value,
                icon="📖",
                tooltip="Choose reading level",
                sort_order=30,
                example="fluent",
            ),
            VariableDefinition(
                name="curriculum",
                display_name="Curriculum Standard",
                type=VariableType.DROPDOWN.value,
                default_value="common_core",
                option_library="curriculum_standards",
                required=False,
                placeholder="Select curriculum",
                description="Educational curriculum framework",
                group=VariableGroup.EDUCATION.value,
                icon="📋",
                tooltip="Choose curriculum standard",
                sort_order=31,
                example="montessori",
            ),
            VariableDefinition(
                name="lesson_objective",
                display_name="Lesson Objective",
                type=VariableType.TEXTAREA.value,
                default_value="Students will identify and name the letter A",
                required=False,
                placeholder="Enter learning objective",
                description="Specific learning goal for the lesson",
                group=VariableGroup.EDUCATION.value,
                icon="🎯",
                tooltip="What students will learn",
                sort_order=32,
                example="Count to 10 with objects",
                max_value=500,
            ),
            
            # ============================================================
            # ABC LEARNING - Additional Variables
            # ============================================================
            VariableDefinition(
                name="teaching_style",
                display_name="Teaching Style",
                type=VariableType.DROPDOWN.value,
                default_value="fun_teacher",
                option_library="teaching_styles",
                required=False,
                placeholder="Select teaching style",
                description="Pedagogical approach for the lesson",
                group=VariableGroup.EDUCATION.value,
                icon="👩‍🏫",
                tooltip="Choose how the content is taught",
                sort_order=33,
                searchable=True,
                example="storytelling",
            ),
            VariableDefinition(
                name="vocabulary_level",
                display_name="Vocabulary Level",
                type=VariableType.DROPDOWN.value,
                default_value="beginner",
                option_library="vocabulary_levels",
                required=False,
                placeholder="Select vocabulary level",
                description="Word difficulty level for content",
                group=VariableGroup.EDUCATION.value,
                icon="📚",
                tooltip="Choose word difficulty",
                sort_order=34,
                searchable=True,
                example="intermediate",
            ),
            VariableDefinition(
                name="language",
                display_name="Language",
                type=VariableType.DROPDOWN.value,
                default_value="english",
                option_library="languages",
                required=False,
                placeholder="Select language",
                description="Language for content generation",
                group=VariableGroup.EDUCATION.value,
                icon="🌍",
                tooltip="Choose the language",
                sort_order=35,
                searchable=True,
                example="spanish",
            ),
            VariableDefinition(
                name="voice",
                display_name="Voice",
                type=VariableType.DROPDOWN.value,
                default_value="female_adult",
                option_library="voices",
                required=False,
                placeholder="Select voice",
                description="Voice preset for narration",
                group=VariableGroup.EDUCATION.value,
                icon="🎙️",
                tooltip="Choose narrator voice",
                sort_order=36,
                searchable=True,
                example="storyteller",
            ),
            VariableDefinition(
                name="art_style",
                display_name="Art Style",
                type=VariableType.DROPDOWN.value,
                default_value="pixar",
                option_library="art_styles",
                required=False,
                placeholder="Select art style",
                description="Visual artistic style for illustrations",
                group=VariableGroup.EDUCATION.value,
                icon="🎨",
                tooltip="Choose illustration style",
                sort_order=37,
                searchable=True,
                example="watercolor",
            ),
            VariableDefinition(
                name="animation_style",
                display_name="Animation Style",
                type=VariableType.DROPDOWN.value,
                default_value="3d_cgi",
                option_library="animation_styles",
                required=False,
                placeholder="Select animation style",
                description="Animation technique for videos",
                group=VariableGroup.EDUCATION.value,
                icon="🎬",
                tooltip="Choose animation method",
                sort_order=38,
                searchable=True,
                example="2d_traditional",
            ),
            VariableDefinition(
                name="lighting",
                display_name="Lighting",
                type=VariableType.DROPDOWN.value,
                default_value="natural",
                option_library="lighting_styles",
                required=False,
                placeholder="Select lighting",
                description="Lighting setup for visual content",
                group=VariableGroup.EDUCATION.value,
                icon="💡",
                tooltip="Choose lighting style",
                sort_order=39,
                searchable=True,
                example="golden_hour",
            ),
            VariableDefinition(
                name="camera_angle",
                display_name="Camera Angle",
                type=VariableType.DROPDOWN.value,
                default_value="eye_level",
                option_library="camera_angles",
                required=False,
                placeholder="Select camera angle",
                description="Camera perspective for visuals",
                group=VariableGroup.EDUCATION.value,
                icon="📷",
                tooltip="Choose viewpoint",
                sort_order=40,
                searchable=True,
                example="low_angle",
            ),
            VariableDefinition(
                name="aspect_ratio",
                display_name="Aspect Ratio",
                type=VariableType.DROPDOWN.value,
                default_value="16:9",
                option_library="aspect_ratios",
                required=False,
                placeholder="Select ratio",
                description="Image/video aspect ratio",
                group=VariableGroup.EDUCATION.value,
                icon="📐",
                tooltip="Choose width:height ratio",
                sort_order=41,
                example="9:16",
            ),
            VariableDefinition(
                name="quality",
                display_name="Quality",
                type=VariableType.DROPDOWN.value,
                default_value="high",
                option_library="quality_presets",
                required=False,
                placeholder="Select quality",
                description="Output quality level",
                group=VariableGroup.EDUCATION.value,
                icon="⭐",
                tooltip="Choose render quality",
                sort_order=42,
                example="ultra",
            ),
            
            # ============================================================
            # NUMBERS LEARNING
            # ============================================================
            VariableDefinition(
                name="counting_object",
                display_name="Counting Object",
                type=VariableType.DROPDOWN.value,
                default_value="apples",
                option_library="counting_objects",
                required=False,
                placeholder="Select object to count",
                description="Object used for counting activities",
                group=VariableGroup.EDUCATION.value,
                icon="🔢",
                tooltip="What to count",
                sort_order=43,
                searchable=True,
                example="stars",
            ),
            VariableDefinition(
                name="counting_style",
                display_name="Counting Style",
                type=VariableType.DROPDOWN.value,
                default_value="count_forward",
                option_library="counting_styles",
                required=False,
                placeholder="Select counting method",
                description="Method of counting to teach",
                group=VariableGroup.EDUCATION.value,
                icon="🔢",
                tooltip="How to count",
                sort_order=44,
                searchable=True,
                example="skip_counting",
            ),
            VariableDefinition(
                name="number_type",
                display_name="Number Type",
                type=VariableType.DROPDOWN.value,
                default_value="cardinal",
                option_library="number_types",
                required=False,
                placeholder="Select number type",
                description="Type of numbers for the activity",
                group=VariableGroup.EDUCATION.value,
                icon="🔢",
                tooltip="Kind of numbers",
                sort_order=45,
                searchable=True,
                example="ordinal",
            ),
            VariableDefinition(
                name="math_operation",
                display_name="Math Operation",
                type=VariableType.DROPDOWN.value,
                default_value="addition",
                option_library="math_operations",
                required=False,
                placeholder="Select operation",
                description="Arithmetic operation to practice",
                group=VariableGroup.EDUCATION.value,
                icon="➕",
                tooltip="Math operation",
                sort_order=46,
                searchable=True,
                example="subtraction",
            ),
            VariableDefinition(
                name="difficulty",
                display_name="Difficulty",
                type=VariableType.DROPDOWN.value,
                default_value="easy",
                option_library="quiz_difficulty",
                required=False,
                placeholder="Select difficulty",
                description="Difficulty level for the activity",
                group=VariableGroup.EDUCATION.value,
                icon="📊",
                tooltip="Challenge level",
                sort_order=47,
                searchable=True,
                example="medium",
            ),
            
            # ============================================================
            # COLORS LEARNING
            # ============================================================
            VariableDefinition(
                name="color_object",
                display_name="Object",
                type=VariableType.DROPDOWN.value,
                default_value="apple",
                option_library="fruits",
                required=False,
                placeholder="Select object",
                description="Object to identify color of",
                group=VariableGroup.EDUCATION.value,
                icon="🍎",
                tooltip="Choose an object",
                sort_order=48,
                searchable=True,
                example="banana",
            ),
            
            # ============================================================
            # SHAPES LEARNING
            # ============================================================
            VariableDefinition(
                name="shape_object",
                display_name="Shape Object",
                type=VariableType.DROPDOWN.value,
                default_value="circle",
                option_library="shapes",
                required=False,
                placeholder="Select shape",
                description="Geometric shape to learn",
                group=VariableGroup.EDUCATION.value,
                icon="🔷",
                tooltip="Choose a shape",
                sort_order=49,
                searchable=True,
                example="triangle",
            ),
            VariableDefinition(
                name="real_world_example",
                display_name="Real World Example",
                type=VariableType.DROPDOWN.value,
                default_value="pizza",
                option_library="foods",
                required=False,
                placeholder="Select example",
                description="Real-world object with this shape",
                group=VariableGroup.EDUCATION.value,
                icon="🍕",
                tooltip="Real world shape example",
                sort_order=50,
                searchable=True,
                example="clock",
            ),
            
            # ============================================================
            # ANIMALS LEARNING
            # ============================================================
            VariableDefinition(
                name="animal_habitat",
                display_name="Habitat",
                type=VariableType.DROPDOWN.value,
                default_value="forest",
                option_library="habitats",
                required=False,
                placeholder="Select habitat",
                description="Where the animal lives",
                group=VariableGroup.EDUCATION.value,
                icon="🏞️",
                tooltip="Animal's home",
                sort_order=51,
                searchable=True,
                example="ocean",
            ),
            VariableDefinition(
                name="animal_diet",
                display_name="Diet",
                type=VariableType.DROPDOWN.value,
                default_value="carnivore",
                option_library="diets",
                required=False,
                placeholder="Select diet",
                description="What the animal eats",
                group=VariableGroup.EDUCATION.value,
                icon="🍽️",
                tooltip="Animal's food",
                sort_order=52,
                searchable=True,
                example="herbivore",
            ),
            VariableDefinition(
                name="animal_type",
                display_name="Animal Type",
                type=VariableType.DROPDOWN.value,
                default_value="mammal",
                option_library="animal_types",
                required=False,
                placeholder="Select type",
                description="Classification of the animal",
                group=VariableGroup.EDUCATION.value,
                icon="🦁",
                tooltip="Animal classification",
                sort_order=53,
                searchable=True,
                example="bird",
            ),
            
            # ============================================================
            # BIRDS LEARNING
            # ============================================================
            VariableDefinition(
                name="bird_species",
                display_name="Bird",
                type=VariableType.DROPDOWN.value,
                default_value="eagle",
                option_library="birds",
                required=False,
                placeholder="Select bird",
                description="Bird species to learn about",
                group=VariableGroup.EDUCATION.value,
                icon="🦅",
                tooltip="Choose a bird",
                sort_order=54,
                searchable=True,
                example="parrot",
            ),
            VariableDefinition(
                name="bird_habitat",
                display_name="Habitat",
                type=VariableType.DROPDOWN.value,
                default_value="forest",
                option_library="habitats",
                required=False,
                placeholder="Select habitat",
                description="Where the bird lives",
                group=VariableGroup.EDUCATION.value,
                icon="🏞️",
                tooltip="Bird's home",
                sort_order=55,
                searchable=True,
                example="wetland",
            ),
            VariableDefinition(
                name="bird_food",
                display_name="Food",
                type=VariableType.DROPDOWN.value,
                default_value="fish",
                option_library="diets",
                required=False,
                placeholder="Select food",
                description="What the bird eats",
                group=VariableGroup.EDUCATION.value,
                icon="🐟",
                tooltip="Bird's diet",
                sort_order=56,
                searchable=True,
                example="nectar",
            ),
            VariableDefinition(
                name="nest_type",
                display_name="Nest Type",
                type=VariableType.DROPDOWN.value,
                default_value="tree_nest",
                option_library="nest_types",
                required=False,
                placeholder="Select nest type",
                description="Type of nest the bird builds",
                group=VariableGroup.EDUCATION.value,
                icon="🪺",
                tooltip="Nest style",
                sort_order=57,
                searchable=True,
                example="hole_nest",
            ),
            VariableDefinition(
                name="flying_style",
                display_name="Flying Style",
                type=VariableType.DROPDOWN.value,
                default_value="soaring",
                option_library="flying_styles",
                required=False,
                placeholder="Select flying style",
                description="How the bird flies",
                group=VariableGroup.EDUCATION.value,
                icon="🕊️",
                tooltip="Flight pattern",
                sort_order=58,
                searchable=True,
                example="hovering",
            ),
            
            # ============================================================
            # FRUITS LEARNING
            # ============================================================
            VariableDefinition(
                name="fruit_type",
                display_name="Fruit",
                type=VariableType.DROPDOWN.value,
                default_value="apple",
                option_library="fruits",
                required=False,
                placeholder="Select fruit",
                description="Fruit to learn about",
                group=VariableGroup.EDUCATION.value,
                icon="🍎",
                tooltip="Choose a fruit",
                sort_order=59,
                searchable=True,
                example="mango",
            ),
            
            # ============================================================
            # VEGETABLES LEARNING
            # ============================================================
            VariableDefinition(
                name="vegetable_type",
                display_name="Vegetable",
                type=VariableType.DROPDOWN.value,
                default_value="carrot",
                option_library="vegetables",
                required=False,
                placeholder="Select vegetable",
                description="Vegetable to learn about",
                group=VariableGroup.EDUCATION.value,
                icon="🥕",
                tooltip="Choose a vegetable",
                sort_order=60,
                searchable=True,
                example="broccoli",
            ),
            VariableDefinition(
                name="growing_place",
                display_name="Growing Place",
                type=VariableType.DROPDOWN.value,
                default_value="farm",
                option_library="growing_places",
                required=False,
                placeholder="Select place",
                description="Where the vegetable grows",
                group=VariableGroup.EDUCATION.value,
                icon="🌱",
                tooltip="Growing location",
                sort_order=61,
                searchable=True,
                example="garden",
            ),
            
            # ============================================================
            # VEHICLES LEARNING
            # ============================================================
            VariableDefinition(
                name="vehicle_type",
                display_name="Vehicle",
                type=VariableType.DROPDOWN.value,
                default_value="car",
                option_library="vehicles",
                required=False,
                placeholder="Select vehicle",
                description="Vehicle to learn about",
                group=VariableGroup.EDUCATION.value,
                icon="🚗",
                tooltip="Choose a vehicle",
                sort_order=62,
                searchable=True,
                example="airplane",
            ),
            VariableDefinition(
                name="transport_type",
                display_name="Transport Type",
                type=VariableType.DROPDOWN.value,
                default_value="land",
                option_library="transport_types",
                required=False,
                placeholder="Select transport type",
                description="Category of transportation",
                group=VariableGroup.EDUCATION.value,
                icon="🚌",
                tooltip="Transport category",
                sort_order=63,
                searchable=True,
                example="air",
            ),
            VariableDefinition(
                name="fuel_type",
                display_name="Fuel Type",
                type=VariableType.DROPDOWN.value,
                default_value="petrol",
                option_library="fuel_types",
                required=False,
                placeholder="Select fuel",
                description="Energy source for the vehicle",
                group=VariableGroup.EDUCATION.value,
                icon="⛽",
                tooltip="What powers it",
                sort_order=64,
                searchable=True,
                example="electric",
            ),
            VariableDefinition(
                name="vehicle_environment",
                display_name="Environment",
                type=VariableType.DROPDOWN.value,
                default_value="city",
                option_library="environments",
                required=False,
                placeholder="Select environment",
                description="Where the vehicle operates",
                group=VariableGroup.EDUCATION.value,
                icon="🌍",
                tooltip="Operating environment",
                sort_order=65,
                searchable=True,
                example="space",
            ),
            
            # ============================================================
            # BODY PARTS LEARNING
            # ============================================================
            VariableDefinition(
                name="body_part_name",
                display_name="Body Part",
                type=VariableType.DROPDOWN.value,
                default_value="head",
                option_library="body_parts",
                required=False,
                placeholder="Select body part",
                description="Body part to learn about",
                group=VariableGroup.EDUCATION.value,
                icon="👋",
                tooltip="Choose a body part",
                sort_order=66,
                searchable=True,
                example="hands",
            ),
            VariableDefinition(
                name="body_function",
                display_name="Function",
                type=VariableType.DROPDOWN.value,
                default_value="thinking",
                option_library="body_functions",
                required=False,
                placeholder="Select function",
                description="What this body part does",
                group=VariableGroup.EDUCATION.value,
                icon="🫀",
                tooltip="Body part function",
                sort_order=67,
                searchable=True,
                example="seeing",
            ),
            VariableDefinition(
                name="healthy_habit",
                display_name="Healthy Habit",
                type=VariableType.DROPDOWN.value,
                default_value="brush_teeth",
                option_library="healthy_habits",
                required=False,
                placeholder="Select habit",
                description="Good habit for body care",
                group=VariableGroup.EDUCATION.value,
                icon="🌟",
                tooltip="Healthy practice",
                sort_order=68,
                searchable=True,
                example="exercise",
            ),
            
            # ============================================================
            # MONTHS LEARNING
            # ============================================================
            VariableDefinition(
                name="season",
                display_name="Season",
                type=VariableType.DROPDOWN.value,
                default_value="spring",
                option_library="seasons",
                required=False,
                placeholder="Select season",
                description="Season of the year",
                group=VariableGroup.EDUCATION.value,
                icon="🌍",
                tooltip="Time of year",
                sort_order=69,
                searchable=True,
                example="autumn",
            ),
            VariableDefinition(
                name="festival",
                display_name="Festival",
                type=VariableType.DROPDOWN.value,
                default_value="christmas",
                option_library="festivals",
                required=False,
                placeholder="Select festival",
                description="Holiday or celebration",
                group=VariableGroup.EDUCATION.value,
                icon="🎉",
                tooltip="Special day",
                sort_order=70,
                searchable=True,
                example="diwali",
            ),
            VariableDefinition(
                name="month_activity",
                display_name="Activity",
                type=VariableType.DROPDOWN.value,
                default_value="school",
                option_library="daily_routines",
                required=False,
                placeholder="Select activity",
                description="Typical activity for this time",
                group=VariableGroup.EDUCATION.value,
                icon="📅",
                tooltip="Daily routine",
                sort_order=71,
                searchable=True,
                example="play",
            ),
            
            # ============================================================
            # DAYS LEARNING
            # ============================================================
            VariableDefinition(
                name="day_activity",
                display_name="Activity",
                type=VariableType.DROPDOWN.value,
                default_value="school",
                option_library="daily_routines",
                required=False,
                placeholder="Select activity",
                description="Typical activity for this day",
                group=VariableGroup.EDUCATION.value,
                icon="📅",
                tooltip="Daily routine",
                sort_order=72,
                searchable=True,
                example="play",
            ),
            VariableDefinition(
                name="mood",
                display_name="Mood",
                type=VariableType.DROPDOWN.value,
                default_value="happy",
                option_library="moods",
                required=False,
                placeholder="Select mood",
                description="How you feel today",
                group=VariableGroup.EDUCATION.value,
                icon="😊",
                tooltip="Current mood",
                sort_order=73,
                searchable=True,
                example="excited",
            ),
            
            # ============================================================
            # OPPOSITES LEARNING
            # ============================================================
            VariableDefinition(
                name="opposite_pair",
                display_name="Opposite Pair",
                type=VariableType.DROPDOWN.value,
                default_value="big_small",
                option_library="opposite_pairs",
                required=False,
                placeholder="Select opposite pair",
                description="Contrasting concepts to learn",
                group=VariableGroup.EDUCATION.value,
                icon="⚖️",
                tooltip="Opposite concepts",
                sort_order=74,
                searchable=True,
                example="hot_cold",
            ),
            
            # ============================================================
            # PHONICS LEARNING
            # ============================================================
            VariableDefinition(
                name="phonics_sound",
                display_name="Phonics Sound",
                type=VariableType.DROPDOWN.value,
                default_value="a_short",
                option_library="phonics_sounds",
                required=False,
                placeholder="Select sound",
                description="Letter sound for phonics practice",
                group=VariableGroup.EDUCATION.value,
                icon="🔤",
                tooltip="Letter sound",
                sort_order=75,
                searchable=True,
                example="b",
            ),
            
            # ============================================================
            # SPELLING LEARNING
            # ============================================================
            VariableDefinition(
                name="spelling_difficulty",
                display_name="Difficulty",
                type=VariableType.DROPDOWN.value,
                default_value="easy",
                option_library="quiz_difficulty",
                required=False,
                placeholder="Select difficulty",
                description="Spelling challenge level",
                group=VariableGroup.EDUCATION.value,
                icon="📊",
                tooltip="Challenge level",
                sort_order=76,
                searchable=True,
                example="medium",
            ),
            
            # ============================================================
            # MATH QUIZ
            # ============================================================
            VariableDefinition(
                name="math_quiz_topic",
                display_name="Topic",
                type=VariableType.DROPDOWN.value,
                default_value="addition",
                option_library="quiz_topics",
                required=False,
                placeholder="Select topic",
                description="Math topic for the quiz",
                group=VariableGroup.EDUCATION.value,
                icon="❓",
                tooltip="Quiz subject",
                sort_order=77,
                searchable=True,
                example="multiplication",
            ),
            VariableDefinition(
                name="math_quiz_difficulty",
                display_name="Difficulty",
                type=VariableType.DROPDOWN.value,
                default_value="easy",
                option_library="quiz_difficulty",
                required=False,
                placeholder="Select difficulty",
                description="Quiz difficulty level",
                group=VariableGroup.EDUCATION.value,
                icon="📊",
                tooltip="Challenge level",
                sort_order=78,
                searchable=True,
                example="hard",
            ),
            
            # ============================================================
            # SCIENCE QUIZ
            # ============================================================
            VariableDefinition(
                name="science_quiz_topic",
                display_name="Topic",
                type=VariableType.DROPDOWN.value,
                default_value="animals",
                option_library="quiz_topics",
                required=False,
                placeholder="Select topic",
                description="Science topic for the quiz",
                group=VariableGroup.EDUCATION.value,
                icon="❓",
                tooltip="Quiz subject",
                sort_order=79,
                searchable=True,
                example="space",
            ),
            VariableDefinition(
                name="science_quiz_difficulty",
                display_name="Difficulty",
                type=VariableType.DROPDOWN.value,
                default_value="easy",
                option_library="quiz_difficulty",
                required=False,
                placeholder="Select difficulty",
                description="Quiz difficulty level",
                group=VariableGroup.EDUCATION.value,
                icon="📊",
                tooltip="Challenge level",
                sort_order=80,
                searchable=True,
                example="medium",
            ),
            
            # ============================================================
            # GK QUIZ
            # ============================================================
            VariableDefinition(
                name="gk_quiz_topic",
                display_name="Topic",
                type=VariableType.DROPDOWN.value,
                default_value="countries",
                option_library="quiz_topics",
                required=False,
                placeholder="Select topic",
                description="General knowledge topic for the quiz",
                group=VariableGroup.EDUCATION.value,
                icon="❓",
                tooltip="Quiz subject",
                sort_order=81,
                searchable=True,
                example="history",
            ),
            VariableDefinition(
                name="gk_quiz_difficulty",
                display_name="Difficulty",
                type=VariableType.DROPDOWN.value,
                default_value="easy",
                option_library="quiz_difficulty",
                required=False,
                placeholder="Select difficulty",
                description="Quiz difficulty level",
                group=VariableGroup.EDUCATION.value,
                icon="📊",
                tooltip="Challenge level",
                sort_order=82,
                searchable=True,
                example="expert",
            ),
            
            # ============================================================
            # STORIES GROUP (15+ variables - fully integrated with OptionLibrary)
            # ============================================================
            VariableDefinition(
                name="theme",
                display_name="Theme",
                type=VariableType.DROPDOWN.value,
                default_value="theme_friendship",
                option_library="story_themes",
                required=False,
                placeholder="Select theme",
                description="Main theme or moral of the story",
                group=VariableGroup.STORIES.value,
                icon="🌟",
                tooltip="What the story teaches",
                sort_order=1,
                searchable=True,
                example="theme_kindness",
            ),
            VariableDefinition(
                name="setting",
                display_name="Setting",
                type=VariableType.DROPDOWN.value,
                default_value="setting_forest",
                option_library="story_settings",
                required=False,
                placeholder="Select setting",
                description="Where the story takes place",
                group=VariableGroup.STORIES.value,
                icon="🏞️",
                tooltip="Story location",
                sort_order=2,
                searchable=True,
                example="setting_castle",
            ),
            VariableDefinition(
                name="story_length",
                display_name="Story Length",
                type=VariableType.DROPDOWN.value,
                default_value="medium",
                option_library="story_lengths",
                required=False,
                placeholder="Select length",
                description="Target length of the story",
                group=VariableGroup.STORIES.value,
                icon="📏",
                tooltip="How long the story should be",
                sort_order=3,
                example="long",
            ),
            VariableDefinition(
                name="ending_style",
                display_name="Ending Style",
                type=VariableType.DROPDOWN.value,
                default_value="ending_happy",
                option_library="ending_styles",
                required=False,
                placeholder="Select ending",
                description="How the story concludes",
                group=VariableGroup.STORIES.value,
                icon="🏁",
                tooltip="Story resolution type",
                sort_order=4,
                example="ending_surprise",
            ),
            VariableDefinition(
                name="conflict",
                display_name="Conflict",
                type=VariableType.DROPDOWN.value,
                default_value="conflict_lost_item",
                option_library="conflict_types",
                required=False,
                placeholder="Select conflict",
                description="Central problem to resolve",
                group=VariableGroup.STORIES.value,
                icon="⚔️",
                tooltip="Main challenge",
                sort_order=5,
                searchable=True,
                example="conflict_mystery",
            ),
            VariableDefinition(
                name="reward",
                display_name="Reward",
                type=VariableType.DROPDOWN.value,
                default_value="reward_treasure",
                option_library="rewards",
                required=False,
                placeholder="Select reward",
                description="Reward received in story outcome",
                group=VariableGroup.STORIES.value,
                icon="🏆",
                tooltip="Story reward",
                sort_order=6,
                searchable=True,
                example="reward_friendship",
            ),
            VariableDefinition(
                name="problem",
                display_name="Problem",
                type=VariableType.DROPDOWN.value,
                default_value="problem_lost_toy",
                option_library="problems",
                required=False,
                placeholder="Select problem",
                description="Child-friendly story problem to solve",
                group=VariableGroup.STORIES.value,
                icon="🧩",
                tooltip="Story problem",
                sort_order=7,
                searchable=True,
                example="problem_missing_pet",
            ),
            VariableDefinition(
                name="solution",
                display_name="Solution",
                type=VariableType.DROPDOWN.value,
                default_value="solution_find_friend",
                option_library="solutions",
                required=False,
                placeholder="Select solution",
                description="Positive solution for story problem",
                group=VariableGroup.STORIES.value,
                icon="🛠️",
                tooltip="Story solution",
                sort_order=8,
                searchable=True,
                example="solution_work_together",
            ),
            VariableDefinition(
                name="magical_element",
                display_name="Magical Element",
                type=VariableType.DROPDOWN.value,
                default_value="magic_wand",
                option_library="magical_elements",
                required=False,
                placeholder="Select magical element",
                description="Magical objects and creatures for stories",
                group=VariableGroup.STORIES.value,
                icon="🪄",
                tooltip="Magical element",
                sort_order=9,
                searchable=True,
                example="fairy_dust",
            ),
            VariableDefinition(
                name="islamic_value",
                display_name="Islamic Value",
                type=VariableType.DROPDOWN.value,
                default_value="islamic_honesty",
                option_library="islamic_values",
                required=False,
                placeholder="Select Islamic value",
                description="Values and virtues for Islamic stories",
                group=VariableGroup.STORIES.value,
                icon="🕌",
                tooltip="Islamic value",
                sort_order=10,
                searchable=True,
                example="islamic_patience",
            ),
            VariableDefinition(
                name="dua",
                display_name="Dua",
                type=VariableType.DROPDOWN.value,
                default_value="dua_subhan_allah",
                option_library="duas",
                required=False,
                placeholder="Select dua",
                description="Short child-friendly duas for stories",
                group=VariableGroup.STORIES.value,
                icon="🕌",
                tooltip="Dua for story",
                sort_order=11,
                searchable=True,
                example="dua_alhamdulillah",
            ),
            VariableDefinition(
                name="space_vehicle",
                display_name="Space Vehicle",
                type=VariableType.DROPDOWN.value,
                default_value="space_vehicle_rocket",
                option_library="space_vehicles",
                required=False,
                placeholder="Select space vehicle",
                description="Vehicles for space adventure stories",
                group=VariableGroup.STORIES.value,
                icon="🚀",
                tooltip="Space vehicle",
                sort_order=12,
                searchable=True,
                example="space_vehicle_explorer_ship",
            ),
            VariableDefinition(
                name="mission",
                display_name="Mission",
                type=VariableType.DROPDOWN.value,
                default_value="mission_rescue",
                option_library="missions",
                required=False,
                placeholder="Select mission",
                description="Mission objectives for stories",
                group=VariableGroup.STORIES.value,
                icon="🎯",
                tooltip="Story mission",
                sort_order=13,
                searchable=True,
                example="mission_exploration",
            ),
            VariableDefinition(
                name="funny_situation",
                display_name="Funny Situation",
                type=VariableType.DROPDOWN.value,
                default_value="funny_banana_peel",
                option_library="funny_situations",
                required=False,
                placeholder="Select funny situation",
                description="Silly situations for lighthearted stories",
                group=VariableGroup.STORIES.value,
                icon="😂",
                tooltip="Funny situation",
                sort_order=14,
                searchable=True,
                example="funny_dancing_elephant",
            ),
            VariableDefinition(
                name="mystery",
                display_name="Mystery",
                type=VariableType.DROPDOWN.value,
                default_value="mystery_missing_key",
                option_library="mysteries",
                required=False,
                placeholder="Select mystery",
                description="Mysteries and puzzles for stories",
                group=VariableGroup.STORIES.value,
                icon="🕵️",
                tooltip="Story mystery",
                sort_order=15,
                searchable=True,
                example="mystery_hidden_treasure",
            ),
            VariableDefinition(
                name="clues",
                display_name="Clues",
                type=VariableType.DROPDOWN.value,
                default_value="clue_footprints",
                option_library="clues",
                required=False,
                placeholder="Select clue",
                description="Clues to help solve story mysteries",
                group=VariableGroup.STORIES.value,
                icon="🕵️",
                tooltip="Story clue",
                sort_order=16,
                searchable=True,
                example="clue_feather",
            ),
            VariableDefinition(
                name="genre",
                display_name="Genre",
                type=VariableType.DROPDOWN.value,
                default_value="fantasy",
                option_library="story_genres",
                required=False,
                placeholder="Select genre",
                description="Literary genre of the story",
                group=VariableGroup.STORIES.value,
                icon="🏰",
                tooltip="Story category",
                sort_order=17,
                searchable=True,
                example="science_fiction",
            ),
            
            # ============================================================
            # TEXT VARIABLES (NO DROPDOWN) - Keep as text/autocomplete
            # ============================================================
            VariableDefinition(
                name="title",
                display_name="Title",
                type=VariableType.TEXT.value,
                default_value="A Magical Adventure",
                required=False,
                placeholder="Enter story title",
                description="Title of the story",
                group=VariableGroup.STORIES.value,
                icon="📖",
                tooltip="Story title",
                sort_order=18,
                example="The Dragon Who Loved to Bake",
            ),
            VariableDefinition(
                name="main_character",
                display_name="Main Character",
                type=VariableType.TEXT.value,
                default_value="Luna the Brave",
                required=False,
                placeholder="Enter main character name",
                description="Protagonist of the story",
                group=VariableGroup.STORIES.value,
                icon="🦸",
                tooltip="Hero of the story",
                sort_order=19,
                example="Captain Cosmos",
            ),
            VariableDefinition(
                name="supporting_character",
                display_name="Supporting Character",
                type=VariableType.TEXT.value,
                default_value="Pip the Penguin",
                required=False,
                placeholder="Enter supporting character",
                description="Supporting character in the story",
                group=VariableGroup.STORIES.value,
                icon="🐧",
                tooltip="Friend or companion",
                sort_order=20,
                example="Professor Owl",
            ),
            VariableDefinition(
                name="companion",
                display_name="Companion",
                type=VariableType.TEXT.value,
                default_value="Pip the Penguin",
                required=False,
                placeholder="Enter companion name",
                description="Companion character",
                group=VariableGroup.STORIES.value,
                icon="🐧",
                tooltip="Companion character",
                sort_order=21,
                example="Spark the Dragon",
            ),
            VariableDefinition(
                name="hero",
                display_name="Hero",
                type=VariableType.TEXT.value,
                default_value="Captain Cosmos",
                required=False,
                placeholder="Enter hero name",
                description="Hero of the adventure",
                group=VariableGroup.STORIES.value,
                icon="🦸",
                tooltip="Adventure hero",
                sort_order=22,
                example="Sir Gallant",
            ),
            VariableDefinition(
                name="sidekick",
                display_name="Sidekick",
                type=VariableType.TEXT.value,
                default_value="Sparky the Robot",
                required=False,
                placeholder="Enter sidekick name",
                description="Hero's sidekick",
                group=VariableGroup.STORIES.value,
                icon="🤖",
                tooltip="Hero's companion",
                sort_order=23,
                example="Whiskers the Cat",
            ),
            VariableDefinition(
                name="villain",
                display_name="Villain",
                type=VariableType.TEXT.value,
                default_value="The Shadow King",
                required=False,
                placeholder="Enter villain name",
                description="Antagonist of the story",
                group=VariableGroup.STORIES.value,
                icon="👑",
                tooltip="The bad guy",
                sort_order=24,
                example="Dr. Chaos",
            ),
            VariableDefinition(
                name="princess",
                display_name="Princess",
                type=VariableType.TEXT.value,
                default_value="Princess Aurora",
                required=False,
                placeholder="Enter princess name",
                description="Princess character",
                group=VariableGroup.STORIES.value,
                icon="👸",
                tooltip="Princess character",
                sort_order=25,
                example="Princess Jasmine",
            ),
            VariableDefinition(
                name="prince",
                display_name="Prince",
                type=VariableType.TEXT.value,
                default_value="Prince Charming",
                required=False,
                placeholder="Enter prince name",
                description="Prince character",
                group=VariableGroup.STORIES.value,
                icon="🤴",
                tooltip="Prince character",
                sort_order=26,
                example="Prince Eric",
            ),
            VariableDefinition(
                name="magical_character",
                display_name="Magical Character",
                type=VariableType.TEXT.value,
                default_value="Fairy Godmother",
                required=False,
                placeholder="Enter magical character",
                description="Magical character in the story",
                group=VariableGroup.STORIES.value,
                icon="🧚",
                tooltip="Magical character",
                sort_order=27,
                example="Merlin the Wizard",
            ),
            VariableDefinition(
                name="prophet_or_personality",
                display_name="Prophet or Personality",
                type=VariableType.TEXT.value,
                default_value="Prophet Muhammad (PBUH)",
                required=False,
                placeholder="Enter prophet or personality",
                description="Islamic prophet or personality",
                group=VariableGroup.STORIES.value,
                icon="🕌",
                tooltip="Prophet or personality",
                sort_order=28,
                example="Prophet Ibrahim (AS)",
            ),
            VariableDefinition(
                name="main_animal",
                display_name="Main Animal",
                type=VariableType.TEXT.value,
                default_value="Leo the Lion",
                required=False,
                placeholder="Enter main animal",
                description="Main animal character",
                group=VariableGroup.STORIES.value,
                icon="🦁",
                tooltip="Main animal",
                sort_order=29,
                example="Ellie the Elephant",
            ),
            VariableDefinition(
                name="animal_friend",
                display_name="Animal Friend",
                type=VariableType.TEXT.value,
                default_value="Milo the Monkey",
                required=False,
                placeholder="Enter animal friend",
                description="Animal friend character",
                group=VariableGroup.STORIES.value,
                icon="🐒",
                tooltip="Animal friend",
                sort_order=30,
                example="Zara the Zebra",
            ),
            VariableDefinition(
                name="astronaut",
                display_name="Astronaut",
                type=VariableType.TEXT.value,
                default_value="Captain Nova",
                required=False,
                placeholder="Enter astronaut name",
                description="Astronaut character",
                group=VariableGroup.STORIES.value,
                icon="👨‍🚀",
                tooltip="Astronaut character",
                sort_order=31,
                example="Commander Vega",
            ),
            VariableDefinition(
                name="alien",
                display_name="Alien",
                type=VariableType.TEXT.value,
                default_value="Zog the Friendly Alien",
                required=False,
                placeholder="Enter alien name",
                description="Alien character",
                group=VariableGroup.STORIES.value,
                icon="👽",
                tooltip="Alien character",
                sort_order=32,
                example="Glimmer the Star Being",
            ),
            VariableDefinition(
                name="funny_friend",
                display_name="Funny Friend",
                type=VariableType.TEXT.value,
                default_value="Benny the Bunny",
                required=False,
                placeholder="Enter funny friend",
                description="Funny friend character",
                group=VariableGroup.STORIES.value,
                icon="🐰",
                tooltip="Funny friend",
                sort_order=33,
                example="Chuckles the Chipmunk",
            ),
            VariableDefinition(
                name="detective",
                display_name="Detective",
                type=VariableType.TEXT.value,
                default_value="Detective Daisy",
                required=False,
                placeholder="Enter detective name",
                description="Detective character",
                group=VariableGroup.STORIES.value,
                icon="🕵️",
                tooltip="Detective character",
                sort_order=34,
                example="Inspector Whiskers",
            ),
            VariableDefinition(
                name="assistant",
                display_name="Assistant",
                type=VariableType.TEXT.value,
                default_value="Officer Ollie",
                required=False,
                placeholder="Enter assistant name",
                description="Detective's assistant",
                group=VariableGroup.STORIES.value,
                icon="👮",
                tooltip="Assistant character",
                sort_order=35,
                example="Sergeant Paws",
            ),
            
            # ============================================================
            # IMAGES GROUP (20 variables)
            # ============================================================
            VariableDefinition(
                name="art_style",
                display_name="Art Style",
                type=VariableType.DROPDOWN.value,
                default_value="pixar",
                option_library="art_styles",
                required=False,
                placeholder="Select art style",
                description="Visual artistic style for generation",
                group=VariableGroup.IMAGES.value,
                icon="🎨",
                tooltip="Choose the art style",
                sort_order=1,
                searchable=True,
                example="watercolor",
            ),
            VariableDefinition(
                name="camera_angle",
                display_name="Camera Angle",
                type=VariableType.DROPDOWN.value,
                default_value="eye_level",
                option_library="camera_angles",
                required=False,
                placeholder="Select camera angle",
                description="Camera perspective for the image",
                group=VariableGroup.IMAGES.value,
                icon="📷",
                tooltip="Viewpoint angle",
                sort_order=2,
                searchable=True,
                example="low_angle",
            ),
            VariableDefinition(
                name="lighting",
                display_name="Lighting",
                type=VariableType.DROPDOWN.value,
                default_value="natural",
                option_library="lighting_styles",
                required=False,
                placeholder="Select lighting",
                description="Lighting setup for the scene",
                group=VariableGroup.IMAGES.value,
                icon="💡",
                tooltip="Lighting style",
                sort_order=3,
                searchable=True,
                example="golden_hour",
            ),
            VariableDefinition(
                name="background",
                display_name="Background",
                type=VariableType.TEXT.value,
                default_value="sunset meadow",
                required=False,
                placeholder="Describe background",
                description="Background setting description",
                group=VariableGroup.IMAGES.value,
                icon="🌄",
                tooltip="Scene background",
                sort_order=4,
                example="starry night sky",
            ),
            VariableDefinition(
                name="composition",
                display_name="Composition",
                type=VariableType.DROPDOWN.value,
                default_value="rule_of_thirds",
                option_library="composition_rules",
                required=False,
                placeholder="Select composition",
                description="Photographic composition rule",
                group=VariableGroup.IMAGES.value,
                icon="📐",
                tooltip="Frame composition",
                sort_order=5,
                example="golden_ratio",
            ),
            VariableDefinition(
                name="render_engine",
                display_name="Render Engine",
                type=VariableType.DROPDOWN.value,
                default_value="cycles",
                option_library="render_engines",
                required=False,
                placeholder="Select render engine",
                description="3D rendering engine to use",
                group=VariableGroup.IMAGES.value,
                icon="🎮",
                tooltip="Rendering backend",
                sort_order=6,
                example="octane",
            ),
            VariableDefinition(
                name="pose",
                display_name="Character Pose",
                type=VariableType.TEXT.value,
                default_value="standing confidently",
                required=False,
                placeholder="Describe pose",
                description="Character body position",
                group=VariableGroup.IMAGES.value,
                icon="🧍",
                tooltip="How the character stands",
                sort_order=7,
                example="sitting on a rock",
            ),
            VariableDefinition(
                name="expression",
                display_name="Facial Expression",
                type=VariableType.DROPDOWN.value,
                default_value="smile",
                option_library="expressions",
                required=False,
                placeholder="Select expression",
                description="Character facial expression",
                group=VariableGroup.IMAGES.value,
                icon="😊",
                tooltip="Face emotion",
                sort_order=8,
                searchable=True,
                example="wonder",
            ),
            VariableDefinition(
                name="hair_style",
                display_name="Hair Style",
                type=VariableType.DROPDOWN.value,
                default_value="long",
                option_library="hair_styles",
                required=False,
                placeholder="Select hair style",
                description="Character hair style",
                group=VariableGroup.IMAGES.value,
                icon="💇",
                tooltip="Haircut type",
                sort_order=9,
                searchable=True,
                example="braid",
            ),
            VariableDefinition(
                name="hair_color",
                display_name="Hair Color",
                type=VariableType.DROPDOWN.value,
                default_value="brown",
                option_library="hair_colors",
                required=False,
                placeholder="Select hair color",
                description="Character hair color",
                group=VariableGroup.IMAGES.value,
                icon="🎨",
                tooltip="Hair color",
                sort_order=10,
                searchable=True,
                example="pink",
            ),
            VariableDefinition(
                name="eye_color",
                display_name="Eye Color",
                type=VariableType.DROPDOWN.value,
                default_value="brown",
                option_library="eye_colors",
                required=False,
                placeholder="Select eye color",
                description="Character eye color",
                group=VariableGroup.IMAGES.value,
                icon="👁️",
                tooltip="Eye color",
                sort_order=11,
                searchable=True,
                example="blue",
            ),
            VariableDefinition(
                name="accessories",
                display_name="Accessories",
                type=VariableType.MULTISELECT.value,
                default_value="",
                option_library="accessories",
                required=False,
                placeholder="Select accessories",
                description="Character accessories",
                group=VariableGroup.IMAGES.value,
                icon="🎒",
                tooltip="Items worn or carried",
                sort_order=12,
                searchable=True,
                allow_custom=True,
                example="glasses, backpack",
            ),
            VariableDefinition(
                name="texture",
                display_name="Texture Style",
                type=VariableType.DROPDOWN.value,
                default_value="smooth",
                option_library="textures",
                required=False,
                placeholder="Select texture",
                description="Surface texture quality",
                group=VariableGroup.IMAGES.value,
                icon="🧱",
                tooltip="Material texture",
                sort_order=13,
                searchable=True,
                example="fur",
            ),
            VariableDefinition(
                name="quality",
                display_name="Quality",
                type=VariableType.DROPDOWN.value,
                default_value="high",
                option_library="quality_presets",
                required=False,
                placeholder="Select quality",
                description="Output quality level",
                group=VariableGroup.IMAGES.value,
                icon="⭐",
                tooltip="Render quality",
                sort_order=14,
                example="ultra",
            ),
            VariableDefinition(
                name="aspect_ratio",
                display_name="Aspect Ratio",
                type=VariableType.DROPDOWN.value,
                default_value="16:9",
                option_library="aspect_ratios",
                required=False,
                placeholder="Select ratio",
                description="Image aspect ratio",
                group=VariableGroup.IMAGES.value,
                icon="📐",
                tooltip="Width:height ratio",
                sort_order=15,
                example="9:16",
            ),
            VariableDefinition(
                name="resolution",
                display_name="Resolution",
                type=VariableType.DROPDOWN.value,
                default_value="1920x1080",
                option_library="resolutions",
                required=False,
                placeholder="Select resolution",
                description="Output image resolution",
                group=VariableGroup.IMAGES.value,
                icon="🖥️",
                tooltip="Pixel dimensions",
                sort_order=16,
                example="3840x2160",
            ),
            VariableDefinition(
                name="color_palette",
                display_name="Color Palette",
                type=VariableType.DROPDOWN.value,
                default_value="warm",
                option_library="color_palettes",
                required=False,
                placeholder="Select palette",
                description="Color scheme for the image",
                group=VariableGroup.IMAGES.value,
                icon="🎨",
                tooltip="Color harmony",
                sort_order=17,
                searchable=True,
                example="complementary",
            ),
            VariableDefinition(
                name="mood",
                display_name="Mood",
                type=VariableType.DROPDOWN.value,
                default_value="cheerful",
                option_library="moods",
                required=False,
                placeholder="Select mood",
                description="Atmospheric mood of the image",
                group=VariableGroup.IMAGES.value,
                icon="🌈",
                tooltip="Emotional tone",
                sort_order=18,
                searchable=True,
                example="mysterious",
            ),
            VariableDefinition(
                name="subject",
                display_name="Main Subject",
                type=VariableType.TEXT.value,
                default_value="cute dragon",
                required=True,
                placeholder="Describe main subject",
                description="Primary focus of the image",
                group=VariableGroup.IMAGES.value,
                icon="🎯",
                tooltip="What to generate",
                sort_order=19,
                example="robot friend",
            ),
            VariableDefinition(
                name="style",
                display_name="Style Modifier",
                type=VariableType.TEXT.value,
                default_value="whimsical, detailed, vibrant",
                required=False,
                placeholder="Style keywords",
                description="Additional style descriptors",
                group=VariableGroup.IMAGES.value,
                icon="✨",
                tooltip="Extra style cues",
                sort_order=20,
                example="cinematic, volumetric lighting",
            ),
            
            # ============================================================
            # VIDEOS GROUP (12 variables)
            # ============================================================
            VariableDefinition(
                name="duration",
                display_name="Duration",
                type=VariableType.DROPDOWN.value,
                default_value="30s",
                option_library="video_durations",
                required=False,
                placeholder="Select duration",
                description="Video length",
                group=VariableGroup.VIDEOS.value,
                icon="⏱️",
                tooltip="How long the video is",
                sort_order=1,
                example="2m",
            ),
            VariableDefinition(
                name="fps",
                display_name="Frame Rate",
                type=VariableType.DROPDOWN.value,
                default_value="30",
                option_library="fps_options",
                required=False,
                placeholder="Select FPS",
                description="Frames per second",
                group=VariableGroup.VIDEOS.value,
                icon="🎞️",
                tooltip="Animation smoothness",
                sort_order=2,
                example="60",
            ),
            VariableDefinition(
                name="video_resolution",
                display_name="Resolution",
                type=VariableType.DROPDOWN.value,
                default_value="1920x1080",
                option_library="resolutions",
                required=False,
                placeholder="Select resolution",
                description="Video resolution",
                group=VariableGroup.VIDEOS.value,
                icon="🖥️",
                tooltip="Video dimensions",
                sort_order=3,
                example="3840x2160",
            ),
            VariableDefinition(
                name="video_aspect_ratio",
                display_name="Aspect Ratio",
                type=VariableType.DROPDOWN.value,
                default_value="16:9",
                option_library="aspect_ratios",
                required=False,
                placeholder="Select ratio",
                description="Video aspect ratio",
                group=VariableGroup.VIDEOS.value,
                icon="📐",
                tooltip="Width:height ratio",
                sort_order=4,
                example="9:16",
            ),
            VariableDefinition(
                name="animation_style",
                display_name="Animation Style",
                type=VariableType.DROPDOWN.value,
                default_value="3d_cgi",
                option_library="animation_styles",
                required=False,
                placeholder="Select style",
                description="Animation technique",
                group=VariableGroup.VIDEOS.value,
                icon="🎬",
                tooltip="Animation method",
                sort_order=5,
                searchable=True,
                example="2d_traditional",
            ),
            VariableDefinition(
                name="transition",
                display_name="Transition",
                type=VariableType.DROPDOWN.value,
                default_value="cut",
                option_library="transitions",
                required=False,
                placeholder="Select transition",
                description="Scene transition effect",
                group=VariableGroup.VIDEOS.value,
                icon="✂️",
                tooltip="Transition type",
                sort_order=6,
                example="fade",
            ),
            VariableDefinition(
                name="camera_movement",
                display_name="Camera Movement",
                type=VariableType.DROPDOWN.value,
                default_value="static",
                option_library="camera_movements",
                required=False,
                placeholder="Select movement",
                description="Cinematic camera movement",
                group=VariableGroup.VIDEOS.value,
                icon="🎥",
                tooltip="Camera motion",
                sort_order=7,
                searchable=True,
                example="dolly",
            ),
            VariableDefinition(
                name="music_style",
                display_name="Music Style",
                type=VariableType.DROPDOWN.value,
                default_value="kids",
                option_library="music_styles",
                required=False,
                placeholder="Select music",
                description="Background music genre",
                group=VariableGroup.VIDEOS.value,
                icon="🎵",
                tooltip="Background music",
                sort_order=8,
                searchable=True,
                example="orchestral",
            ),
            VariableDefinition(
                name="voice_style",
                display_name="Voice Style",
                type=VariableType.DROPDOWN.value,
                default_value="teacher",
                option_library="voice_styles",
                required=False,
                placeholder="Select voice style",
                description="Speaking style for narration",
                group=VariableGroup.VIDEOS.value,
                icon="🎙️",
                tooltip="Narration style",
                sort_order=9,
                searchable=True,
                example="storyteller",
            ),
            VariableDefinition(
                name="video_quality",
                display_name="Quality",
                type=VariableType.DROPDOWN.value,
                default_value="high",
                option_library="quality_presets",
                required=False,
                placeholder="Select quality",
                description="Output quality level",
                group=VariableGroup.VIDEOS.value,
                icon="⭐",
                tooltip="Render quality",
                sort_order=10,
                example="ultra",
            ),
            VariableDefinition(
                name="video_subject",
                display_name="Subject",
                type=VariableType.TEXT.value,
                default_value="learning colors",
                required=True,
                placeholder="Describe video topic",
                description="Main topic of the video",
                group=VariableGroup.VIDEOS.value,
                icon="🎯",
                tooltip="Video subject",
                sort_order=11,
                example="counting to 10",
            ),
            VariableDefinition(
                name="target_age",
                display_name="Target Age",
                type=VariableType.DROPDOWN.value,
                default_value="preschool",
                option_library="age_groups",
                required=False,
                placeholder="Select age group",
                description="Intended viewer age group",
                group=VariableGroup.VIDEOS.value,
                icon="👶",
                tooltip="Target audience",
                sort_order=12,
                searchable=True,
                example="early_childhood",
            ),
            
            # ============================================================
            # VOICES GROUP (8 variables)
            # ============================================================
            VariableDefinition(
                name="voice_preset",
                display_name="Voice Preset",
                type=VariableType.DROPDOWN.value,
                default_value="female_adult",
                option_library="voices",
                required=False,
                placeholder="Select voice",
                description="Voice character preset",
                group=VariableGroup.VOICES.value,
                icon="🎙️",
                tooltip="Voice character",
                sort_order=1,
                searchable=True,
                example="storyteller",
            ),
            VariableDefinition(
                name="accent",
                display_name="Accent",
                type=VariableType.DROPDOWN.value,
                default_value="american",
                option_library="accents",
                required=False,
                placeholder="Select accent",
                description="Regional accent for voice",
                group=VariableGroup.VOICES.value,
                icon="🗣️",
                tooltip="Regional accent",
                sort_order=2,
                searchable=True,
                example="british",
            ),
            VariableDefinition(
                name="voice_style",
                display_name="Voice Style",
                type=VariableType.DROPDOWN.value,
                default_value="conversational",
                option_library="voice_styles",
                required=False,
                placeholder="Select style",
                description="Speaking style",
                group=VariableGroup.VOICES.value,
                icon="🎙️",
                tooltip="How the voice sounds",
                sort_order=3,
                searchable=True,
                example="narrator",
            ),
            VariableDefinition(
                name="language",
                display_name="Language",
                type=VariableType.DROPDOWN.value,
                default_value="english",
                option_library="languages",
                required=False,
                placeholder="Select language",
                description="Language for voice generation",
                group=VariableGroup.VOICES.value,
                icon="🌍",
                tooltip="Voice language",
                sort_order=4,
                searchable=True,
                example="spanish",
            ),
            VariableDefinition(
                name="speed",
                display_name="Speed",
                type=VariableType.SLIDER.value,
                default_value="1.0",
                required=False,
                placeholder="0.5 - 2.0",
                description="Speech speed multiplier",
                group=VariableGroup.VOICES.value,
                icon="⚡",
                tooltip="How fast to speak",
                sort_order=5,
                min_value=0.5,
                max_value=2.0,
                example="1.2",
                unit="x",
            ),
            VariableDefinition(
                name="pitch",
                display_name="Pitch",
                type=VariableType.SLIDER.value,
                default_value="0",
                required=False,
                placeholder="-12 to +12",
                description="Voice pitch adjustment",
                group=VariableGroup.VOICES.value,
                icon="🎵",
                tooltip="Voice pitch",
                sort_order=6,
                min_value=-12,
                max_value=12,
                example="2",
                unit="semitones",
            ),
            VariableDefinition(
                name="emotion",
                display_name="Emotion",
                type=VariableType.DROPDOWN.value,
                default_value="cheerful",
                option_library="emotions",
                required=False,
                placeholder="Select emotion",
                description="Emotional tone of voice",
                group=VariableGroup.VOICES.value,
                icon="😊",
                tooltip="Voice emotion",
                sort_order=7,
                searchable=True,
                example="excited",
            ),
            VariableDefinition(
                name="text",
                display_name="Text to Speak",
                type=VariableType.TEXTAREA.value,
                default_value="Hello! Welcome to AI Kids Studio!",
                required=True,
                placeholder="Enter text to convert to speech",
                description="Text content for voice generation",
                group=VariableGroup.VOICES.value,
                icon="📝",
                tooltip="What to say",
                sort_order=8,
                max_value=5000,
                example="Once upon a time...",
            ),
            
            # ============================================================
            # YOUTUBE GROUP (10 variables)
            # ============================================================
            VariableDefinition(
                name="platform",
                display_name="Platform",
                type=VariableType.DROPDOWN.value,
                default_value="youtube",
                options=["youtube", "youtube_shorts", "youtube_kids"],
                required=False,
                placeholder="Select platform",
                description="YouTube platform variant",
                group=VariableGroup.YOUTUBE.value,
                icon="📺",
                tooltip="Where to publish",
                sort_order=1,
                example="youtube_shorts",
            ),
            VariableDefinition(
                name="video_title",
                display_name="Video Title",
                type=VariableType.TEXT.value,
                default_value="Learn Colors with Fun Animation!",
                required=True,
                placeholder="Enter video title",
                description="Title for the YouTube video",
                group=VariableGroup.YOUTUBE.value,
                icon="📝",
                tooltip="Video title",
                sort_order=2,
                max_value=100,
                example="Count to 10 with Animals!",
            ),
            VariableDefinition(
                name="description",
                display_name="Description",
                type=VariableType.TEXTAREA.value,
                default_value="Join us for a fun learning adventure!",
                required=False,
                placeholder="Enter description",
                description="Video description",
                group=VariableGroup.YOUTUBE.value,
                icon="📄",
                tooltip="Video description",
                sort_order=3,
                max_value=5000,
                example="Learn numbers 1-10...",
            ),
            VariableDefinition(
                name="tags",
                display_name="Tags",
                type=VariableType.TEXT.value,
                default_value="kids, education, learning, colors",
                required=False,
                placeholder="Comma-separated tags",
                description="Search tags for discovery",
                group=VariableGroup.YOUTUBE.value,
                icon="🏷️",
                tooltip="Video tags",
                sort_order=4,
                max_value=500,
                example="numbers, counting, math",
            ),
            VariableDefinition(
                name="thumbnail_style",
                display_name="Thumbnail Style",
                type=VariableType.DROPDOWN.value,
                default_value="bright_colorful",
                options=["bright_colorful", "minimal", "character_focus", "before_after", "text_heavy", "mystery"],
                required=False,
                placeholder="Select style",
                description="Thumbnail design approach",
                group=VariableGroup.YOUTUBE.value,
                icon="🖼️",
                tooltip="Thumbnail look",
                sort_order=5,
                example="character_focus",
            ),
            VariableDefinition(
                name="target_audience",
                display_name="Target Audience",
                type=VariableType.DROPDOWN.value,
                default_value="kids_6_12",
                option_library="age_groups",
                required=False,
                placeholder="Select audience",
                description="Intended viewer age group",
                group=VariableGroup.YOUTUBE.value,
                icon="👨‍👩‍👧‍👦",
                tooltip="Who watches",
                sort_order=6,
                searchable=True,
                example="teens",
            ),
            VariableDefinition(
                name="upload_schedule",
                display_name="Upload Schedule",
                type=VariableType.DROPDOWN.value,
                default_value="weekly",
                options=["daily", "weekly", "biweekly", "monthly", "custom"],
                required=False,
                placeholder="Select frequency",
                description="Publishing frequency",
                group=VariableGroup.YOUTUBE.value,
                icon="📅",
                tooltip="How often to post",
                sort_order=7,
                example="daily",
            ),
            VariableDefinition(
                name="call_to_action",
                display_name="Call to Action",
                type=VariableType.TEXT.value,
                default_value="Subscribe for more fun videos!",
                required=False,
                placeholder="Enter CTA",
                description="End screen call to action",
                group=VariableGroup.YOUTUBE.value,
                icon="🔔",
                tooltip="What to ask viewers",
                sort_order=8,
                max_value=200,
                example="Like and comment below!",
            ),
            VariableDefinition(
                name="seo_keywords",
                display_name="SEO Keywords",
                type=VariableType.TEXT.value,
                default_value="kids learning, educational videos",
                required=False,
                placeholder="Enter keywords",
                description="Search optimization keywords",
                group=VariableGroup.YOUTUBE.value,
                icon="🔍",
                tooltip="Search keywords",
                sort_order=9,
                max_value=500,
                example="science for kids, experiments",
            ),
            VariableDefinition(
                name="playlist_name",
                display_name="Playlist",
                type=VariableType.TEXT.value,
                default_value="Science Adventures",
                required=False,
                placeholder="Enter playlist name",
                description="Playlist to add video to",
                group=VariableGroup.YOUTUBE.value,
                icon="📋",
                tooltip="Playlist name",
                sort_order=10,
                example="Fun Math Games",
            ),
            
            # ============================================================
            # SOCIAL MEDIA GROUP (8 variables)
            # ============================================================
            VariableDefinition(
                name="platform",
                display_name="Platform",
                type=VariableType.DROPDOWN.value,
                default_value="instagram",
                options=["instagram", "tiktok", "youtube_shorts", "facebook", "twitter", "pinterest", "linkedin"],
                required=False,
                placeholder="Select platform",
                description="Social media platform",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="📱",
                tooltip="Where to post",
                sort_order=1,
                example="tiktok",
            ),
            VariableDefinition(
                name="content_type",
                display_name="Content Type",
                type=VariableType.DROPDOWN.value,
                default_value="reel",
                options=["reel", "story", "post", "carousel", "live", "igtv"],
                required=False,
                placeholder="Select type",
                description="Type of social content",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="📸",
                tooltip="Content format",
                sort_order=2,
                example="carousel",
            ),
            VariableDefinition(
                name="hashtags",
                display_name="Hashtags",
                type=VariableType.TEXT.value,
                default_value="#kids #education #fun #learning",
                required=False,
                placeholder="Enter hashtags",
                description="Discovery hashtags",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="🏷️",
                tooltip="Tags for reach",
                sort_order=3,
                max_value=2200,
                example="#scienceforkids #STEM",
            ),
            VariableDefinition(
                name="caption",
                display_name="Caption",
                type=VariableType.TEXTAREA.value,
                default_value="Learning is an adventure! 🌟",
                required=False,
                placeholder="Write caption",
                description="Post caption text",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="✍️",
                tooltip="Post text",
                sort_order=4,
                max_value=2200,
                example="Did you know? 🤔",
            ),
            VariableDefinition(
                name="post_time",
                display_name="Best Post Time",
                type=VariableType.TIME.value,
                default_value="10:00",
                required=False,
                placeholder="HH:MM",
                description="Optimal posting time",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="⏰",
                tooltip="When to post",
                sort_order=5,
                example="19:00",
            ),
            VariableDefinition(
                name="engagement_goal",
                display_name="Engagement Goal",
                type=VariableType.DROPDOWN.value,
                default_value="comments",
                options=["likes", "comments", "shares", "saves", "follows", "clicks"],
                required=False,
                placeholder="Select goal",
                description="Primary engagement metric",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="🎯",
                tooltip="What to optimize for",
                sort_order=6,
                example="shares",
            ),
            VariableDefinition(
                name="brand_voice",
                display_name="Brand Voice",
                type=VariableType.DROPDOWN.value,
                default_value="friendly",
                options=["friendly", "professional", "playful", "inspiring", "educational", "authentic"],
                required=False,
                placeholder="Select voice",
                description="Brand personality tone",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="🗣️",
                tooltip="How brand sounds",
                sort_order=7,
                example="inspiring",
            ),
            VariableDefinition(
                name="content_pillar",
                display_name="Content Pillar",
                type=VariableType.DROPDOWN.value,
                default_value="education",
                options=["education", "entertainment", "inspiration", "behind_scenes", "user_generated", "promotional"],
                required=False,
                placeholder="Select pillar",
                description="Content strategy pillar",
                group=VariableGroup.SOCIAL_MEDIA.value,
                icon="🏛️",
                tooltip="Content category",
                sort_order=8,
                example="entertainment",
            ),
            
            # ============================================================
            # PRODUCTIVITY GROUP (8 variables)
            # ============================================================
            VariableDefinition(
                name="task_name",
                display_name="Task Name",
                type=VariableType.TEXT.value,
                default_value="Create lesson plan",
                required=True,
                placeholder="Enter task",
                description="Task or todo item",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="✅",
                tooltip="What to do",
                sort_order=1,
                example="Grade assignments",
            ),
            VariableDefinition(
                name="priority",
                display_name="Priority",
                type=VariableType.DROPDOWN.value,
                default_value="medium",
                options=["low", "medium", "high", "urgent"],
                required=False,
                placeholder="Select priority",
                description="Task importance level",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="🔴",
                tooltip="Urgency level",
                sort_order=2,
                example="high",
            ),
            VariableDefinition(
                name="due_date",
                display_name="Due Date",
                type=VariableType.DATE.value,
                default_value="",
                required=False,
                placeholder="YYYY-MM-DD",
                description="Task deadline",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="📅",
                tooltip="When it's due",
                sort_order=3,
                example="2024-12-31",
            ),
            VariableDefinition(
                name="estimated_time",
                display_name="Estimated Time",
                type=VariableType.NUMBER.value,
                default_value="30",
                required=False,
                placeholder="Minutes",
                description="Expected duration in minutes",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="⏱️",
                tooltip="Time needed",
                sort_order=4,
                min_value=5,
                max_value=480,
                example="60",
                unit="minutes",
            ),
            VariableDefinition(
                name="project",
                display_name="Project",
                type=VariableType.TEXT.value,
                default_value="AI Kids Studio",
                required=False,
                placeholder="Project name",
                description="Associated project",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="📁",
                tooltip="Project folder",
                sort_order=5,
                example="Content Creation",
            ),
            VariableDefinition(
                name="tags",
                display_name="Tags",
                type=VariableType.TEXT.value,
                default_value="content, planning",
                required=False,
                placeholder="Comma-separated tags",
                description="Organizational tags",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="🏷️",
                tooltip="Filter tags",
                sort_order=6,
                example="video, urgent",
            ),
            VariableDefinition(
                name="status",
                display_name="Status",
                type=VariableType.DROPDOWN.value,
                default_value="todo",
                options=["todo", "in_progress", "review", "done", "blocked"],
                required=False,
                placeholder="Select status",
                description="Current task state",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="📊",
                tooltip="Progress state",
                sort_order=7,
                example="in_progress",
            ),
            VariableDefinition(
                name="notes",
                display_name="Notes",
                type=VariableType.TEXTAREA.value,
                default_value="",
                required=False,
                placeholder="Additional notes",
                description="Task details and context",
                group=VariableGroup.PRODUCTIVITY.value,
                icon="📝",
                tooltip="Extra info",
                sort_order=8,
                max_value=2000,
                example="Need to review new curriculum standards",
            ),
            
            # ============================================================
            # AI ASSISTANT GROUP (8 variables)
            # ============================================================
            VariableDefinition(
                name="ai_model",
                display_name="AI Model",
                type=VariableType.DROPDOWN.value,
                default_value="gpt-4",
                options=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet", "gemini-pro", "local-llama"],
                required=False,
                placeholder="Select model",
                description="AI model to use",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="🤖",
                tooltip="Which AI to use",
                sort_order=1,
                example="claude-3-sonnet",
            ),
            VariableDefinition(
                name="temperature",
                display_name="Temperature",
                type=VariableType.SLIDER.value,
                default_value="0.7",
                required=False,
                placeholder="0.0 - 2.0",
                description="Creativity vs consistency",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="🌡️",
                tooltip="Randomness level",
                sort_order=2,
                min_value=0.0,
                max_value=2.0,
                example="0.9",
            ),
            VariableDefinition(
                name="max_tokens",
                display_name="Max Tokens",
                type=VariableType.NUMBER.value,
                default_value="2000",
                required=False,
                placeholder="Token limit",
                description="Maximum response length",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="📏",
                tooltip="Response length limit",
                sort_order=3,
                min_value=100,
                max_value=8000,
                example="4000",
                unit="tokens",
            ),
            VariableDefinition(
                name="system_prompt",
                display_name="System Prompt",
                type=VariableType.TEXTAREA.value,
                default_value="You are a helpful AI assistant for creating children's educational content.",
                required=False,
                placeholder="Enter system prompt",
                description="AI behavior instructions",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="🎭",
                tooltip="AI personality",
                sort_order=4,
                max_value=4000,
                example="You are a friendly teacher for kids aged 5-8.",
            ),
            VariableDefinition(
                name="top_p",
                display_name="Top P",
                type=VariableType.SLIDER.value,
                default_value="1.0",
                required=False,
                placeholder="0.0 - 1.0",
                description="Nucleus sampling parameter",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="🎯",
                tooltip="Diversity control",
                sort_order=5,
                min_value=0.0,
                max_value=1.0,
                example="0.9",
            ),
            VariableDefinition(
                name="frequency_penalty",
                display_name="Frequency Penalty",
                type=VariableType.SLIDER.value,
                default_value="0.0",
                required=False,
                placeholder="-2.0 to 2.0",
                description="Reduce repetition",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="🔄",
                tooltip="Repetition penalty",
                sort_order=6,
                min_value=-2.0,
                max_value=2.0,
                example="0.5",
            ),
            VariableDefinition(
                name="presence_penalty",
                display_name="Presence Penalty",
                type=VariableType.SLIDER.value,
                default_value="0.0",
                required=False,
                placeholder="-2.0 to 2.0",
                description="Encourage new topics",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="💡",
                tooltip="Topic diversity",
                sort_order=7,
                min_value=-2.0,
                max_value=2.0,
                example="0.3",
            ),
            VariableDefinition(
                name="response_format",
                display_name="Response Format",
                type=VariableType.DROPDOWN.value,
                default_value="text",
                options=["text", "json", "markdown", "yaml"],
                required=False,
                placeholder="Select format",
                description="Output format structure",
                group=VariableGroup.AI_ASSISTANT.value,
                icon="📄",
                tooltip="Response structure",
                sort_order=8,
                example="json",
            ),
            
            # ============================================================
            # CUSTOM GROUP (5 variables for user-defined)
            # ============================================================
            VariableDefinition(
                name="custom_1",
                display_name="Custom Field 1",
                type=VariableType.TEXT.value,
                default_value="",
                required=False,
                placeholder="Your custom value",
                description="User-defined custom variable",
                group=VariableGroup.CUSTOM.value,
                icon="⚙️",
                tooltip="Custom field",
                sort_order=1,
                advanced=True,
            ),
            VariableDefinition(
                name="custom_2",
                display_name="Custom Field 2",
                type=VariableType.TEXT.value,
                default_value="",
                required=False,
                placeholder="Your custom value",
                description="User-defined custom variable",
                group=VariableGroup.CUSTOM.value,
                icon="⚙️",
                tooltip="Custom field",
                sort_order=2,
                advanced=True,
            ),
            VariableDefinition(
                name="custom_3",
                display_name="Custom Field 3",
                type=VariableType.TEXTAREA.value,
                default_value="",
                required=False,
                placeholder="Your custom text",
                description="User-defined custom variable",
                group=VariableGroup.CUSTOM.value,
                icon="⚙️",
                tooltip="Custom field",
                sort_order=3,
                advanced=True,
            ),
            VariableDefinition(
                name="custom_4",
                display_name="Custom Field 4",
                type=VariableType.DROPDOWN.value,
                default_value="",
                options=[],
                required=False,
                placeholder="Select option",
                description="User-defined custom variable",
                group=VariableGroup.CUSTOM.value,
                icon="⚙️",
                tooltip="Custom field",
                sort_order=4,
                advanced=True,
                allow_custom=True,
            ),
            VariableDefinition(
                name="custom_5",
                display_name="Custom Field 5",
                type=VariableType.NUMBER.value,
                default_value="0",
                required=False,
                placeholder="Enter number",
                description="User-defined custom variable",
                group=VariableGroup.CUSTOM.value,
                icon="⚙️",
                tooltip="Custom field",
                sort_order=5,
                advanced=True,
            ),
        ]

    # ============================================================
    # BACKWARD COMPATIBLE PUBLIC API
    # ============================================================
    
    def register(self, variable: VariableDefinition) -> None:
        """Register a variable definition.
        
        Args:
            variable: VariableDefinition to register
        """
        self._variables[variable.name] = variable
        if variable.group not in self._groups:
            self._groups[variable.group] = []
        if variable.name not in self._groups[variable.group]:
            self._groups[variable.group].append(variable.name)
        logger.debug(f"Registered variable: {variable.name} in group {variable.group}")
    
    def unregister(self, name: str) -> None:
        """Remove a variable definition.
        
        Args:
            name: Variable identifier to remove
        """
        if name in self._variables:
            var = self._variables.pop(name)
            if var.group in self._groups and name in self._groups[var.group]:
                self._groups[var.group].remove(name)
            logger.debug(f"Unregistered variable: {name}")
    
    def exists(self, name: str) -> bool:
        """Check if a variable exists.
        
        Args:
            name: Variable identifier
            
        Returns:
            True if variable exists
        """
        return name in self._variables
    
    def get(self, name: str) -> Optional[VariableDefinition]:
        """Get a variable definition by name.
        
        Args:
            name: Variable identifier
            
        Returns:
            VariableDefinition or None if not found
        """
        return self._variables.get(name)
    
    def get_all(self) -> List[VariableDefinition]:
        """Get all registered variable definitions.
        
        Returns:
            List of all VariableDefinition objects
        """
        return list(self._variables.values())
    
    # ============================================================
    # ENHANCED API
    # ============================================================
    
    def get_by_group(self, group: str) -> List[VariableDefinition]:
        """Get all variables in a group.
        
        Args:
            group: Group name (VariableGroup value)
            
        Returns:
            List of variables in the group, sorted by sort_order
        """
        var_names = self._groups.get(group, [])
        variables = [self._variables[name] for name in var_names if name in self._variables]
        return sorted(variables, key=lambda v: v.sort_order)
    
    def get_groups(self) -> List[str]:
        """Get all group names that have variables.
        
        Returns:
            List of group names
        """
        return [g for g, vars in self._groups.items() if vars]
    
    def get_group_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all groups.
        
        Returns:
            Dict with group metadata
        """
        return {
            group: {
                "label": group,
                "count": len(vars),
                "variables": vars,
            }
            for group, vars in self._groups.items()
            if vars
        }
    
    def search(self, query: str, group: Optional[str] = None) -> List[VariableDefinition]:
        """Search variables by name, display_name, or description.
        
        Args:
            query: Search query
            group: Optional group to limit search
            
        Returns:
            Matching variables
        """
        query = query.lower()
        results = []
        
        vars_to_search = self.get_by_group(group) if group else self.get_all()
        
        for var in vars_to_search:
            if (query in var.name.lower() or 
                query in var.display_name.lower() or 
                query in var.description.lower() or
                (var.placeholder and query in var.placeholder.lower())):
                results.append(var)
        
        return results
    
    def get_required(self) -> List[VariableDefinition]:
        """Get all required variables.
        
        Returns:
            List of required variables
        """
        return [v for v in self._variables.values() if v.required]
    
    def get_advanced(self) -> List[VariableDefinition]:
        """Get all advanced variables.
        
        Returns:
            List of advanced variables
        """
        return [v for v in self._variables.values() if v.advanced]
    
    def validate_all(self, values: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate multiple values against their variable definitions.
        
        Args:
            values: Dict of variable_name -> value
            
        Returns:
            Dict of variable_name -> list of error messages (empty if valid)
        """
        errors = {}
        for name, value in values.items():
            var = self.get(name)
            if var:
                var_errors = var.validate(value)
                if var_errors:
                    errors[name] = var_errors
            elif self.exists(name):
                # Variable exists but not in values - check if required
                var = self.get(name)
                if var and var.required:
                    errors[name] = [f"{var.display_name} is required"]
        return errors
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get default values for all variables.
        
        Returns:
            Dict of variable_name -> default_value
        """
        return {
            name: var.default_value 
            for name, var in self._variables.items() 
            if var.default_value is not None
        }
    
    def get_dropdown_data(self, name: str) -> List[Dict[str, str]]:
        """Get dropdown options for a variable.
        
        Args:
            name: Variable name
            
        Returns:
            List of option dicts with value, label, description, icon
        """
        var = self.get(name)
        if not var:
            return []
        return var.get_dropdown_options()
    
    def export_schema(self) -> Dict[str, Any]:
        """Export complete registry schema for persistence/UI generation.
        
        Returns:
            Complete schema dictionary
        """
        return {
            "variables": [var.to_dict() for var in self.get_all()],
            "groups": self.get_group_info(),
        }
    
    def import_schema(self, schema: Dict[str, Any]) -> int:
        """Import variables from schema.
        
        Args:
            schema: Schema dictionary from export_schema
            
        Returns:
            Number of variables imported
        """
        count = 0
        for var_data in schema.get("variables", []):
            try:
                var = VariableDefinition.from_dict(var_data)
                self.register(var)
                count += 1
            except Exception as e:
                logger.error(f"Failed to import variable {var_data.get('name')}: {e}")
        return count
    
    def clear(self) -> None:
        """Clear all variables (use with caution)."""
        self._variables.clear()
        for group in self._groups:
            self._groups[group].clear()
        logger.warning("Variable registry cleared")
    
    def __len__(self) -> int:
        """Return number of registered variables."""
        return len(self._variables)
    
    def __contains__(self, name: str) -> bool:
        """Check if variable exists (supports 'in' operator)."""
        return self.exists(name)
    
    def __iter__(self):
        """Iterate over variable definitions."""
        return iter(self._variables.values())
    
    def __getitem__(self, name: str) -> VariableDefinition:
        """Get variable by name (supports bracket notation)."""
        var = self.get(name)
        if var is None:
            raise KeyError(f"Variable not found: {name}")
        return var


# Global registry instance
_default_registry: Optional[VariableRegistry] = None


def get_variable_registry() -> VariableRegistry:
    """Get the default global variable registry.
    
    Returns:
        Global VariableRegistry instance
    """
    global _default_registry
    if _default_registry is None:
        _default_registry = VariableRegistry()
    return _default_registry


def reset_variable_registry() -> VariableRegistry:
    """Reset and return a new global registry.
    
    Returns:
        New VariableRegistry instance
    """
    global _default_registry
    _default_registry = VariableRegistry()
    return _default_registry