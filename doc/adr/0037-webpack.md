# 37. Webpack for JavaScript and CSS Compilation

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law website includes JavaScript functions that provide interactive features to users. Additionally, modern JavaScript syntax and uncompiled CSS may not be compatible with older browsers and can lead to unnecessarily large payloads.

### Problem

- JavaScript syntax varies across versions, and some features may not be compatible with older browsers.
- Without compilation and optimisation, JavaScript and CSS payload sizes can be unnecessarily large, affecting performance.

### Goals

- Ensure JavaScript is backward-compatible with older browsers.
- Minimise JavaScript and CSS bundle sizes to improve performance.

## Options Considered

1. **Webpack** – A widely used, feature-rich bundler that supports JavaScript and CSS compilation.
2. **ESBuild** – Extremely fast but less feature-complete and has limited plugin support for advanced bundling needs.
3. **Rollup** – Optimised for JavaScript library bundling but less suitable for full applications with CSS processing.

## Decision

### Solution

Use Webpack to compile JavaScript and CSS.

### Justification

- Webpack is an industry-standard tool with strong community support.
- Provides comprehensive bundling capabilities, including JavaScript transpilation and CSS processing.
- Supports backward compatibility for older browsers via Babel integration.
- Offers tree shaking and code splitting, reducing unnecessary JavaScript payload.

## Consequences

- JavaScript and CSS will be compiled before deployment, introducing an additional build step.
- Smaller bundle sizes will improve page load times.
- JavaScript will be more compatible with a wider range of browsers.
