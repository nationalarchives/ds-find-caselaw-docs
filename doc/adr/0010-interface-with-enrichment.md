# 10. Interface with Enrichment

Date: 2022-09-20

## Status

Accepted

## Context

We had a meeting on the morning of 20th September to discuss how the Enrichment service would know what documents it needed to enrich, how it'd get them and how it'd send them back. We then further refined this and
[built a prototype](https://github.com/nationalarchives/ds-caselaw-editor-ui/pull/392)
and presented our decisions to a meeting on the 27th September.

## Decision

- Find Case Law (dxw) will place a notification onto an SNS topic that it manages when an document is edited. If there is a need to be able to retry the lambda, it is possible for Enrichment to subscribe an SQS queue to the topic so they have visibility and control.
- That notification will contain a JSON dictionary, with at least the following keys:

  - `uri_reference`: the document that is being notified about, e.g. `ewhc/fam/2022/2134`, which can be appended to API endpoints like `api.caselaw.nationalarchives.gov.uk/lock/ewhc/fam/2022/2134`
  - `status`: currently the status of the document when edited: `published` implies the document has previously or just now been published; `not published` implies the document has never been published or has been unpublished.
    In total this may look like: `{"uri_reference": "ewhc/fam/2022/2134", "status": "published"}`

- Earlier versions of this document suggested there would be a `host` key. Given the editor does not know the URI of
  the API, we recommend the enrichment engine is explicitly told the correct API to use.

- The value of the `status` key is also available as an `update_type` MessageAttribute.
- There is also a string MessageAttribute of `trigger_enrichment` which will be `1` if enrichment is desired, and absent if enrichment is not desired, allowing more explicit control of enrichment.

- The staging SNS is at arn:aws:sns:eu-west-2:626206937213:caselaw-stg-judgment-updated
- The staging API is at https://api.staging.caselaw.nationalarchives.gov.uk/
- There is currently no production SNS but it will be at a different numerical account (and not have -stg)
- The production API is at https://api.caselaw.nationalarchives.gov.uk/

- Enrichment Engine will subscribe to (a subset of) the SNS notifications, and upon receipt, execute a Lambda function that will use the Case Law privileged API to fetch the XML document, and lock it for editing
- Enrichment Engine will submit the completed XML document using the PATCH endpoint , setting `?unlock=1` to release the lock, and setting the annotation parameter to `enriched`.
