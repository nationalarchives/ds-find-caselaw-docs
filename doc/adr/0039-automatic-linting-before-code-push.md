# 39. Automatic Linting Before Code Push

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

The Find Case Law codebase uses multiple linting tools to enforce consistency and industry standards.

### Problem

- Developers must manually run linting tools, configure their editor to run them automatically, or wait for CI/CD validation after pushing code.
- This can lead to inconsistencies, wasted CI/CD resources, and preventable errors being caught late in the development process.

### Goals

- Automatically enforce linting before code is pushed.
- Reduce manual effort required for running linters.
- Catch and fix linting issues early in the development workflow.

## Options Considered

1. **Use pre-commit hooks** – Runs linting checks before allowing a commit to be created.
2. **Use pre-push hooks** – Runs linting checks before allowing a push to the remote repository.

## Decision

### Solution

Use pre-commit hooks to enforce linting automatically before committing code.

### Justification

- Ensures that all committed code is linted and meets project standards.
- Prevents developers from pushing non-compliant code and relying on CI/CD for linting validation.
- Runs automatically on commit, requiring no manual intervention from developers.

## Consequences

- All committed code will be linted, ensuring consistency across the codebase.
- Developers accustomed to frequent small commits may need to adjust to a slower workflow due to linting execution.
- Developers must set up pre-commit hooks in each repository to ensure enforcement.
