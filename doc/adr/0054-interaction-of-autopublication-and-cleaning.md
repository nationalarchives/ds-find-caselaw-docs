# 54. Interaction of autopublication and cleaning

Date: 2026-02-06

## Status

Accepted

## Context

We want to clean assets associated with a document. This takes tens of seconds each (but parallelised),
and is triggered by the ingester putting the file into the S3 bucket, but does not have an obvious
feedback mechanism. This is a challenge when we want to publish the document, which will involve copying
the cleaned documents (there are checks that they are in fact cleaned) into the public bucket, so
publication cannot occur immediately.

## Decision

If the Ingester is instructed to autopublish a document, after uploading the files to S3 the ingester waits, allowing reasonable amount of time (30 sec - 5 min) in the hope that cleansing will have completed.

Regardless of the actual success or failure of the publishing operation, the ingest process is marked as a success so the ingested document is removed from the ingestion queue.

## Consequences

- We can autopublish cleaned documents
- Ingestion costs may rise due to additional time being used.
- Risk of lambda timeout if excessive delays are used. (max 900 seconds, 15 minutes)
- Documents will appear in the EUI list of documents either briefly
  during the delay, or require manual intervention if the document
  was not cleansed during that time period.
- Other approaches may have more favourable properties long term, but are quite a bit of work.

### Mitigations

We may want to consider hiding or marking records in the EUI which are flagged for autopublication but are not yet published.
We may want to treat those which are younger/older than the delay differently (e.g. hide for first 5 minutes)

### Alternative Strategies considered

- A worker periodically tries to publish documents flagged for autopublication but not yet published
- The cleaning process checks if the document is flagged for autopublication in MarkLogic, and if everything is cleaned, publishes
