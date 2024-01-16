# 16. Re-parsing

Date: 2024-01-16

## Status

Accepted

## Context

Documents that have been on the site for a while were parsed with an older version of the parser. There are a number
of improvements which have been made since which will not be reflected in the XML. We can resend a document to parser
to get an up-to-date XML.

Naively, this would remove all the editor's human-approved metadata, so we must ensure that the metadata is preserved.
We do this by sending the metadata to the parser, which uses it preferentially to what it discovers in the document.

This also removes enrichment; we don't consider this to be a problem. It will be enriched by the 1/minute trickle feed.

## Implementation

We publish a JSON string to the TRE event bus, containing:

properties.messageType: the string literal "uk.gov.nationalarchives.da.messages.request.courtdocument.parse.RequestCourtDocumentParse"
properties.timestamp: When we sent the message as an ISO8601-timestamp ending in "Z" (UTC)
properties.function: the string literal "fcl-judgment-parse-request"
properties.producer: the string literal "FCL"
properties.executionId: A unique string. There may be limitations on its length.
properties.parentExecutionId: None

parameters.s3Bucket: the S3 bucket the docx is stored in
parameters.s3Key: the path in the S3 bucket of the docx
parameters.reference: For reparsing, this should be the "TDR reference" that the docx that we are sending arrived in.
    For any documents that are not reparses (but original parses), the document should contain a unique reference, possibly starting with FCL instead.
parameters.originator: the string literal "FCL"
parameters.parserInstructions.documentType: optional, either "judgment" or "pressSummary", controls how it is parsed.

We think we'll also have

parameters.parserInstructions.metadata.neutralCitation: Instruct parser to not determine the neutral citation and just respond with this value
and similarly .court, .documentDate and .documentName -- spellings to be decided. Maybe .url / .uri too.

---

TODO:
how we pick things to reparse, when we reparse, relationship to the enrich workflow




## Decision

The change that we're proposing or have agreed to implement.

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change that will need to be mitigated.
