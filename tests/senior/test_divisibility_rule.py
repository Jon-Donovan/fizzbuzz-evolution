"""Tests for divisibility rules."""

from dataclasses import FrozenInstanceError

import pytest

from fizzbuzz_evolution.senior import (
    DivisibilityRule,
    InvalidDivisorError,
    InvalidReplacementError,
)


def test_rule_matches_positive_zero_and_negative_multiples() -> None:
    rule = DivisibilityRule(3, "Fizz")

    assert rule.matches(3)
    assert rule.matches(0)
    assert rule.matches(-3)
    assert not rule.matches(4)


def test_rule_supports_negative_divisor() -> None:
    rule = DivisibilityRule(-3, "Fizz")

    assert rule.matches(6)
    assert rule.matches(-6)


def test_rule_renders_configured_replacement() -> None:
    rule = DivisibilityRule(3, "Fizz")

    assert rule.render(3) == "Fizz"


def test_rule_rejects_zero_divisor() -> None:
    with pytest.raises(InvalidDivisorError) as error_info:
        DivisibilityRule(0, "Zero")

    assert error_info.value.divisor == 0
    assert str(error_info.value) == "rule divisor must not be zero"


@pytest.mark.parametrize("replacement", ["", " ", "\t\n"])
def test_rule_rejects_empty_replacement(replacement: str) -> None:
    with pytest.raises(InvalidReplacementError) as error_info:
        DivisibilityRule(3, replacement)

    assert error_info.value.replacement == replacement
    assert str(error_info.value) == "rule replacement must not be empty or whitespace"


def test_rule_is_immutable() -> None:
    rule = DivisibilityRule(3, "Fizz")

    with pytest.raises(FrozenInstanceError):
        rule.divisor = 5  # type: ignore[misc]
