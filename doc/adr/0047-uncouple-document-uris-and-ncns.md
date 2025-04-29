# 47. Uncouple document URIs and NCNs

Date: 2025-04-29

## Status

Accepted

## Context

We are currently assuming that all documents reside at a URI which is informed solely by their Neutral Citation Number (see [ADR 4](ADR0004)). However, we are now required to store documents which do not have a neutral citation number at all.

We have considered using a 'pseudo-NCN' (see [ADR 18](ADR0018)) to resolve this issue, assigning documents without an NCN one which has been minted in-house. However, it was felt that the presence of a new identifier which looked and behaved exactly like a court-issued NCN but which wasn't one would cause issues.

## Decision

### Document URIs

#### Ingestion

We will completely uncouple a document's NCN from its URI (ie, from the location it is actually stored) and instead issue all new documents with a URI at ingestion time which is in the form of a UUIDv4 prefixed with the letter `d`, for example:

`d-1f8bcdda-5771-488d-9064-973f9f4b3c36`

This guarantees (to all intents and purposes) that no two documents can ever have a colliding URI.

#### EUI

The EUI will no longer attempt to move documents to a new URI when their NCN is changed; once a document has been assigned a UUID-based URI by the ingester that URI will never be altered.

### The identifier framework

Documents are currently accessed via their database URIs, prefixed with the `caselaw.nationalarchives.gov.uk` domain. We want to preserve the existing behaviour where a short URL based on the document's NCN can be used to access it, even if the underlying URI is UUID-based.

We will store these identifiers in the document properties in MarkLogic.

Each identifier will have a value (eg `[2025] UKSC 1`) and a schema to which it belongs (eg `Neutral Citation Number`).

#### Schemas

Each schema will contain rules for what constitutes a valid identifier under that schema, if we consider the identifier to be preferred for display, and how to convert that identifier value to a URL slug.

#### URL Slugs

By converting identifier values to precompiled URL slugs, we can use [TDE](https://developer.marklogic.com/concept/template-driven-extraction/) to maintain an indexed list of slugs and their corresponding documents in an SQL table. We can then use this to look up a slug and get the URI of the matching document. For example:

- Document `d-1f8bcdda-5771-488d-9064-973f9f4b3c36` has an identifier `[2025] UKSC 1`, under the schema `Neutral Citation Number`
- The `Neutral Citation Number` schema has rules for converting `[2025] UKSC 1` to the slug `uksc/2025/1`, matching the format in [ADR 4](0004-adopt-a-standardised-url-scheme.md). This is saved with the identifier and stored in the SQL lookup table.
- When a user visits `caselaw.nationalarchives.gov.uk/uksc/2025/1`, we extract the `uksc/2025/1` slug from the URL.
- Looking up ``uksc/2025/1` in the SQL table gives us document URL `d-1f8bcdda-5771-488d-9064-973f9f4b3c36`, which can be retrieved and returned to the user.

#### Identifying identifiers

All identifiers will have their own internal identifier within the system to allow future CRUD operations as necessary, in the form of a UUIDv4 prefixed with the letters `id`, for example:

`id-6d029496-c3d4-4168-a557-d85a2939a06b`

## Consequences

We will be able to accept documents which do not have an NCN.

We can extend the identifier framework to an arbitrary number of identifier schemas, allowing documents to be identified not just by NCN but potentially also by BAILII numbers, ECLIDs, case number and more.

In some contexts (particularly relating to machine usage of the data) the URI of a judgment's 'work' according to [ADR 4](ADR0004) will expose the full UUID-based URI. This will also apply to cases of downloading PDFs and other assets, including images. This is not considered to be a problem, since the 'human-readable' URLs provided by the identifier framework will remain short and readable in accordance with that ADR.

Existing processes may exist downstream which rely on semantic information within a URI. However, these would be incompatible with documents which do not have an NCN, so forcing downstream processes to handle non-semantic URIs with semantic data embedded elsewhere may be preferable.

### Supersedes

- This supersedes [ADR 4](ADR0004), since document URIs are now based on a UUID. For most user-facing aspects this will be irrelevant thanks to the use of compiled URLs for each identifier.

[ADR0004]: 0004-adopt-a-standardised-url-scheme.md "Adopt a standardised URL scheme"
[ADR0018]: 0018-pseudo-ncns.md "Pseudo-NCNs"
