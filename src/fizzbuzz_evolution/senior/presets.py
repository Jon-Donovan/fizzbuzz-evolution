"""Ready-to-use Senior-stage rule presets."""

from .engine import RuleEngine
from .rules import DivisibilityRule, Rule

CLASSIC_RULES: tuple[Rule, ...] = (
    DivisibilityRule(3, "Fizz"),
    DivisibilityRule(5, "Buzz"),
)


def create_fizzbuzz_engine() -> RuleEngine:
    """Create an engine configured with the classic FizzBuzz rules."""
    return RuleEngine(CLASSIC_RULES)
