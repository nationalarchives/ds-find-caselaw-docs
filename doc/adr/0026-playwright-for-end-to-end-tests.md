# 26. Playwright for End-to-End Testing

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

End-to-end (E2E) tests are required to ensure the Find Case Law website functions as expected while implementing changes and new features.

### Problem

Currently, end-to-end testing is performed manually, which is time-consuming, prone to being overlooked, and increases the risk of regressions in less frequently used areas of the website.

### Goals

- Implement automated end-to-end tests for critical user paths.
- Integrate tests into the CI/CD pipeline for automated execution.
- Use a well-maintained and widely adopted testing framework.
- Ensure tests are written in a language all developers are comfortable with.

## Options Considered

1. **Cypress** – Popular and feature-rich but requires JavaScript/TypeScript.
2. **Playwright** – Supports multiple languages, including Python, and is well-maintained.
3. **Capybara** – Primarily used in Ruby environments, not suitable for this project.
4. **Puppeteer** – JavaScript-based and less feature-complete for end-to-end testing compared to Playwright.

## Decision

### Solution

Use **Playwright** for end-to-end testing.

### Justification

- Playwright supports Python, ensuring all developers can contribute to test writing and maintenance.
- It is a well-maintained, widely adopted, and feature-rich testing framework.
- Playwright provides robust support for modern web applications, including handling multiple browser contexts, network mocking, and parallel execution.

## Consequences

- End-to-end tests must be written and maintained for all critical user paths.
- Automated testing will increase confidence in the stability of the service during development and deployment.
- Updates to key user paths will require corresponding updates to the end-to-end tests.
