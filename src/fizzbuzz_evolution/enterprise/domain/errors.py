"""Domain errors for the Enterprise stage."""


class DomainError(Exception):
    """Base class for expected domain failures."""


class InvalidRangeError(DomainError):
    """Raised when a number range has reversed bounds."""

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end
        super().__init__(f"Range start ({start}) must not be greater than end ({end}).")


class InvalidRuleIdError(DomainError):
    """Raised when a rule identifier is empty."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__("Rule identifier must not be empty or whitespace.")


class InvalidDivisorError(DomainError):
    """Raised when a divisibility rule uses zero as its divisor."""

    def __init__(self, divisor: int) -> None:
        self.divisor = divisor
        super().__init__("Rule divisor must not be zero.")


class InvalidReplacementError(DomainError):
    """Raised when a rule replacement has no visible content."""

    def __init__(self, replacement: str) -> None:
        self.replacement = replacement
        super().__init__("Rule replacement must not be empty or whitespace.")
