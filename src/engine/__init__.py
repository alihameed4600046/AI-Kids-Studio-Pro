"""AI Engine package for AI Kids Studio Pro.

This package provides the core AI engine abstractions and implementations
including prompt management, model management, and mock engines for testing.
"""

from src.engine.ai_engine import (
    AIEngine,
    AIEngineError,
    AuthenticationError,
    ContentFilterError,
    EngineConfig,
    EngineNotReadyError,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
    RetryStrategy,
)
from src.engine.mock_engine import MockEngine, MockModelManager, MockScenario
from src.engine.model_manager import (
    ModelManager,
    ProviderConfig,
    ProviderRegistry,
    ProviderType,
    QuotaUsage,
    TaskType,
)
from src.engine.prompt_engine import PromptEngine, PromptTemplateError

__all__ = [
    "AIEngine",
    "AIEngineError",
    "AuthenticationError",
    "ContentFilterError",
    "EngineConfig",
    "EngineNotReadyError",
    "EngineState",
    "GenerationRequest",
    "GenerationResponse",
    "MockEngine",
    "MockModelManager",
    "MockScenario",
    "ModelManager",
    "PromptEngine",
    "PromptTemplateError",
    "ProviderConfig",
    "ProviderRegistry",
    "ProviderType",
    "QuotaUsage",
    "RateLimitError",
    "RetryStrategy",
    "TaskType",
]
