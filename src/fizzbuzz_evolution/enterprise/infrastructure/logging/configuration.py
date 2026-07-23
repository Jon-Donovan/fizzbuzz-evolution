"""Central logging configuration for the Enterprise CLI."""

import logging
from typing import TextIO

from ..config import LogLevel


def configure_logging(level: LogLevel, stream: TextIO) -> None:
    """Configure deterministic application logging on the supplied stream."""
    logging.basicConfig(
        level=level.value,
        format="%(levelname)s %(name)s %(message)s",
        stream=stream,
        force=True,
    )
