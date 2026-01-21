# 50. Throw exception on metadata conflict in Parser

Date: 2025-11-20

## Status

Accepted

## Context

The Parser component is responsible for translating input documents (typically .docx or .pdf) into LegalDocML. During this process, the Parser has access to two distinct sources of metadata:

- Internal Metadata: Information embedded directly within the source document text and formatting
- External Metadata: Information provided alongside the document payload usually originating from the Editor or Backlog csv file.

Up until now, the external metadata has primarily been used to pass supplementary information which does not exist within the body of the document being parsed however upcoming work to the Backlog parser will introduce more externally overridable metadata which could feasibly conflict with information found inline within a document.

The reasons theorised that could cause a conflict are as follows:

- The Parser is pulling information from the document incorrectly
- The document contains a typo or alternative letter casing that an Editor is attempting to correct
- The information supplied in the Backlog csv is incorrect

We needed to determine the strategy for handling these collisions during the parsing phase. The options considered were:

- Trust Internal: Ignore external metadata if internal exists.
- Trust External: Overwrite internal metadata with external values silently.
- Merge/Hybrid: Attempt complex logic to determine which source is more trustworthy
- Fail: Halt the process and alert the caller.

## Decision

We will throw an exception in the Parser for new metadata override capabilities (such as Jurisdiction) when a specific metadata key exists in both the Internal and External sources but carries conflicting values.

The Parser will not attempt to resolve the conflict automatically.

- If a key exists only in Internal, it is preserved.
- If a key exists only in External, it is added.
- If a key exists in both and values are identical, the process continues.
- If a key exists in both and values differ, the parsing fails immediately.

## Consequences

### Positive

- We can evaluate specific scenarios as they occur which will give us more information about what the correct approach for the future should be.
- We eliminate the risk of silently publishing metadata that contradicts the source document without human oversight.
- It becomes immediately obvious when there is an issue.

### Negative

- The parser is stricter and hence more brittle. Minor whitespace differences or casing inconsistencies between the supplied metadata and the document will cause parse failures until normalisation logic is applied.
