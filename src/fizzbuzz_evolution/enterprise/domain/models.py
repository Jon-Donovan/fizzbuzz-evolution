"""Immutable domain models for Enterprise FizzBuzz evaluation."""

from collections.abc import Iterator
from dataclasses import dataclass

from .errors import InvalidRangeError, InvalidRuleIdError


@dataclass(frozen=True, slots=True)
class Number:
    """A number evaluated by the domain."""

    value: int


@dataclass(frozen=True, slots=True)
class RuleId:
    """A stable identifier for a domain rule."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidRuleIdError(self.value)


@dataclass(frozen=True, slots=True)
class RuleOutput:
    """The output produced by one matching rule."""

    rule_id: RuleId
    value: str


@dataclass(frozen=True, slots=True)
class Evaluation:
    """A structured result for one evaluated number."""

    number: Number
    value: str
    matches: tuple[RuleOutput, ...]


@dataclass(frozen=True, slots=True)
class NumberRange:
    """An inclusive range of domain numbers."""

    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise InvalidRangeError(self.start, self.end)

    def __iter__(self) -> Iterator[Number]:
        for value in range(self.start, self.end + 1):
            yield Number(value)
