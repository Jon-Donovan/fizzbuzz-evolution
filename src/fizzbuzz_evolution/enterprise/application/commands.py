"""Application commands for Enterprise use cases."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GenerateSequenceCommand:
    """Request generation of an inclusive FizzBuzz sequence."""

    start: int = 1
    end: int = 100
