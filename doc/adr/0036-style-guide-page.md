# 36. Style Guide Page

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law website contains numerous components used across different pages.

### Problem

- There is no centralised view of available components, their variations, or documentation explaining their intended use.
- Developers and designers lack a clear reference for maintaining consistency across the website.

### Goals

- Provide a way to visualise all available components.
- Document component variations and usage guidelines.

## Options Considered

1. **Use Storybook** – A widely used tool for component documentation, but primarily designed for React-based projects.
2. **Build a custom style guide page** – A simple, standalone page listing components and their variations.

## Decision

### Solution

Develop a style guide page to document and display available components.

### Justification

- Storybook is a powerful tool but is optimised for React-based applications, making it less suitable for Find Case Law.
- A custom style guide page is simpler to implement and better suited to the existing technology stack.
- Provides a centralised reference for developers and designers without requiring additional tooling.

## Consequences

- The style guide page will provide a single source of truth for component design and usage.
- Developers will need to manually update the style guide as new components are added.
