"""Generate inclusive sequences using a configured rule engine."""

from .engine import RuleEngine
from .errors import InvalidRangeError


def generate(engine: RuleEngine, start: int = 1, end: int = 100) -> list[str]:
    """Return evaluated values for the inclusive range from start through end."""
    if start > end:
        raise InvalidRangeError(start, end)

    return [engine.evaluate(number) for number in range(start, end + 1)]
