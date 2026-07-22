# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Implement the `05-enterprise` stage.

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
