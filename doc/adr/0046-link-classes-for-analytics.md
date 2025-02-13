# 46. Link Classes for Analytics

**Date:** 2025-02-12
**Status:** Proposed

## Context

### Background

The Find Case Law Public User Interface contains many links that need to be tracked for analytics purposes.

### Problem

Google Analytics no longer automatically tracks button text for events. Instead, it relies on element classes to determine which link triggered an event.

### Goals

- Enable Google Analytics users to easily identify which link triggered an event.
- Implement a low-maintenance solution that requires minimal developer intervention.

## Options Considered

1. Manually add a link class to all tracked links.
2. Use a django template tag to automatically append an analytics class to links.

## Decision

### Solution

Implement a django template tag that automatically adds an analytics-specific class to links.

### Justification

- Keeping analytics-related classes separate ensures they do not interfere with functional classes used for styling or other purposes.
- Automating class assignment through a template tag reduces manual effort and minimises the chance of inconsistent analytic classes.

## Consequences

- Google Analytics users will be able to easily track which links trigger events.
- Analytics classes will be isolated to avoid conflicts with existing styles.
- The template tag will need to be implemented and applied to all relevant links.
