# 52. Keep shared metadata in the utilites repository

Date: 2025-12-17

## Status

Accepted

## Context

[ADR 51](0052-keep-shared-metadata-in-the-utilites-repository.md) introduces a new JSON Schema file which defines the shape of the metadata JSON output by the parser. This is the latest in a line of files which define common standards for data across the Find Case Law service, including the database XML schema and courts data. Instead of these files being scattered around various repositories, they should be kept in one location to simplify referencing them.

## Decision

We will keep the canonical versions of these common schemas, definitions, metadata and similar in the [utilities repository](https://github.com/nationalarchives/ds-caselaw-utils). Wherever possible, these will be stored in language-agnostic formats such as YAML, JSON or XSD.

When derived artefacts such as typed classes or documentation are also included, they shall be automatically generated from the canonical version and this generation shall be enforced through the use of CI.

New shared schemas, definitions etc shall be put in the utilities repository by default. Where appropriate, migration plans will be put in place for those already existing.

## Consequences

- A process will need to be put in place in downstream repositories to ensure they are kept up to date with changes to the common metadata and schemas.
- Plans to migration existing schemas etc will need to be put in place.
