# 24. Usage of GOV.UK Front-End

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law website is a public government service. The GOV.UK Frontend library provides pre-built, accessible components designed for government services.

### Problem

To develop new features efficiently, the project requires a component library that is accessible, follows industry standards, and minimises maintenance effort. Building all components from scratch would slow development and increase maintenance overhead.

### Goals

- Ensure accessibility in new features.
- Accelerate development.
- Maintain industry-standard component behavior.
- Minimise code maintenance.

## Options Considered

1. Build a custom component library from scratch.
2. Use the GOV.UK Frontend library as a dependency and override styling where necessary.
3. Fork the GOV.UK component library and modify core styles directly.
4. Use a third-party component library and style it to match Find Case Law branding.

## Decision

### Solution

- Add the GOV.UK Frontend library as a dependency.
- Override styles that do not align with Find Case Law where necessary.
- Keep CSS overrides as decoupled from the application as possible.
- Wrap GOV.UK components in Find Case Law-specific components to decouple usage from direct dependency on GOV.UK markup.

### Justification

- Using GOV.UK Frontend as a dependency ensures compatibility with upstream updates and feature additions.
- Overriding styles selectively minimises breaking changes and prevents tight coupling between Find Case Law styling and GOV.UK components.
- Abstracting GOV.UK components into Find Case Law equivalents allows for future changes with minimal impact when updating the library.

## Consequences

- New features can be built efficiently without unnecessary development overhead.
- Components remain accessible and adhere to government service standards.
- Decoupling from direct GOV.UK component usage reduces maintenance effort and limits the impact of upstream changes.
