# 16. Notes

Date: 2023-09-27

## Status

Provisional

## Context

We want a log of events including notes from human and machine events.

## Decision

Whilst the log might contain other events (e.g. publication of new versions, enrichment times, etc.) a
core aspect is recording notes.

These should be placed in the Marklogic Properties and be a single tag with nested tags, eg.

<notes>
  <note time="2022-02-02T02:02:02Z" source="human" author="dragon" type="on hold">Judgment has typo</note>
  <note time="2022-01-01T01:01:01Z" source="machine" author="ingester" type="new judgment">Judgment TDR-2023-RFT uploaded</note>
</notes>

Notes should be added to the end of this list; should identify whether they're human-written or machine-written, have timestamps, help us understand what person or machine wrote the message, allow a machine-readable categorisation of messages, and has writable text.

Editors will be able to add notes via the Editor UI

## Consequences

We should be able to track the lifecycle of a document
