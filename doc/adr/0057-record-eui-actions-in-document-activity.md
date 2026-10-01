# 57. Record EUI actions in document activity

Date: 2026-10-01

## Status

Accepted

## Context

The FCL team needs to understand which actions are performed through the Editor User Interface (EUI) and who performed them. The initial use case for this MVP is recording when a PDF is uploaded or replaced through the EUI.

The system uses DLS version annotations to record information about document updates. However, a PDF upload changes an S3 asset without changing the judgment XML. Recording this event as a DLS version annotation would therefore depend on MarkLogic creating a new DLS version for a save with unchanged XML, and that behavior is not established. Additionally, the system contains a mechanism for adding metadata, but this is intended for adding data about the judgments themselves, and is not a suitable place for recording EUI activity.

MarkLogic does not record whether a document has an associated PDF or who uploaded it. The API client builds a PDF link from the document URI without checking whether a PDF exists.

## Decision

For the MVP, record EUI actions in an append-only activity sidecar associated with the judgment or press summary in MarkLogic. Keep this sidecar separate from both the document XML and DLS version annotations, so an event can be recorded without changing the document content or creating a DLS version. The sidecar may be represented as an `<activity>` structure or an equivalent MarkLogic sidecar, following existing patterns for data stored alongside documents. Use 'activity' rather than 'history' to avoid confusion with DLS version history, and rather than 'audit' because this MVP does not provide a comprehensive audit trail.

The MVP will record successful PDF uploads and replacements only. Each activity entry will identify the action, when it occurred, the calling function and agent, and the requesting editor's username. Store the username or similar identifier as a string in `action_requested_by`. Define and document a schema for activity entries as part of implementation. The proposed payload shape is intentionally aligned with the existing DLS version annotation format: it uses the same top-level fields and keeps action-specific data in `payload`. This is a consistency choice; activity entries remain separate from DLS version annotations. The following illustrates the proposed event shape:

```json
{
  "type": "pdf_upload",
  "calling_function": "upload",
  "calling_agent": "ds-caselaw-editor/unknown {DEFAULT_USER_AGENT}",
  "automated": false,
  "message": "PDF uploaded",
  "payload": {
    "action_requested_by": "editor-username",
    "occurred_at": "2026-10-02T12:00:00+01:00"
  }
}
```

The activity entry will be added only after a successful upload or replacement. Failed upload attempts will not be recorded by this mechanism.

The EUI does not currently support deleting PDFs, so deletion events are outside the scope of this decision.

## Consequences

- PDF upload activity is stored separately from judgment metadata and DLS version history; recording an event does not alter or version the judgment XML.
- The activity sidecar and S3 upload are separate operations and are not atomic. If storing the activity entry fails after the S3 upload, the PDF may be stored without an activity entry; this ADR does not define a recovery mechanism.
- Storing an event in MarkLogic does not automatically make it visible in the existing EUI history view; displaying these entries there is outside the scope of this ADR.
- This MVP establishes a reusable pattern but records only PDF uploads and replacements. It does not establish a comprehensive audit model for all EUI operations or record failed attempts; these can be considered later if needed.
- The activity schema and write path will need to be implemented for this sidecar.
