"""Presenter selection for configured output formats."""

from ...infrastructure.config import OutputFormat
from .json_presenter import JsonPresenter
from .protocol import ResultPresenter
from .text_presenter import TextPresenter


def create_presenter(output_format: OutputFormat) -> ResultPresenter:
    """Create the presenter associated with an output format."""
    if output_format is OutputFormat.JSON:
        return JsonPresenter()
    return TextPresenter()
