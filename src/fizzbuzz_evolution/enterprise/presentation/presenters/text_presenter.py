"""Plain-text Enterprise result presenter."""

from ...application import GenerateSequenceResult


class TextPresenter:
    """Render one evaluated value per line."""

    def present(self, result: GenerateSequenceResult) -> str:
        """Render the sequence as plain text without a trailing newline."""
        return "\n".join(item.value for item in result.items)
