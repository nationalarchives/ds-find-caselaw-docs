# 34. GOV.UK Front-End CSS Imports

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law website currently imports the entire GOV.UK Frontend CSS.

### Problem

- Importing the full GOV.UK CSS includes unnecessary styles for unused components.
- This results in a larger CSS bundle, impacting performance.

### Goals

- Reduce the CSS bundle size by only including necessary styles.

## Options Considered

1. **Import the entire GOV.UK CSS** – Easier to maintain but includes unused styles, increasing bundle size.
2. **Import only the CSS for the components in use** – Reduces bundle size while requiring explicit imports when new components are added.

## Decision

### Solution

Only import the CSS for the GOV.UK components in use.

### Justification

- Reduces unnecessary CSS, improving performance.
- New component styles can be added incrementally as needed.
- Helps maintain a cleaner, more efficient stylesheet.

## Consequences

- Developers must manually import CSS when using a new GOV.UK component.
- If a GOV.UK component is removed, its associated CSS import must also be removed.
- The CSS bundle size will be reduced, improving load times and performance.
