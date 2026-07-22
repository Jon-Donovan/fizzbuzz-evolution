"""Extensible and configurable Senior-stage FizzBuzz implementation."""

from .engine import RuleEngine
from .errors import (
    FizzBuzzError,
    InvalidDivisorError,
    InvalidRangeError,
    InvalidReplacementError,
)
from .generator import generate
from .presets import CLASSIC_RULES, create_fizzbuzz_engine
from .rules import DivisibilityRule, Rule

__all__ = [
    "CLASSIC_RULES",
    "DivisibilityRule",
    "FizzBuzzError",
    "InvalidDivisorError",
    "InvalidRangeError",
    "InvalidReplacementError",
    "Rule",
    "RuleEngine",
    "create_fizzbuzz_engine",
    "generate",
]
