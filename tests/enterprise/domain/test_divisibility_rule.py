"""Tests for the Enterprise divisibility rule."""

from dataclasses import FrozenInstanceError

import pytest

from fizzbuzz_evolution.enterprise import (
    DivisibilityRule,
    InvalidDivisorError,
    InvalidReplacementError,
    Number,
    RuleId,
    RuleOutput,
)


def test_divisibility_rule_matches_supported_numbers() -> None:
    rule = DivisibilityRule(RuleId("fizz"), 3, "Fizz")

    assert rule.matches(Number(3))
    assert rule.matches(Number(0))
    assert rule.matches(Number(-3))
    assert not rule.matches(Number(4))


def test_divisibility_rule_accepts_negative_divisor() -> None:
    assert DivisibilityRule(RuleId("fizz"), -3, "Fizz").matches(Number(6))


def test_divisibility_rule_returns_structured_output() -> None:
    rule = DivisibilityRule(RuleId("fizz"), 3, "Fizz")

    assert rule.apply(Number(3)) == RuleOutput(RuleId("fizz"), "Fizz")


def test_divisibility_rule_rejects_zero_divisor() -> None:
    with pytest.raises(InvalidDivisorError) as error:
        DivisibilityRule(RuleId("zero"), 0, "Zero")

    assert error.value.divisor == 0


@pytest.mark.parametrize("replacement", ["", " ", "\n"])
def test_divisibility_rule_rejects_empty_replacement(replacement: str) -> None:
    with pytest.raises(InvalidReplacementError) as error:
        DivisibilityRule(RuleId("invalid"), 3, replacement)

    assert error.value.replacement == replacement


def test_divisibility_rule_is_immutable() -> None:
    rule = DivisibilityRule(RuleId("fizz"), 3, "Fizz")

    with pytest.raises(FrozenInstanceError):
        rule.divisor = 5  # type: ignore[misc]
