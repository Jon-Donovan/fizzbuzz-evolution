"""Rule provider built from validated infrastructure configuration."""

from dataclasses import dataclass

from ...domain import DivisibilityRule, Rule, RuleId
from ..config import DivisibilityRuleConfig


@dataclass(frozen=True, slots=True)
class ConfiguredRuleProvider:
    """Provide immutable domain rules created from configuration models."""

    rules: tuple[Rule, ...]

    @classmethod
    def from_configs(
        cls,
        configs: tuple[DivisibilityRuleConfig, ...],
    ) -> "ConfiguredRuleProvider":
        """Build domain rules from validated configuration entries."""
        rules: tuple[Rule, ...] = tuple(
            DivisibilityRule(
                rule_id=RuleId(config.rule_id),
                divisor=config.divisor,
                replacement=config.replacement,
            )
            for config in configs
        )
        return cls(rules)

    def get_rules(self) -> tuple[Rule, ...]:
        """Return configured domain rules."""
        return self.rules
