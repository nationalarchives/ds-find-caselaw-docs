# 40. Atomic CSS Classes

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law website includes a small number of atomic CSS classes.

### Problem

- Atomic CSS classes have not been fully adopted, leading to inconsistencies in styling.
- Developers must reference multiple sources to understand how a component is styled, increasing cognitive complexity.

### Goals

- Establish a consistent approach to composing CSS.
- Reduce the cognitive complexity of maintaining and modifying styles.

## Options Considered

1. Fully adopt atomic CSS classes across all components.
2. Remove atomic CSS classes and rely on component-scoped styles.

## Decision

### Solution

Remove atomic CSS classes in favor of component-scoped CSS.

### Justification

- Atomic CSS classes are not widely used and contribute to inconsistency rather than simplifying styling.
- Removing them reduces complexity by consolidating styling within component-specific CSS.
- A component-scoped approach improves readability and maintainability.

## Consequences

- Existing atomic CSS classes will need to be deprecated and replaced with component-scoped styles.
- The transition will be incremental, requiring updates across the codebase.
- The Find Case Law CSS will become easier to understand and maintain.
