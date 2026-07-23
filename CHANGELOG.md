# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-07-23

### Added

- Unified evaluation and sequence contracts across all five implementation styles.
- Comparative architecture documentation and completion guide.
- Architecture Decision Records for iterative evolution, the rule engine, ports and adapters,
  YAML configuration, and the English-language policy.
- Automated repository language-policy verification.
- Release tooling extras and package artifact validation guidance.

### Changed

- Promoted package metadata to version `1.0.0` and stable development status.
- Set the test suite minimum coverage threshold to 95 percent.
- Replaced the remaining Russian Senior-stage documentation with English documentation.
- Expanded CI to validate built distributions with Twine.


## [0.5.0] - 2026-07-23

### Added

- Typed, versioned YAML configuration for application defaults, logging, and divisibility rules.
- Infrastructure rule provider and explicit composition root for configured applications.
- Enterprise CLI with stable exit codes and CLI-over-YAML precedence.
- Plain-text and structured JSON presenters.
- Central logging configuration that keeps stdout machine-readable.
- Unit, integration, and subprocess acceptance tests for the complete Enterprise pipeline.
- English documentation and an example YAML configuration.

### Changed

- Added PyYAML as a runtime dependency and the `fizzbuzz-enterprise` console script.
- Updated project and package versions to `0.5.0`.


## [0.4.0] - 2026-07-23

### Added

- Enterprise domain value objects for numbers, ranges, rule identifiers, rule outputs, and evaluations.
- Enterprise rule protocol and divisibility rule with explicit domain validation.
- Structured domain evaluation service preserving all matching rule outputs.
- Application command, result, `RuleProvider` port, and sequence generation use case.
- Classic Enterprise preset and manual composition helper.
- Enterprise domain and application unit tests.
- Enterprise integration with the shared stage behavior contract.
- English documentation for the Enterprise domain/application architecture.

### Changed

- Marked the Enterprise domain/application stage as implemented.
- Updated project and package versions to `0.4.0`.

## [0.3.0] - 2026-07-22

### Added

- Structural `Rule` protocol and immutable `DivisibilityRule`.
- Ordered `RuleEngine` that composes all matching rule outputs.
- Classic FizzBuzz preset and engine factory.
- Senior-stage range generator and testable CLI.
- Validation errors for zero divisors, empty replacements, and reversed ranges.
- Tests proving extension through custom rules without engine changes.
- Senior-stage documentation and shared contract coverage.

### Changed

- Added the Senior implementation to module entry-point integration tests.
- Updated project and package versions to `0.3.0`.

## [0.2.0] - 2026-07-22

### Added

- Middle-stage evaluator, inclusive range generator, and testable CLI.
- Typed `FizzBuzzError` and `InvalidRangeError` exception hierarchy.
- CLI options for custom `--start` and `--end` bounds.
- Boundary tests for zero, negative values, single-value ranges, and reversed ranges.
- Middle-stage documentation and shared behavioral contract coverage.

### Changed

- Added the Middle implementation to the module entry-point integration tests.
- Updated project and package versions to `0.2.0`.

## [0.1.0] - 2026-07-22

### Added

- Classic textbook FizzBuzz implementation with an explicit `% 15` branch.
- Literal FizzBuzz implementation based on independent `% 3` and `% 5` conditions.
- Inclusive range generators for both stages.
- Module entry points for running each stage from the command line.
- Unit tests, shared contract tests, and command-line tests.
- English documentation for the classic and literal stages.

### Changed

- Standardized source code, comments, docstrings, and documentation on English.
- Synchronized the package version at `0.1.0`.

### Removed

- Generated `fizzbuzz_evolution.egg-info` metadata from the source tree.
