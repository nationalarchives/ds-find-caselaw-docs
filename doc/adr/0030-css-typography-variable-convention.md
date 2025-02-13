# 30. CSS Typography Variable Convention

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

Typography values across the application are currently inconsistent and lack a standardized convention.

### Problem

The absence of a consistent typography variable convention results in:

- Inconsistent user experience and design.
- Increased maintenance effort when updating typography.
- Unclear guidance on which typography values to use in different contexts.

### Goals

- Standardize typography values across the Find Case Law front-end.
- Reduce maintenance overhead when adjusting typography styles.
- Establish a clear naming convention to streamline development.

## Options Considered

1. Define typography values inline with no convention – Leaves styling inconsistent and difficult to manage.
2. Use SCSS functions to generate typography values dynamically – Increases cognitive complexity, making it harder to determine actual values.
3. Use a named size convention – Define a static set of variables based on descriptive sizes (`xs`, `sm`, `lg`, `xl`).
4. Use a numerical naming convention – Define a static set of variables using a numbered scale (`typography-1-text-size`, `typography-2-text-size`).
5. Use variables that directly mimic values – Assign variable names to their exact values (e.g., `typography-1-text-size = 1rem`), making updates more difficult.

## Decision

### Solution

Adopt a static set of variables following a named size convention (e.g., `typography-xs-text-size`, `typography-xl-text-size`).

### Justification

- Coupling typography variables to their intended use case ensures appropriate application and prevents misuse.
- Named size conventions (e.g., `xs`, `sm`, `lg`, `xl`) are intuitive and immediately indicate their relative sizes.
- Avoids ambiguity compared to numerical naming (`typography-1-text-size`), which does not convey whether the size is small or large (e.g., `h1` is large, but `1` is not inherently meaningful).

## Consequences

- **Consistent user experience** – Typography remains uniform across the website.
- **Improved maintainability** – Updating typography styles will be straightforward and predictable.
- **Easier development** – Developers can quickly understand and apply the correct typography variables.
