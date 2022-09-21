# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.0.0].

## [Unreleased]

## [Release 1.0.6]
- ADR 0009: Reading unpublished judgments and Marklogic security boundaries
- ADR 0010: Interface with Enrichment
- Use unfiltered search results
- Add KB to Neutral Citation regex in helper.xqy
- Search by consignment number
- support for new header alignment styles

## [Release 1.0.5]
- Grant the caselaw-writer role the ability to view unpublished documents
- Script to create python server (fastapi)
- Privileged API spec improvement
- Add VPN related documentation
- Create failover replicas for the caselaw-content databases
- Rename judgment0.xsl and judgment2.xsl to have more descriptive names

## [Release 1.0.4]
- changes for upcoming parser release: subparagraphs
- Add a new privilege and role allowing users to view unpublished documents

## [Release 1.0.3]
- Document FRBRdate discussion as an ADR
- remove inline fonts (except Symbol)
- remove <h2>s
- Deprecate loading data locally from S3

## [Release 1.0.2]
- use <b>, <i> and <u> elements

## [Release 1.0.1]
- Re-enable non-websafe images in the XSLT transformations

## [Release 1.0.0]
- Initial tagged release
- Add transformation sort order for search

[Unreleased]: https://github.com/nationalarchives/ds-caselaw-public-access-service/compare/v1.0.6...HEAD
[Release 1.0.6]: https://github.com/nationalarchives/ds-caselaw-public-access-service/compare/v1.0.6...v1.0.5
[Release 1.0.5]: https://github.com/nationalarchives/ds-caselaw-public-access-service/compare/v1.0.5...v1.0.4
[Release 1.0.4]: https://github.com/nationalarchives/ds-caselaw-public-access-service/compare/v1.0.4...v1.0.3
[Release 1.0.3]: https://github.com/nationalarchives/ds-caselaw-public-access-service/compare/v1.0.2...v1.0.3
[Release 1.0.2]: https://github.com/nationalarchives/ds-caselaw-public-access-service/compare/v1.0.1...v1.0.2
[Release 1.0.1]: https://github.com/nationalarchives/ds-caselaw-public-access-service/compare/v1.0.0...v1.0.1
- [keep a changelog 1.0.0]: https://keepachangelog.com/en/1.0.0/
