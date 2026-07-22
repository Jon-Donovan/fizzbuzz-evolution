"""Tests for ready-to-use Senior-stage presets."""

from fizzbuzz_evolution.senior import (
    CLASSIC_RULES,
    DivisibilityRule,
    RuleEngine,
    create_fizzbuzz_engine,
)


def test_classic_preset_reproduces_fizzbuzz_behavior() -> None:
    engine = create_fizzbuzz_engine()

    assert engine.evaluate(1) == "1"
    assert engine.evaluate(3) == "Fizz"
    assert engine.evaluate(5) == "Buzz"
    assert engine.evaluate(15) == "FizzBuzz"


def test_classic_rules_can_be_extended_without_changing_engine() -> None:
    engine = RuleEngine((*CLASSIC_RULES, DivisibilityRule(7, "Bazz")))

    assert engine.evaluate(7) == "Bazz"
    assert engine.evaluate(21) == "FizzBazz"
    assert engine.evaluate(35) == "BuzzBazz"
    assert engine.evaluate(105) == "FizzBuzzBazz"
