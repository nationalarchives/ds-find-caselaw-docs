# 50. Remove metadata from documents stored by Find Case Law

Date: 2025-09-08

## Status

Accepted

## Context

Some documents sent to the Find Case Law service contain metadata which – whilst not necessarily sensitive – should not be provided as part of the published data, either to the general public or to republishers.

## Decision

Since the original submitted document is always sent to preservation, Find Case Law can safely remove this metadata from the files being stored and served to users.

We will do this by implementing lambda functions capable of taking an artefact (such as a `.docx` or `.pdf` file) from an S3 bucket, removing the unwanted metadata ('scrubbing' the file), and then replacing it with the new version. This artefact will have the fact this process has happened recorded as an [S3 tag](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

A workflow will be configured such that the act of creating or updating an artefact of the appropriate type will trigger this process (where a document has not already been scrubbed). For existing documents, we will run a one-time task to queue requests for all existing document artefacts.

Since all ingestion and submission routes ultimately result in document artefacts being added to an S3 bucket, this means we only have one place to manage this workflow for new and updated documents. Since the process runs as a lambda it will also easily scale with demand.

In addition to scrubbing document-level metadata, some unwanted data may exist as part of tracked changes, version history or comments. Removing these features can be difficult to do programmatically, but detecting their presence is much simpler. As such editors will receive a warning message when previewing or attempting to publish a document with these features present. They will _not_ be prevented from publishing, but the recommendation will be that the clerks resubmit a 'clean' version of the document.

### Metadata to remove

Specifically, we will be removing:

- Document-level author information
- Comment author information
- Tracked changes author information

## Consequences

- Editors may experience a small delay before documents can be safely published whilst this 'scrubbing' process takes place.
- Some documents submitted with tracked changes or comments may have publication delayed whilst clerks provide a version without these features.
- There will be an additional cost to accepting new documents. It is likely this will be a neglibible amount compared to the cost of running the service, and will only be incurred when there is a new submission (aside from the initial cleaning).
