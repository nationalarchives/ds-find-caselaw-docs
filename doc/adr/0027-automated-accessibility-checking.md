# 27. Automated Accessibility Checking

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

Automating accessibility testing is necessary to ensure that the Find Case Law service meets accessibility standards consistently.

### Problem

Accessibility testing is currently a manual process with no standardised approach. As a result, accessibility best practices are often overlooked during development, leading to inconsistent compliance and potential usability issues.

### Goals

- Implement an automated process to flag accessibility issues in the codebase.
- Standardise accessibility tests to ensure consistency and alignment with formal accessibility audits.

## Options Considered

1. **BrowserStack** – Provides accessibility testing as a service but adds external dependencies and potential cost overhead.
2. **PA11Y** – An open-source tool, but requires additional configuration and does not integrate with Playwright.
3. **Axe-Core** – A widely used accessibility engine, but would require additional scripting for automation.
4. **Wave Chrome Extension with a test script** – Useful for manual checks but does not support automated testing.
5. **Axe-Playwright** – A wrapper around Axe-Core that integrates directly with Playwright for automated accessibility testing.

## Decision

### Solution

Integrate **Axe-Playwright** into the existing automated test suite to perform accessibility checks on all pages covered by end-to-end tests.

### Justification

- Seamlessly integrates with the existing Playwright-based testing setup.
- Provides standardised accessibility checks aligned with industry best practices.
- Works within the CI/CD pipeline, enabling continuous accessibility monitoring.

## Consequences

- All pages covered by end-to-end tests will undergo automated accessibility checks, ensuring key user journeys remain accessible.
- Any new pages requiring accessibility validation must have corresponding Playwright tests.
- Large feature implementations that introduce accessibility issues will need to be fixed before merging and releasing code.
