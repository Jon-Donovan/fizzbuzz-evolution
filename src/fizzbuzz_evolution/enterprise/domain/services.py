"""Domain services for evaluating numbers against ordered rules."""

from collections.abc import Iterable

from .models import Evaluation, Number
from .rules import Rule


class EvaluationService:
    """Evaluate numbers with an immutable, ordered collection of rules."""

    def __init__(self, rules: Iterable[Rule]) -> None:
        self._rules = tuple(rules)

    def evaluate(self, number: Number) -> Evaluation:
        """Return a structured evaluation for one number."""
        matches = tuple(rule.apply(number) for rule in self._rules if rule.matches(number))
        value = "".join(match.value for match in matches) or str(number.value)
        return Evaluation(number=number, value=value, matches=matches)
