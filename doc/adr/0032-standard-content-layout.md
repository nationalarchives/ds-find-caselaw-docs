# 32. Standard Content Layout

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law website includes multiple content pages, but their layouts are inconsistent and loosely defined.

### Problem

- Content pages do not follow a standardised format, leading to inconsistencies in structure and design.
- Duplication of HTML across pages increases maintenance effort.
- Adding new content pages without a clear structure introduces further inconsistencies.

### Goals

- Establish a standardised content layout for the majority of content pages.
- Clearly define layout sections to ensure consistency and ease of extension.
- Reduce HTML duplication across content pages.

## Options Considered

1. Maintain the current loosely defined format and migrate non-conforming content pages to it.
2. Implement a new standardised content layout with clearly defined sections and move duplicated HTML to a base layout.

## Decision

### Solution

- Implement a new standardised content layout with well-defined sections for different parts of the page.
- Refactor existing content pages to follow this layout where appropriate.

### Justification

- Ensures a consistent content structure across the website.
- Reduces duplication by centralising shared HTML elements in a base layout.
- Makes it easier to add new content pages without introducing inconsistencies.

## Consequences

- Existing content pages must be updated to adopt the new layout.
- New content pages will follow a predefined structure, simplifying development.
- Future updates to the content layout will require fewer modifications across multiple pages.
- Custom layouts will be needed for content pages that do not fit the standard format.
