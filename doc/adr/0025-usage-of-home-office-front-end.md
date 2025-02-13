# 25. Usage of Home Office Front-End

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The application currently uses multiple alert components from different libraries, leading to inconsistencies in styling and behavior.

### Problem

The use of multiple alert component styles results in an inconsistent user experience and increases maintenance overhead by requiring support for multiple implementations.

### Goals

- Standardise the alert component across the application.
- Minimise maintenance effort.
- Ensure accessibility.
- Align the alert component's styling with the Find Case Law service.

## Options Considered

1. Build a custom alert component.
2. Use the GOV.UK Frontend alert component.
3. Use the TNA Frontend alert component.
4. Use the Home Office alert component.

## Decision

### Solution

- Use the Home Office alert component.
- Extract and integrate only this component rather than including the entire Home Office Frontend library.

### Justification

- The Home Office alert component aligns most closely with the Find Case Law styling, requiring minimal modifications.
- Using a pre-existing, accessible component reduces development and maintenance effort compared to a custom implementation.
- Extracting only the required component avoids unnecessary dependencies from the full Home Office Frontend library.

## Consequences

- The application will have a consistent and accessible alert component.
- The extracted component will need to be manually maintained as an external dependency.
