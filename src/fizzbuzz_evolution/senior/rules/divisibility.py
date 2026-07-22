"""Divisibility-based rule implementation."""

from dataclasses import dataclass

from ..errors import InvalidDivisorError, InvalidReplacementError


@dataclass(frozen=True, slots=True)
class DivisibilityRule:
    """Produce a replacement when a number is divisible by a configured divisor."""

    divisor: int
    replacement: str

    def __post_init__(self) -> None:
        """Validate the immutable rule configuration."""
        if self.divisor == 0:
            raise InvalidDivisorError(self.divisor)
        if not self.replacement.strip():
            raise InvalidReplacementError(self.replacement)

    def matches(self, number: int) -> bool:
        """Return whether the number is divisible by this rule's divisor."""
        return number % self.divisor == 0

    def render(self, number: int) -> str:
        """Return the configured replacement for a matching number."""
        return self.replacement
