# 44. Judgment Tables

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

Judgments often contain tables of varying structures and data formats.

### Problem

A single, standardised approach to rendering tables does not work across all judgments due to the diversity in content and formatting. In some cases, tables become illegible, making the current solution inadequate.

### Goals

- Ensure judgment tables are easy to read on desktop.
- Ensure tables remain accessible and viewable on smaller devices.

## Options Considered

1. Require submitted judgments to follow a specific table format and reject non-compliant submissions.
2. Modify the parser to convert all tables into a standard format.
3. Implement CSS that works for the majority of judgment table cases.

## Decision

### Solution

Implement CSS that supports the majority of judgment table cases.

### Justification

- Requiring authors to follow a strict table format is impractical.
- Automatically converting tables via the parser is unreliable, as inferring context from a judgment is difficult.
- A CSS-based solution allows tables to be displayed as intended while improving readability and accessibility across different devices.

## Consequences

- Judgment tables will remain as close as possible to their original format while being readable on both desktop and mobile.
- Some tables may still require improvements, so CSS should be refined as needed while ensuring backward compatibility.
- Authors of judgments will not need to change their current formatting practices.
