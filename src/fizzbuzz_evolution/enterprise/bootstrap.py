"""Composition helpers for the Enterprise stage."""

from dataclasses import dataclass

from .application import GenerateSequenceUseCase
from .domain import Rule
from .presets import CLASSIC_RULES


@dataclass(frozen=True, slots=True)
class StaticRuleProvider:
    """Provide an immutable collection of rules for local composition."""

    rules: tuple[Rule, ...]

    def get_rules(self) -> tuple[Rule, ...]:
        """Return the configured rules."""
        return self.rules


def create_fizzbuzz_use_case() -> GenerateSequenceUseCase:
    """Create a sequence use case configured with classic FizzBuzz rules."""
    return GenerateSequenceUseCase(StaticRuleProvider(CLASSIC_RULES))
