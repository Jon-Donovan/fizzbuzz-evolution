"""Configuration loader contracts."""

from pathlib import Path
from typing import Protocol

from .models import EnterpriseConfig


class ConfigLoader(Protocol):
    """Load a validated Enterprise configuration from an external source."""

    def load(self, path: Path) -> EnterpriseConfig:
        """Load and validate configuration from the supplied path."""
        ...
