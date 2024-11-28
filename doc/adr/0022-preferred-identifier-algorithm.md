# 23. Preferred Identifier Algorithm

Date: 2024-11-28

## Status

Draft

## Context

When moving to a model where multiple documents have multiple identifiers, we need to understand how we choose which one to display for human identification purposes.

## Decision

Scores for individual components are multiplied together; IDs scoring 0 are never routinely considered preferred. (Scores for a component are 1 unless otherwise specified)

#### Deprecation

Identifier is deprecated: 0
Document is deprecated: 0

#### Schema

Default: 0.5?
NCN: 1
BAILII: 0.8
FCL SQID: 0.01

#### Recentness

Take the most recent (which measure of recentness? on publication? identifier?) if all other choices are even.

### Other options

We probably want to be able to limit to "only public documents" (for the PUI), "only human friendly identifiers", which can also add a 0 modifier to an identifier/document pair.

## Consequences

We have a modular system for determining the best identifier/document to return in multiple scenarios.
