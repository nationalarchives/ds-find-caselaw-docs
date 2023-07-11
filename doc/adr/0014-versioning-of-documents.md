# 14. Versioning of Documents

Date: 2023-05-17

## Status

Accepted

## Context

It's not quite clear what versions are meant to reflect. Is this a history of that URI, warts and all,
or is this a sanitised version reflecting only the history of that case.

A historical approach means that it's possible to understand the uglier parts of the history -- "oh,
/eat/2099/1 contained an unrelated file in January, that's why people are complaining about it having
changed."

A sanitised approach means that it's easier to understand the interactions with the courts -- "this document has
had three court-sent revisions; the second removes a comma and the third adds a paragraph of additional context"

We should be clear about our expectations for what a version in MarkLogic means, so that we can make appropriate
decisions when manually editing documents.

Historically we have typically deleted versions to make clear space for a judgment to arrive at that space by changing
the neutral citation number.

## Decision

We will take a historical approach: documents remain within the MarkLogic history unless there is a need to remove them.

## Consequences

- We SHOULD NOT expose older versions to the public without careful thoughts about the ramifications --
  there may be unrelated documents in there
- We SHOULD NOT routinely delete incorrect versions, although there may be technical reasons to do so, and
  we should recognise deletions have occurred in the past. (example: moving a document currently requires the URI
  to not contain an existing document, but that is likely to change soon.)
- We are able to understand more about the history of the URI by looking at the MarkLogic versions, with no omissions
- Some maintenance tasks will likely be easier since we do not need to worry about deleting versions.
