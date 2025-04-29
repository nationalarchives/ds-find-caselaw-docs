# 48. Assign FCL-specific IDs to documents at publication time

Date: 2025-04-29

## Status

Accepted

## Context

Following [ADR 47](ADR0074), although we can accept documents without NCNs, resolving URLs to a document relies on the presence of an identifier which can compile to a URL slug. Since we only currently support Neutral Citation Numbers as identifiers, and these documents do not have one, they remain inaccessible to the public.

We need to introduce an identifier which can be issued to all documents, regardless of the presence (or not) of other identifiers. This identifier should be entirely within a namespace controlled by Find Case Law, so it is not subject to external concerns.

## Decision

Based on the work in [ADR 18](ADR0018), we will issue all documents a new "Find Case Law Identifier" (FCLID for short). This will be generated using the [SQID](https://sqids.org) library based on a sequential number stored in MarkLogic.

Although the SQID library has a blacklist of words which should not be generated, we will further restrict the alphabet to remove all vowels and all letter/number combinations which are easily confused, leaving us with the following alphabet:

`bcdfghjkmnpqrstvwxyz23456789`

We will generate all FCLIDs with a minimum length of eight characters.

### URL slug generation

When generating URL slug patterns (see [ADR 47](ADR0074)) for FCLIDs we will use the form `tna.{id}`, for example identifier `cw7s3kws` will compile to URL slug `tna.cw7s3kws`.

## Consequences

All _published_ documents will have at least one identifier in the form of a FCLID, but published documents with an NCN will have at least two identifiers. UIs should be able to handle this situation.

There will be a period where not all documents have FCLIDs until data maintenance tasks are run. This is not considered an issue, as accessibility via an FCLID will be new functionality for those documents and its abscence will not be a regression.

Users may experience confusion that multiple URLs return the same document.

We must make sure we properly declare canonical document URLs for search engines.

The MarkLogic database now stores a sequential number which is critial for identifier minting, and we must be aware of this and make sure appropriate record locking is in place to avoid race conditions.

### Supersedes

- This supersedes [ADR 18](ADR0018), since we have decided allocating identifiers which look and behave similarly to NCNs but which aren't is a bad idea.

[ADR0018]: 0018-pseudo-ncns.md "Pseudo-NCNs"
[ADR0047]: 0047-uncouple-document-uris-and-ncns.md "Uncouple document URIs and NCNs"
