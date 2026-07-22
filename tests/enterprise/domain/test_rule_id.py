"""Tests for Enterprise rule identifiers."""

import pytest

from fizzbuzz_evolution.enterprise import InvalidRuleIdError, RuleId


def test_rule_id_preserves_valid_value() -> None:
    assert RuleId("fizz").value == "fizz"


@pytest.mark.parametrize("value", ["", " ", "\t"])
def test_rule_id_rejects_empty_values(value: str) -> None:
    with pytest.raises(InvalidRuleIdError) as error:
        RuleId(value)

    assert error.value.value == value
