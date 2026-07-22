"""Application-specific exceptions for the Senior stage."""


class FizzBuzzError(Exception):
    """Base exception for expected Senior-stage failures."""


class InvalidRangeError(FizzBuzzError):
    """Raised when the start of a range is greater than its end."""

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end
        super().__init__(f"range start ({start}) must not be greater than range end ({end})")


class InvalidDivisorError(FizzBuzzError):
    """Raised when a divisibility rule uses zero as its divisor."""

    def __init__(self, divisor: int) -> None:
        self.divisor = divisor
        super().__init__("rule divisor must not be zero")


class InvalidReplacementError(FizzBuzzError):
    """Raised when a rule replacement is empty or contains only whitespace."""

    def __init__(self, replacement: str) -> None:
        self.replacement = replacement
        super().__init__("rule replacement must not be empty or whitespace")
