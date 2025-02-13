# 28. Using SASS for All CSS

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law front-end requires a maintainable and efficient styling approach.

### Problem

Writing styles in pure CSS is inefficient, difficult to maintain, and increases the risk of inconsistencies across the application.

### Goals

- Implement a simple and efficient approach to writing CSS.
- Reduce duplication and promote reusability of styles.
- Ensure compiled CSS is optimised for performance.

## Options Considered

1. **Pure CSS** – Lacks support for variables, mixins, and other features that improve maintainability.
2. **LESS** – Similar to SCSS but less commonly used and supported in government services.
3. **SCSS** – Widely used, flexible, and compatible with GOV.UK Frontend and other government-supported libraries.
4. **Stylus** – Less commonly adopted and has a smaller ecosystem.
5. **PostCSS** – Powerful but primarily used for processing CSS rather than writing styles directly.

## Decision

### Solution

Adopt SCSS as the standard for all front-end styling in Find Case Law.

### Justification

- SCSS is widely used in public sector applications, including GOV.UK services.
- Seamlessly integrates with government-supported libraries such as GOV.UK Frontend.
- Enables writing efficient and maintainable CSS using variables, mixins, and nesting.
- Supports compiling optimised CSS with reduced duplication.

## Consequences

- SCSS-supported libraries can be integrated more easily.
- GOV.UK Frontend styles can be imported and customised as needed.
- Styles will be more maintainable, efficient, and consistent across the application.
