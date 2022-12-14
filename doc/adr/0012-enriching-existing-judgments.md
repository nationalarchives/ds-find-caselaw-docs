# 12. Enriching existing judgments

Date: 2022-12-13

## Status

Accepted

## Context

At some point we'll need to enrich all the documents that are already on MarkLogic but haven't been enriched.

## Decision

Once the full pipeline is up and running, dxw will trickle them into the pipeline
as though they were just regular judgements [via the SNS endpoint]. They are then enriched
as normal, and then pushed back as normal without any changes on the enrichment end.

This also then means we have a mechanism for re-enriching the entire corpus if enrichment
substantially changes again in future; we just tweak what it thinks the latest version
should be and it'll slowly trickle everything through again.

(This last paragraph seems to imply building something that'll search the database for
unenriched published documents and passing a few of them to enrichment at a time; it's
not yet clear where it should live)

It's also worth considering this when tackling the backlog of judgments not yet on MarkLogic; this will automatically trickle feed in new judgments that are automatically marked as published but bypass the Editor UI and thus won't automatically get enriched on publish. (Or we can flag them up directly as part of the upload process.)


## Consequences

This seems like the simplest possible approach.
