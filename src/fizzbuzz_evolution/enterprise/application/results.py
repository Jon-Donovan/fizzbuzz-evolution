"""Structured application results for Enterprise use cases."""

from dataclasses import dataclass

from ..domain import Evaluation


@dataclass(frozen=True, slots=True)
class GenerateSequenceResult:
    """Structured result returned by sequence generation."""

    start: int
    end: int
    items: tuple[Evaluation, ...]
