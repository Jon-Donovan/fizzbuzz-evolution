"""Tests for configured Enterprise rule providers."""

from fizzbuzz_evolution.enterprise import Number
from fizzbuzz_evolution.enterprise.infrastructure.config import DivisibilityRuleConfig
from fizzbuzz_evolution.enterprise.infrastructure.rules import ConfiguredRuleProvider


def test_builds_domain_rules_in_configuration_order() -> None:
    provider = ConfiguredRuleProvider.from_configs(
        (
            DivisibilityRuleConfig("buzz", 5, "Buzz"),
            DivisibilityRuleConfig("fizz", 3, "Fizz"),
        )
    )

    rules = provider.get_rules()

    assert [rule.rule_id.value for rule in rules] == ["buzz", "fizz"]
    assert [rule.apply(Number(15)).value for rule in rules] == ["Buzz", "Fizz"]
