# 55. Determine original version of submitted asset during reprocessing

Date: 2026-02-09

## Status

Accepted

## Context

[ADR 53](0053-automated-document-metadata-cleansing.md) introduces the concept of automated processing of document assets once they have been uploaded to storage. In this specific case the processing is the removal of information which should not be made public, but in future it could hypothetically be extended to include other forms of processing.

However, this processing is performed on documents in-place, replacing the existing asset with the cleaned one. This can lead to a situation where cleaning operations with an undetected bug could destructively modify documents with no ability to recover information. Additional processing which may be added in the future could also compound this problem, for example image compression progressively degrading image quality.

## Decision

Asset processing will be changed so that processing is always applied to the original version of an asset as provided by the court. This version will be retrieved from the asset versions (managed at the storage layer) based on the heuristic described below.

### Always processing from original

Asset processing currently uses the latest 'current' version of an asset. Instead, it should inspect the version history of the asset in search of the latest version of the asset which was submitted by the court, and use this instead.

Specifically, this will be done by either:

- Where asset metadata is directly available, for example in a structured metadata table or response from the storage layer API, querying for the latest version which does not have the 'cleaned with version' marker.
- WHere queriable asset metadata is not available, starting with the newest version of the file, requesting the metadata, and inspecting it to see if the 'cleaned with version' marker is present. If the marker is present, moving to the next newest version and repeating the process until a version without the marker is found.

### Improved 'candidate' logic

The current version-based decision logic for if an asset is pending reprocessing – which uses a naïve major version comparison – will be replaced by more complex logic which is capable of (for example) reprocessing specific versions or file types.

Implementation of this logic is not defined in this ADR.

## Consequences

- All future decisions around storage of assets must be made with this ADR in mind, as storage-level versioning with no limit on retention period is required to guarantee access to the original asset.
