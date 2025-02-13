# 43. Judgment Paragraph Anchors

**Date:** 2025-02-07
**Status:** Accepted

## Context

### Background

Judgments include paragraph numbers, and users want the ability to link to specific paragraphs easily.

### Problem

There is currently no way for users to copy or share a direct link to a specific paragraph in a judgment.

### Goals

- Enable users to link directly to a specific paragraph in a judgment.
- Provide an easy way for users to copy a link to a paragraph.

## Options Considered

1. Add links directly into the XML that generates the HTML.
2. Dynamically add links to paragraphs using JavaScript.

## Decision

### Solution

Use JavaScript to dynamically add links to paragraphs.

### Justification

- Features must degrade gracefully when JavaScript is disabled. Since clipboard functionality requires JavaScript, coupling the entire feature to JavaScript ensures a consistent implementation.
- Modifying the XML generation process would require adding content that was not in the original document, which is undesirable.
- JavaScript-based implementation keeps the feature isolated from the XML and base HTML, reducing complexity.

## Consequences

- The paragraph linking feature will only be available to users with JavaScript enabled.
- The feature remains self-contained and does not impact the XML or base HTML.
- It can be enabled or disabled via a feature flag.
- Updates or modifications can be made without affecting multiple codebases.
