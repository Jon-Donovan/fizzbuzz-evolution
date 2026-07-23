# ADR 0004: Use Versioned YAML for External Configuration

- Status: Accepted
- Date: 2026-07-23

## Context

The Enterprise stage needs human-readable external configuration for defaults, logging, and rule
registration.

## Decision

Use YAML with an explicit schema version and typed validation models. Command-line values override
YAML values, and YAML values override built-in defaults.

## Consequences

Configuration is readable and reviewable, while validation failures remain controlled. PyYAML is
a runtime dependency. Schema evolution must preserve or explicitly reject older versions.
