"""Tests for the Senior-stage rule engine."""

from collections.abc import Iterator

from fizzbuzz_evolution.senior import DivisibilityRule, Rule, RuleEngine


def test_engine_returns_number_when_no_rule_matches() -> None:
    engine = RuleEngine([DivisibilityRule(3, "Fizz")])

    assert engine.evaluate(2) == "2"


def test_engine_composes_all_matching_rules() -> None:
    engine = RuleEngine(
        [
            DivisibilityRule(3, "Fizz"),
            DivisibilityRule(5, "Buzz"),
        ]
    )

    assert engine.evaluate(3) == "Fizz"
    assert engine.evaluate(5) == "Buzz"
    assert engine.evaluate(15) == "FizzBuzz"


def test_engine_preserves_registration_order() -> None:
    engine = RuleEngine(
        [
            DivisibilityRule(5, "Buzz"),
            DivisibilityRule(3, "Fizz"),
        ]
    )

    assert engine.evaluate(15) == "BuzzFizz"


def test_empty_engine_returns_original_number() -> None:
    assert RuleEngine([]).evaluate(15) == "15"


def test_engine_materializes_input_iterable() -> None:
    def rules() -> Iterator[Rule]:
        yield DivisibilityRule(3, "Fizz")
        yield DivisibilityRule(5, "Buzz")

    engine = RuleEngine(rules())

    assert engine.evaluate(15) == "FizzBuzz"
    assert engine.evaluate(15) == "FizzBuzz"


def test_engine_is_not_affected_by_source_list_changes() -> None:
    rules: list[Rule] = [DivisibilityRule(3, "Fizz")]
    engine = RuleEngine(rules)

    rules.append(DivisibilityRule(5, "Buzz"))

    assert engine.evaluate(5) == "5"
    assert engine.rules == (DivisibilityRule(3, "Fizz"),)
