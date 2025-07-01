# 49. Confirm Document URIs, Identifiers, Atom Feed IDs, FRBR Model and S3 Asset Key Structure

Date: 2025-07-01

## Status

Accepted

## Context

Up until now, the FRBR Work and Expression identifiers in our XML have been generated based on NCN-derived URLs, produced directly by the parser. This approach has repeatedly resulted in malformed or unstable identifiers when:

- Documents have no NCN
- The parser fails to extract an NCN correctly
- NCNs later change (for example, due to B-NCNs or data corrections)

This has led to inconsistencies and broken assumptions in our metadata model.

In addition:

- Our document URIs for newly published documents have moved to UUIDs for guaranteed uniqueness (see [ADR 47](ADR0047)).
- Older documents (pre-d-UUID introduction) continue to reside at NCN-based URIs in MarkLogic.
- We now issue FCLIDs to all documents for consistent, stable, human-facing identifiers (see [ADR 48](ADR0048)).

Although this change could be viewed as a breaking change, in reality the prior model has been broken and unreliable. We already change XML metadata whenever we republish a document for other reasons, so this fits within our operational norms.

## Decision

### MarkLogic Document URI

All newly published documents (post-introduction of d-UUIDs) are stored in MarkLogic at a d-UUID-based URI assigned at ingestion.

Pre-existing documents (before d-UUIDs were introduced) continue to reside at NCN-based URIs in MarkLogic.

We will not use FCLIDs as document URIs, because UUIDs guarantee uniqueness at scale without risk of collision.

### FRBR Identifiers

Work identifier: The FRBR Work will use the FCLID as its identifier.

Expression identifier: The FRBR Expression will use the MarkLogic document URI:

- d-UUID for documents published since introduction of UUID URIs
- NCN-based URI for documents published earlier

This ensures:

- We have consistent, valid, and stable identifiers for both Work and Expression, even if NCNs change.
- We remove reliance on potentially unstable or missing NCNs for these fundamental identifiers in new data.

### Atom Feed ID

Atom `<id>` elements will continue to be based on the document’s MarkLogic URI:

- Post-UUID: d-UUID
- Pre-UUID: existing NCN-based URI (legacy)

We will not change Atom feed structure at this time.

### S3 Asset Key Structure

S3 asset keys will continue to align with the MarkLogic document URI (d-UUID).

### Migration and Communication Plan

We will:

- Implement code that modifies XML on the fly to emit the correct Work and Expression identifiers.
- Make this behaviour opt-in initially:
  - Republishers will explicitly opt-in to receiving the updated XML.
  - We will coordinate this via Lisa McGuinness, who will notify republishers when and how they can test the new behaviour.
- Allow at least one month for republishers to test and adopt the change.
- After the transition period, forcibly enable the new behaviour for all consumers.
- At our convenience, perform a data migration on stored XML to bring it in line permanently.
- Finally, remove the temporary code shim once the migration is complete.

We will support this change with:

- A web page in our web app documenting XML, Atom feed, and asset structures clearly for users.
- Direct communications to users explaining the change and its rationale.

## Consequences

Our FRBR model will be reliable and consistent across all documents.

We eliminate a long-standing source of malformed metadata and fragile identifiers.

External consumers will be given time and support to adapt.

Our versioning and republishing behaviour will remain consistent with how we have operated to date.

## Supersedes

This ADR clarifies and finalises decisions that build on:

- [ADR 4](ADR0004): uncoupling document URIs from NCNs
- [ADR 17](ADR0017): assigning FCLIDs to documents
- [ADR 47](ADR0047): pseudo-NCNs (effectively deprecated in favour of FCLIDs for Work IDs)

[ADR0004]: 0004-adopt-a-standardised-url-scheme.md "Adopt a standardised URL scheme"
[ADR0017]: 0017-pseudo-ncns.md "Pseudo-NCNs"
[ADR0047]: 0047-uncouple-document-uris-and-ncns.md "Uncouple document URIs and NCNs"
[ADR0048]: 0048-assign-fcl-specific-ids-to-documents-at-publication-time.md "Assign FCL-specific IDs to documents at publication time"
