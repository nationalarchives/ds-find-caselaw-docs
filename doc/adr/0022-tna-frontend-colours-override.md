# 22. TNA Front-End Colour Overrides

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The application uses colour values provided by the TNA front-end library. However, the available colours do not fully align with the requirements of Find Case Law.

### Problem

The existing TNA colour palette does not provide appropriate mappings for all features and areas within Find Case Law, resulting in inconsistent or suboptimal visual presentation.

### Goals

Establish a mechanism to define colours that align with the requirements of Find Case Law while maintaining compatibility with the TNA front-end library.

## Options Considered

1. Use an alternative colour scheme instead of the TNA colours.
2. Introduce additional colours outside the TNA scheme and combine them as needed.
3. Override specific TNA colours to better align with the Find Case Law design.

## Decision

### Solution

Override specific TNA colour values by importing the SCSS variable map into the application and redefining the relevant colours.

### Justification

- Maintains alignment with the colour choices defined in the colour variable ADR.
- Provides flexibility to adjust colour values as needed for Find Case Law.
- Reduces the need for a completely independent colour scheme.

## Consequences

- The application will diverge from the standard TNA colour scheme.
- Changes to the TNA colour variable map (e.g., naming conventions or format) will require updates to the implementation.
- The modified colours may not fully adhere to the accessibility standards of the TNA scheme.
