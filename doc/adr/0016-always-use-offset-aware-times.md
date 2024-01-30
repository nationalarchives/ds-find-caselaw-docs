# 16. Always use offset-aware times

Date: 2024-01-30

## Status

Accepted

## Context

We are not always storing dates and times in a way which conveys timezone offset information. This can introduce unexpected behaviours, especially with developers in other timezones and around daylight savings time, both in information storage, querying and display.

## Decision

Whenever writing a datetime or providing it in a machine-readable way (for example via the API or embedded in XML), include timezone offset information (for example `datetime.datetime.now(datetime.timezone.utc)`).

Whenever reading a datetime, do so in a way which correctly provides and parses timezone offset information.

Whenever displaying a datetime, either do so in a timezone-aware context or explicitly include offset information (eg when displaying dates for debugging purposes). This may either be an assumed timezone (eg it's not unreasonable to assume service users are in `Europe/London`), or the user's local timezone.

## Consequences

- Downstream content reusers may need to modify their datetime handling to account for the extra information.
- We may need to modify some queries against MarkLogic so they explicitly ask for datetimes in UTC, rather than the server's [implicit timezone](https://help.marklogic.com/Knowledgebase/Article/View/227/0).
