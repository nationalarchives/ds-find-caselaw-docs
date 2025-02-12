# 29. CSS Spacing Variable Convention

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

Spacing values across the application are currently inconsistent and do not follow a standardised convention.

### Problem

The lack of a consistent spacing convention results in:

- Inconsistencies in user experience and visual design.
- Increased maintenance overhead when adjusting spacing.
- Difficulty in making layout changes efficiently.

### Goals

- Standardise spacing values across the Find Case Law front-end.
- Reduce maintenance effort when updating spacing.
- Provide a clear convention to enable faster development and modifications.

## Options Considered

1. **Use SCSS functions** – Generate spacing values dynamically based on a base size (e.g., `calc(base-size * 1.5)`).
2. **Use named size variables** – Define a static set of variables (`xs`, `sm`, `lg`, `xl`) based on relative size.
3. **Use numerical naming convention** – Define a static set of variables using a numbered scale (`space-1`, `space-2`, etc.).
4. **Use variables that mimic values** – Define variables where the name directly reflects the value (e.g., `space-1` equals `1rem`).

## Decision

### Solution

Adopt a static set of variables following a numerical naming convention (e.g., `space-1`, `space-2`, etc.).

### Justification

- SCSS functions add unnecessary cognitive complexity, as the output is not immediately clear when reading the SCSS.
- Named size variables (e.g., `xs`, `sm`, `lg`) lack clear relationships between values, making it harder to determine spacing hierarchy.
- Variables that mimic their values directly (e.g., `space-1 = 1rem`) create unnecessary maintenance overhead, as renaming would be required if values change.
- A numerical naming convention provides:
  - **Consistency** – Ensures predictable spacing across the application.
  - **Maintainability** – Values can be adjusted without renaming variables.
  - **Clarity** – Developers can easily compare spacing values in relation to each other.

## Consequences

- **Consistent user experience** – Spacing will be uniform across the website.
- **Simplified development** – A clear convention reduces ambiguity and speeds up implementation.
- **Easier maintenance** – Updating spacing values will not require renaming variables.
