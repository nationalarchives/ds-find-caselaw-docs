# 12. Enriching existing judgments

Date: 2022-12-13

## Status

Accepted
Edited 2024-01-11 to reflect as-implemented

## Context

We now enrich all the documents that are already on MarkLogic but haven't been enriched.

## Decision

We trickle them into the pipeline as though they were just regular judgements [via the custom-api, which is via the SNS endpoint]. They are then enriched
as normal, and then pushed back as normal without any changes on the enrichment end.

There is a (cronjob)[https://github.com/dxw/dalmatian-config/pull/833/files] that runs  in the Editor UI once a minute, passing the most recent unenriched document (determined via (xquery)[https://github.com/nationalarchives/ds-caselaw-custom-api-client/blob/cf40f5cb26b40a79786c8d2f8d6b988e65a34735/src/caselawclient/xquery/get_pending_enrichment_for_version.xqy], published or not.

The speed of the enrichment trickle-feed is (controllable)[https://github.com/nationalarchives/ds-caselaw-editor-ui/blob/ba6fe691c33c45acadb6cc1a6a6f1db31db3f56f/judgments/management/commands/enrich_next_in_reenrichment_queue.py#L6]: whilst it'll take weeks at one a minute, we can walk-before-we-run and accelerate that if everything is happy.

## Consequences

We have a mechanism for re-enriching the entire corpus if enrichment
substantially changes again in future; we just tweak what it thinks the latest version
should be and it'll slowly trickle everything through again.

Historical judgments have already been processed by vLex. We now intend to remove this.

## Future decisions

We might choose to:

- reparse documents so that new parser improvements apply to existing documents
