"""Built-in Enterprise rule presets."""

from .domain import DivisibilityRule, Rule, RuleId

CLASSIC_RULES: tuple[Rule, ...] = (
    DivisibilityRule(RuleId("fizz"), 3, "Fizz"),
    DivisibilityRule(RuleId("buzz"), 5, "Buzz"),
)
