# Iteration 7 — Completion

## Goal

Iteration 7 turns the completed educational implementations into a coherent versioned project
that can be tested, built, installed, and reviewed as a release artifact.

## Deliverables

- a unified behavioral contract covering every implementation;
- comparative documentation explaining design trade-offs;
- Architecture Decision Records for the most important choices;
- an enforced English-language policy for source documentation;
- package metadata and changelog updates for version `1.0.0`;
- CI checks for linting, formatting, typing, tests, coverage, package build, and artifact checks.

## Release verification

Run the complete local verification sequence:

```bash
ruff check .
ruff format --check .
mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The build must produce both a source distribution and a wheel. The wheel must expose the
`fizzbuzz-enterprise` console script and include the typed-package marker.

## Scope boundary

Version 1.0.0 intentionally excludes HTTP APIs, databases, containers, distributed processing,
plugin discovery, and asynchronous execution. These features would add infrastructure without
improving the educational comparison delivered by the project.
