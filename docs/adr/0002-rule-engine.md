# ADR 0002: Use an Ordered Rule Engine for the Senior Stage

- Status: Accepted
- Date: 2026-07-23

## Context

A fixed evaluator requires modification whenever another replacement rule is introduced.

## Decision

The Senior stage uses a structural `Rule` protocol and an engine that concatenates all matching
outputs in registration order. Engine configuration is immutable after construction.

## Consequences

New rules can be added without modifying the engine. Ordering remains explicit. The abstraction is
more complex than direct conditionals and is therefore reserved for the Senior stage.
