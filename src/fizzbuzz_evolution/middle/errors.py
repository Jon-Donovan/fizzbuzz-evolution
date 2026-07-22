"""Application-specific exceptions for the Middle stage."""


class FizzBuzzError(Exception):
    """Base exception for expected Middle-stage failures."""


class InvalidRangeError(FizzBuzzError):
    """Raised when the start of a range is greater than its end."""

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end
        super().__init__(f"range start ({start}) must not be greater than range end ({end})")
