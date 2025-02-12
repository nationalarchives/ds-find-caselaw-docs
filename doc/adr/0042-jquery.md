# 42. jQuery

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

jQuery is currently used for some functions in the Find Case Law Public User Interface, but not consistently across the project.

### Problem

Modern JavaScript, combined with a JavaScript compiler, now provides the backwards compatibility that jQuery once offered. Since this functionality is already available, jQuery is no longer necessary and adds unnecessary bloat to JavaScript bundles.

### Goals

- Reduce JavaScript bundle size.
- Remove unnecessary dependencies.
- Future-proof the codebase by using modern JavaScript.

## Options Considered

1. Keep jQuery.
2. Remove jQuery and replace its functionality with modern JavaScript.

## Decision

### Solution

Remove jQuery.

### Justification

- jQuery is no longer required for backward compatibility.
- Removing jQuery will reduce the JavaScript bundle size.
- Using modern JavaScript aligns with best practices and improves maintainability.

## Consequences

- Existing jQuery code will need to be rewritten in vanilla JavaScript.
- JavaScript code will follow modern standards.
- The JavaScript bundle will be smaller and more efficient.
