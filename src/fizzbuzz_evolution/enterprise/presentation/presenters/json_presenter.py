"""JSON Enterprise result presenter."""

import json

from ...application import GenerateSequenceResult


class JsonPresenter:
    """Render the complete structured result as stable JSON."""

    def present(self, result: GenerateSequenceResult) -> str:
        """Render the public JSON representation of a sequence result."""
        payload = {
            "start": result.start,
            "end": result.end,
            "items": [
                {
                    "number": item.number.value,
                    "value": item.value,
                    "matches": [
                        {
                            "rule_id": match.rule_id.value,
                            "value": match.value,
                        }
                        for match in item.matches
                    ],
                }
                for item in result.items
            ],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
