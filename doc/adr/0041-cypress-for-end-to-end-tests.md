# 41. Cypress for End-to-End Tests

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

Cypress has been set up for end-to-end testing in the Find Case Law Editor User Interface project. However, it has never been fully configured and currently lacks tests. In contrast, Playwright has been properly configured in the Find Case Law Public User Interface repository and has extensive end-to-end tests.

### Problem

Using different tools for end-to-end testing across projects creates inconsistency and requires developers to switch between different testing frameworks. Maintaining both Cypress and Playwright would add unnecessary complexity.

### Goals

- Standardise end-to-end testing across projects.
- Use a single tool to simplify development and maintenance.
- Implement end-to-end tests in the Find Case Law Editor User Interface.

## Options Considered

1. Replace Cypress with Playwright.
2. Replace Playwright with Cypress.
3. Use a different end-to-end testing tool entirely.

## Decision

### Solution

Replace Cypress with Playwright in the Find Case Law Editor User Interface.

### Justification

- Playwright is already fully configured and in use in the Find Case Law Public User Interface repository.
- Standardising on Playwright allows developers to leverage existing knowledge and setup from the other repository.
- Using a single testing framework reduces complexity and ensures consistency across projects.

## Consequences

- Cypress will be removed from the Find Case Law Editor User Interface as it is not currently used.
- Playwright will be set up in the Find Case Law Editor User Interface, and end-to-end tests will be added.
- The presence of end-to-end tests will provide greater confidence when making changes and implementing new features.
