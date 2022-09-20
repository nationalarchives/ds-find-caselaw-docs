# 10. Interface with Enrichment

Date: 2022-09-20

## Status

Accepted

## Context

We had a meeting on the morning of 20th September to discuss how the Enrichment service would know what documents it needed
to enrich, how it'd get them and how it'd send them back.

## Decision

* Find Case Law (dxw) will place a notification onto an SNS queue that it manages when an enrichment is required.
* That notification will contain the public URL of a document to be enriched, using an initial JSON format something like `{"uri":"ewhc/tcc/2022/2348", "host": "api.caselaw.nationalarchives.gov.uk"}` (possibly embedded in some SNS-specific structure)
* Enrichment Engine will subscribe to the SNS notifications, and upon receipt, execute a Lambda function that will use the Case Law privileged API to fetch the XML document, and lock it for editing
* Enrichment Engine will submit the completed XML document using the PATCH endpoint , setting unlock to true to release the lock, and setting the annotation parameter to 'enriched'.

