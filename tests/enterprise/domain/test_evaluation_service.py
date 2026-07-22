"""Tests for Enterprise domain evaluation."""

from dataclasses import dataclass

from fizzbuzz_evolution.enterprise import (
    DivisibilityRule,
    Evaluation,
    EvaluationService,
    Number,
    RuleId,
    RuleOutput,
)


def classic_rules() -> list[DivisibilityRule]:
    return [
        DivisibilityRule(RuleId("fizz"), 3, "Fizz"),
        DivisibilityRule(RuleId("buzz"), 5, "Buzz"),
    ]


def test_evaluation_returns_original_number_without_matches() -> None:
    assert EvaluationService(classic_rules()).evaluate(Number(2)) == Evaluation(
        number=Number(2),
        value="2",
        matches=(),
    )


def test_evaluation_preserves_all_matching_rule_outputs() -> None:
    assert EvaluationService(classic_rules()).evaluate(Number(15)) == Evaluation(
        number=Number(15),
        value="FizzBuzz",
        matches=(
            RuleOutput(RuleId("fizz"), "Fizz"),
            RuleOutput(RuleId("buzz"), "Buzz"),
        ),
    )


def test_evaluation_preserves_registration_order() -> None:
    rules = reversed(classic_rules())

    assert EvaluationService(rules).evaluate(Number(15)).value == "BuzzFizz"


def test_evaluation_accepts_empty_rule_collection() -> None:
    assert EvaluationService([]).evaluate(Number(15)).value == "15"


def test_evaluation_materializes_input_rules() -> None:
    rules = classic_rules()
    service = EvaluationService(rules)
    rules.append(DivisibilityRule(RuleId("bazz"), 7, "Bazz"))

    assert service.evaluate(Number(7)).value == "7"


def test_evaluation_supports_structural_custom_rules() -> None:
    @dataclass(frozen=True)
    class ExactMatchRule:
        rule_id: RuleId
        expected: int

        def matches(self, number: Number) -> bool:
            return number.value == self.expected

        def apply(self, number: Number) -> RuleOutput:
            return RuleOutput(self.rule_id, f"Exact({number.value})")

    service = EvaluationService([ExactMatchRule(RuleId("exact-ten"), 10)])

    assert service.evaluate(Number(10)).value == "Exact(10)"
