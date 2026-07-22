"""Enterprise domain and application implementation."""

from .application import (
    GenerateSequenceCommand,
    GenerateSequenceResult,
    GenerateSequenceUseCase,
    RuleProvider,
)
from .bootstrap import StaticRuleProvider, create_fizzbuzz_use_case
from .domain import (
    DivisibilityRule,
    DomainError,
    Evaluation,
    EvaluationService,
    InvalidDivisorError,
    InvalidRangeError,
    InvalidReplacementError,
    InvalidRuleIdError,
    Number,
    NumberRange,
    Rule,
    RuleId,
    RuleOutput,
)
from .presets import CLASSIC_RULES

__all__ = [
    "CLASSIC_RULES",
    "DivisibilityRule",
    "DomainError",
    "Evaluation",
    "EvaluationService",
    "GenerateSequenceCommand",
    "GenerateSequenceResult",
    "GenerateSequenceUseCase",
    "InvalidDivisorError",
    "InvalidRangeError",
    "InvalidReplacementError",
    "InvalidRuleIdError",
    "Number",
    "NumberRange",
    "Rule",
    "RuleId",
    "RuleOutput",
    "RuleProvider",
    "StaticRuleProvider",
    "create_fizzbuzz_use_case",
]
