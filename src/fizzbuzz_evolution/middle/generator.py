"""Generate inclusive FizzBuzz sequences."""

from .errors import InvalidRangeError
from .evaluator import evaluate


def generate(start: int = 1, end: int = 100) -> list[str]:
    """Return FizzBuzz values for the inclusive range from start through end."""
    if start > end:
        raise InvalidRangeError(start, end)

    return [evaluate(number) for number in range(start, end + 1)]
