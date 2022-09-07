# 9. Reading unpublished judgments and Marklogic security boundaries

Date: 2022-08-24

## Status

Accepted

## Context

We need to stop people and applications reading things that aren't published yet unless they have permission to do so.
Historically this has been handled at the application level: the public-ui only shows published documents and the editor-ui can show both.

But with the creation of the privileged API there may be users (although who they are isn't clear) who shouldn't be able to read unpublished documents.

Ideally, we'd like the security boundary to be at Marklogic: if the Marklogic user (from the basic auth credentials passed by the Priv API, for example)
has permission to do something, then they can do it. That would involve changing where the concept of being published is from a property of the document
to being a permission on the document (e.g. `caselaw-unpublished-reader` can read this document) which could be exposed.

(we suspect we'd be using [`xdmp:document-[get|add|remove|set]-permissions`](https://docs.marklogic.com/xdmp:document-set-permissions) )

But that's a big change we're not ready to commit to yet, so...

## Decision

We have a function called `verify_show_unpublished` in the `custom-api-client` which usually returns the value of `show_unpublished` passed to it which can then be passed to the XQuery. But, if the user doesn't have the `caselaw-unpublished-reader` role and requested `show_unpublished=True` in the function, it returns `False` so they will not see any unpublished documents.

Currently the `caselaw-reader` permission can be used to prevent privileged API client users from reading unpublished documents, but applications with this permission (e.g. `public-ui`, `editor-ui`) from using the Marklogic interface if they directly import `custom-api-client`. The `editor-ui` should receive the `caselaw-unpublished-reader` role for clarity's sake.

## Consequences

We must not allow a user without `caselaw-unpublished-reader` to upload arbitrary XQuery since they would bypass `verify_show_unpublished` and be able to see unpublished documents.

We must remember to include calls to `verify_show_unpublished` any time we make a query that considers unpublished documents.

We must remember to appropriately give `caselaw-unpublished-reader` and `caselaw-reader` to users who need to see or not see unpublished documents.
