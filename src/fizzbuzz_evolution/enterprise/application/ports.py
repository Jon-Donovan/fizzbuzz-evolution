"""Application ports required by Enterprise use cases."""

from typing import Protocol

from ..domain import Rule


class RuleProvider(Protocol):
    """Provide the ordered rules used by the application."""

    def get_rules(self) -> tuple[Rule, ...]:
        """Return the current ordered collection of domain rules."""
        ...
