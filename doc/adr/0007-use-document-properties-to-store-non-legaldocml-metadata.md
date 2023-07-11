# 7. Use Document Properties To Store Non-LegalDocML Metadata

Date: 2022-02-23

## Status

Accepted

## Context

Judgment documents contain metadata such as title, court, date, etc, as well as the body of the judgment. However, we also need to store service-specific metadata, such as:

- Transfer Digital Records consignment number
- Is the judgment publicly available?
- When was the judgment last enriched?

Marklogic documents (and directories) have associated [Property Documents](https://docs.marklogic.com/guide/app-dev/properties). These documents can store arbitrary properties alongside the judgment documents themselves. These properties can be any XML element, and are searchable and queryable.

## Decision

We will use Marklogic's property documents and associated XQuery APIs to store service-specific metadata fields.

Metadata fields will be managed by the custom REST API, not by API clients directly. The API will validate metadata fields and check against an expected list as appropriate. Available metadata fields will be documented as part of that API.

## Consequences

New metadata fields can be added in an iterative fashion, over time, we do not need to specify them all up front.
