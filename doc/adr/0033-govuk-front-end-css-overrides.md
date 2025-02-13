# 33. GOV.UK Front-End CSS Overrides

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law website uses the GOV.UK Frontend CSS for styling components. However, some styles need to be overridden to better align with the service's design requirements.

### Problem

- There is a need to override certain GOV.UK Frontend styles while maintaining consistency.
- Overrides should be structured in a maintainable and scalable way.

### Goals

- Provide a structured approach for overriding GOV.UK Frontend styles.
- Ensure overrides are easy to manage and maintain.
- Prevent duplication and inconsistencies in overridden styles.

## Options Considered

1. **Single global CSS file for all overrides** – Centralises overrides but becomes difficult to manage as the number of overrides grows.
2. **Separate override files for each GOV.UK component** – Organises overrides per component, improving maintainability and discoverability.
3. **Override styles inline where each GOV.UK component is used** – Leads to duplication and inconsistency across the application.

## Decision

### Solution

Use separate CSS override files for each GOV.UK component that requires modifications.

### Justification

- Ensures consistency by centralising overrides per component.
- Prevents duplication, as overrides are applied once and reused throughout the application.
- Improves maintainability, making it easier to locate and modify specific component overrides.

## Consequences

- GOV.UK Frontend styles can be overridden in a structured and maintainable way.
- Styling changes will be easier to track and modify when needed.
- New overrides can be added systematically without affecting unrelated components.
