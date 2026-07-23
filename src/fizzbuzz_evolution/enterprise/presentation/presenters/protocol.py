"""Presentation contract for Enterprise sequence results."""

from typing import Protocol

from ...application import GenerateSequenceResult


class ResultPresenter(Protocol):
    """Render an application result without performing output side effects."""

    def present(self, result: GenerateSequenceResult) -> str:
        """Render the supplied result."""
        ...
