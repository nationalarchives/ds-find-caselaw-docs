# 45. Buttons

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The application contains multiple types of buttons with varying styles and implementations.

### Problem

- There is little consistency in how buttons are styled and composed.
- Different implementations have led to inconsistencies in the user experience and increased complexity when deciding how to style buttons.

### Goals

- Establish a core set of buttons with a standardised design.
- Ensure consistent button styles across the Find Case Law Public User Interface.
- Define a consistent approach to composing button styles.

## Options Considered

1. Define button mixins that can be imported into components.
2. Define a set of button classes for use across the application.
3. Style each button individually within its respective component.

## Decision

### Solution

Define a set of button classes to be used consistently across the application.

### Justification

- Buttons are standalone components and should be treated as such.
- Styling buttons via mixins within other components could introduce inconsistencies as additional styles are applied on a per-component basis.
- Using predefined button classes ensures consistency and avoids unnecessary duplication of styles.

## Consequences

- Using button mixins will be **deprecated** in favor of using button classes for new components.
- Buttons will have consistent styling throughout the Find Case Law Public User Interface.
- Composing components that use buttons will be simpler and more predictable.
