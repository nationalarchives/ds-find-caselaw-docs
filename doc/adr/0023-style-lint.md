# 23. StyleLint Configuration

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

A basic configuration of StyleLint is currently enforced through a pre-commit hook. However, this configuration is minimal.

### Problem

The existing StyleLint setup lacks comprehensive rules to ensure consistent and standardised CSS. This results in potential inconsistencies that require manual intervention during development and code reviews.

### Goals

Implement an automated style linting configuration that enforces consistent and standardised CSS while minimising manual effort during composition and review.

## Options Considered

1. Use the `stylelint-selector-bem` library to enforce BEM class naming.
2. Use the `stylelint-clean-order` library to enforce a structured CSS property order.
3. Use `stylelint-standard-css` to enforce general CSS best practices.
4. Define a custom selector class pattern for BEM class naming.
5. Maintain a per-repository StyleLint configuration file.
6. Use a shared StyleLint configuration file across repositories, with the option for per-repository extensions.

## Decision

### Solution

- Use the `stylelint-clean-order` and `stylelint-standard-css` libraries for property ordering and general CSS best practices.
- Define a custom selector class pattern for BEM class naming.
- Maintain a shared StyleLint configuration file that can be extended by individual repositories as needed.

### Justification

- The `stylelint-clean-order` and `stylelint-standard-css` libraries provide effective linting out of the box, reducing the need to define custom rules.
- The `stylelint-selector-bem` library requires extensive configuration, making it equivalent to defining custom rules manually.
- A shared StyleLint configuration ensures consistency across repositories while allowing flexibility where necessary.

## Consequences

- The BEM selector function must be maintained internally. However, as the BEM methodology is stable, changes should be infrequent.
- Allowing repositories to extend the shared configuration introduces the possibility of slight deviations in CSS conventions across projects.
- Any updates to the StyleLint configuration will require corresponding updates in downstream repositories, including adjustments to any affected CSS.
