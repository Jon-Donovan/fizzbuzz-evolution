# ADR 0003: Isolate Enterprise Domain and Application Layers

- Status: Accepted
- Date: 2026-07-23

## Context

Configuration files, command-line parsing, logging, and serialization change for reasons that are
unrelated to FizzBuzz evaluation.

## Decision

The Enterprise implementation separates domain models and services, application commands and use
cases, infrastructure adapters, presentation adapters, and a composition root. The application
layer depends on the `RuleProvider` port rather than YAML or CLI details.

## Consequences

Domain behavior can be tested without infrastructure. Adapters can change independently. The
additional structure is educational and would be excessive for the smallest implementation.
