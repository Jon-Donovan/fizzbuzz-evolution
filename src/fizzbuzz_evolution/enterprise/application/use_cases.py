"""Enterprise application use cases."""

from ..domain import EvaluationService, NumberRange
from .commands import GenerateSequenceCommand
from .ports import RuleProvider
from .results import GenerateSequenceResult


class GenerateSequenceUseCase:
    """Generate structured evaluations for an inclusive number range."""

    def __init__(self, rule_provider: RuleProvider) -> None:
        self._rule_provider = rule_provider

    def execute(self, command: GenerateSequenceCommand) -> GenerateSequenceResult:
        """Execute the sequence generation use case."""
        number_range = NumberRange(command.start, command.end)
        evaluator = EvaluationService(self._rule_provider.get_rules())
        items = tuple(evaluator.evaluate(number) for number in number_range)
        return GenerateSequenceResult(start=command.start, end=command.end, items=items)
