"""Rule contracts and domain rule implementations."""

from dataclasses import dataclass
from typing import Protocol

from .errors import InvalidDivisorError, InvalidReplacementError
from .models import Number, RuleId, RuleOutput


class Rule(Protocol):
    """Structural contract implemented by Enterprise domain rules."""

    @property
    def rule_id(self) -> RuleId:
        """Return the stable identifier of the rule."""
        ...

    def matches(self, number: Number) -> bool:
        """Return whether this rule applies to the number."""
        ...

    def apply(self, number: Number) -> RuleOutput:
        """Return the output produced for a matching number."""
        ...


@dataclass(frozen=True, slots=True)
class DivisibilityRule:
    """Produce a replacement when a number is divisible by a divisor."""

    rule_id: RuleId
    divisor: int
    replacement: str

    def __post_init__(self) -> None:
        if self.divisor == 0:
            raise InvalidDivisorError(self.divisor)
        if not self.replacement.strip():
            raise InvalidReplacementError(self.replacement)

    def matches(self, number: Number) -> bool:
        """Return whether the number is divisible by the configured divisor."""
        return number.value % self.divisor == 0

    def apply(self, number: Number) -> RuleOutput:
        """Return the rule output for a matching number."""
        return RuleOutput(rule_id=self.rule_id, value=self.replacement)
