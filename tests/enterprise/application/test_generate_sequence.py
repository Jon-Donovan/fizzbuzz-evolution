"""Tests for the Enterprise sequence generation use case."""

from dataclasses import dataclass

import pytest

from fizzbuzz_evolution.enterprise import (
    CLASSIC_RULES,
    GenerateSequenceCommand,
    GenerateSequenceUseCase,
    InvalidRangeError,
    Rule,
    StaticRuleProvider,
    create_fizzbuzz_use_case,
)


@dataclass
class StubRuleProvider:
    rules: tuple[Rule, ...]
    calls: int = 0

    def get_rules(self) -> tuple[Rule, ...]:
        self.calls += 1
        return self.rules


def test_use_case_returns_structured_sequence() -> None:
    result = create_fizzbuzz_use_case().execute(GenerateSequenceCommand(1, 5))

    assert result.start == 1
    assert result.end == 5
    assert tuple(item.value for item in result.items) == ("1", "2", "Fizz", "4", "Buzz")
    assert result.items[2].matches[0].rule_id.value == "fizz"


def test_use_case_supports_negative_range() -> None:
    result = create_fizzbuzz_use_case().execute(GenerateSequenceCommand(-1, 1))

    assert tuple(item.value for item in result.items) == ("-1", "FizzBuzz", "1")


def test_use_case_supports_empty_rules() -> None:
    use_case = GenerateSequenceUseCase(StaticRuleProvider(()))

    result = use_case.execute(GenerateSequenceCommand(3, 5))

    assert tuple(item.value for item in result.items) == ("3", "4", "5")


def test_use_case_requests_rules_once_per_execution() -> None:
    provider = StubRuleProvider(CLASSIC_RULES)
    use_case = GenerateSequenceUseCase(provider)

    use_case.execute(GenerateSequenceCommand(1, 15))

    assert provider.calls == 1


def test_use_case_rejects_reversed_range_before_requesting_rules() -> None:
    provider = StubRuleProvider(CLASSIC_RULES)
    use_case = GenerateSequenceUseCase(provider)

    with pytest.raises(InvalidRangeError):
        use_case.execute(GenerateSequenceCommand(5, 1))

    assert provider.calls == 0
