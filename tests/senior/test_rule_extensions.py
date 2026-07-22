"""Tests proving that custom rules can extend the engine structurally."""

from dataclasses import dataclass
from math import isqrt

from fizzbuzz_evolution.senior import DivisibilityRule, RuleEngine


@dataclass(frozen=True)
class ExactMatchRule:
    """Match one exact value without inheriting from a library class."""

    expected: int
    replacement: str

    def matches(self, number: int) -> bool:
        return number == self.expected

    def render(self, number: int) -> str:
        return self.replacement


class SquareRule:
    """Render a dynamic result for non-negative perfect squares."""

    def matches(self, number: int) -> bool:
        return number >= 0 and isqrt(number) ** 2 == number

    def render(self, number: int) -> str:
        return f"Square({number})"


def test_engine_accepts_custom_structural_rule() -> None:
    engine = RuleEngine([DivisibilityRule(3, "Fizz"), ExactMatchRule(10, "Ten")])

    assert engine.evaluate(3) == "Fizz"
    assert engine.evaluate(10) == "Ten"


def test_rule_output_can_depend_on_evaluated_number() -> None:
    engine = RuleEngine([SquareRule()])

    assert engine.evaluate(9) == "Square(9)"
    assert engine.evaluate(8) == "8"
