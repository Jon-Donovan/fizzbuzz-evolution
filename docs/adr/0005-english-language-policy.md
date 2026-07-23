# ADR 0005: Keep Project Documentation and Code Comments in English

- Status: Accepted
- Date: 2026-07-23

## Context

Mixed-language comments and documentation reduce consistency and make automated review harder.

## Decision

Source code comments, docstrings, command-line messages, and repository documentation are written
in English. Translations may be maintained as separate artifacts when required.

## Consequences

The repository has one consistent technical language. A test scans maintained text files and
rejects Cyrillic characters so accidental regressions are detected during CI.
