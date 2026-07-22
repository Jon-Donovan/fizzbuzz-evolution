"""Extensible rule engine for evaluating individual numbers."""

from collections.abc import Iterable

from .rules import Rule


class RuleEngine:
    """Evaluate numbers by composing all matching rules in registration order."""

    def __init__(self, rules: Iterable[Rule]) -> None:
        self._rules = tuple(rules)

    @property
    def rules(self) -> tuple[Rule, ...]:
        """Return the immutable sequence of registered rules."""
        return self._rules

    def evaluate(self, number: int) -> str:
        """Return concatenated rule output or the original number when no rule matches."""
        result = "".join(rule.render(number) for rule in self._rules if rule.matches(number))
        return result or str(number)
