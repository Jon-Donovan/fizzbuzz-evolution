"""Composition root helpers for the Enterprise stage."""

from dataclasses import dataclass
from pathlib import Path

from .application import GenerateSequenceUseCase
from .domain import Rule
from .infrastructure.config import EnterpriseConfig, YamlConfigLoader
from .infrastructure.rules import ConfiguredRuleProvider
from .presets import CLASSIC_RULES


@dataclass(frozen=True, slots=True)
class StaticRuleProvider:
    """Provide an immutable collection of rules for local composition."""

    rules: tuple[Rule, ...]

    def get_rules(self) -> tuple[Rule, ...]:
        """Return the configured rules."""
        return self.rules


@dataclass(frozen=True, slots=True)
class EnterpriseApplication:
    """Composed application services and their validated defaults."""

    use_case: GenerateSequenceUseCase
    config: EnterpriseConfig


def create_fizzbuzz_use_case() -> GenerateSequenceUseCase:
    """Create a sequence use case configured with classic FizzBuzz rules."""
    return GenerateSequenceUseCase(StaticRuleProvider(CLASSIC_RULES))


def create_application(config: EnterpriseConfig) -> EnterpriseApplication:
    """Compose an Enterprise application from validated configuration."""
    provider = ConfiguredRuleProvider.from_configs(config.rules)
    return EnterpriseApplication(GenerateSequenceUseCase(provider), config)


def create_application_from_config(path: Path) -> EnterpriseApplication:
    """Load configuration and compose the Enterprise application."""
    return create_application(YamlConfigLoader().load(path))
