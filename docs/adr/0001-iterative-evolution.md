# ADR 0001: Present One Problem Through Iterative Designs

- Status: Accepted
- Date: 2026-07-23

## Context

Architectural concepts are easier to compare when behavior remains stable. Separate unrelated
examples make it difficult to identify which complexity belongs to the domain and which belongs
to the design approach.

## Decision

The project implements the same FizzBuzz behavior in named stages: Classic, Literal, Middle,
Senior, and Enterprise. Shared contract tests protect the common behavior while stage-specific
tests document each design.

## Consequences

Readers can compare implementations directly. Some duplication is intentional because each stage
must remain understandable without depending on the previous stage's internals.
