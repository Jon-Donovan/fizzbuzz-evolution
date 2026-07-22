"""Structural contract for Senior-stage rules."""

from typing import Protocol


class Rule(Protocol):
    """Describe behavior required by the rule engine."""

    def matches(self, number: int) -> bool:
        """Return whether this rule matches the supplied number."""
        ...

    def render(self, number: int) -> str:
        """Return the text produced when this rule matches."""
        ...
