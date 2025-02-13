# 35. Bundled JavaScript vs. Page-Specific JavaScript

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

Currently, all JavaScript for the Find Case Law website is bundled into a single file and included on every page.

### Problem

- Pages load unnecessary JavaScript that is not required for their functionality.
- This increases page load times and affects performance.

### Goals

- Improve page load times by reducing unnecessary JavaScript execution.

## Options Considered

1. **Continue serving all JavaScript on every page** – Simplifies implementation but negatively impacts performance.
2. **Use an automated JavaScript compiler to split JavaScript** – Provides automatic code splitting but may require additional configuration and overhead.
3. **Manually split JavaScript into modules and include only on relevant pages** – Ensures minimal JavaScript is loaded per page while maintaining control over what is included.

## Decision

### Solution

Manually split JavaScript into module and include only on the relevant pages.

### Justification

- Reduces load times by ensuring only required JavaScript is loaded on each page.
- JavaScript is only used on a few pages, making it feasible to manually manage module inclusion.
- Provides better control over which scripts are loaded, avoiding unnecessary complexity from automated splitting tools.

## Consequences

- Pages will load faster due to reduced JavaScript execution.
- Developers must ensure that JavaScript modules are explicitly included on the pages that require them.
- Encourages a modular approach to writing JavaScript, improving maintainability.
