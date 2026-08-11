# Runbook: MarkLogic Incident Response

Use this runbook when MarkLogic shows signs of degradation: high CPU, long-running requests, stuck evals, or timeout errors in Rollbar/alerts.

> **Prerequisites:** Access to MarkLogic admin and monitoring interfaces, your log platform, and AWS CloudWatch.

## Assumptions

- You are operating in the correct environment and handling all times in UTC.
- You have credentials for the MarkLogic Manage API.
- Environment-specific timeout values are maintained in internal operational documentation.

## Preflight

Before triage, confirm:

- incident window (UTC start time, latest observed impact, current time);
- required tools available locally (`curl`, `jq`);
- secure handling for credentials (`ML_USER`, `ML_PASSWORD`, `ML_HOST`).

If `jq` is unavailable, continue investigation through MarkLogic admin/monitoring interfaces and log platform views.

---

## 1) Trigger signals

- Dalmatian/CloudWatch CPU alarm for MarkLogic host
- Rollbar read timeout errors
- MarkLogic Monitoring Dashboard shows long-running `module=eval` requests (time increasing)
- User-facing 500/504 errors on search or document pages

---

## 2) Immediate triage

### Check active long-running requests via Manage API

```bash
curl -sS --digest -u "$ML_USER:$ML_PASSWORD" \
  -H "Accept: application/json" \
  "$ML_HOST:8002/manage/v2/requests?view=default&format=json" \
  -o /tmp/ml-requests.json

jq empty /tmp/ml-requests.json
```

Count active eval requests:

```bash
jq '[.. | objects | select(.module?=="eval")] | length' /tmp/ml-requests.json
```

List active eval requests:

```bash
jq -r '.. | objects | select(.module?=="eval")
  | [.["request-id"], .host?, .server?, .["start-time"]?, .time?]
  | @tsv' /tmp/ml-requests.json
```

Total active requests:

```bash
jq '[.. | objects | select(has("request-id"))] | length' /tmp/ml-requests.json
```

Record UTC timestamps for each command/query execution in the incident timeline.

### Check App Server Status (Admin Console)

Navigate to the App Server Status view in the MarkLogic Admin Console for the affected host and app server group.

Look for requests with status `running` or `cancelling` and high elapsed time.

### Capture snapshot for each stuck request

| request-id | host | app server | module | status | start time | elapsed |
| ---------- | ---- | ---------- | ------ | ------ | ---------- | ------- |
|            |      |            | eval   |        |            |         |

---

## 3) Correlate with application alerts

- Check Rollbar for `ReadTimeout` errors — note exact timestamps
- Cross-reference with MarkLogic CPU alarm timestamps
- Check ECS Container Insights for PUI CPU spike (EUI spike = different cause)
- Check SolarWinds logs:
  - `8011_RequestLog.txt` — request lifecycle and duration (best source)
  - `8011_AccessLog.txt` — endpoint and client context
  - `ErrorLog.txt` — lock, memory, or system-level errors

---

## 4) Understanding the timeout mismatch

The application read timeout can fire before MarkLogic stops processing. This does **not** cancel the MarkLogic request. MarkLogic continues executing until:

- it completes naturally
- it hits its own app server timeout
- it is manually cancelled

This means requests can pile up and keep CPU elevated long after user-facing errors resolve.

---

## 5) Containment: cancelling stuck requests

### Normal cancel

From the Admin Console App Server Status page, select the request and cancel.

### Force-delete requests stuck in `cancelling`

If requests remain in `cancelling` indefinitely, follow the MarkLogic force-cancel procedure:

- [MarkLogic docs: Canceling a Request](https://docs.progress.com/bundle/marklogic-server-administrate-10/page/topics/http-servers/canceling-a-request.html)

Record all cancelled request-ids and timestamps.

After cancellation, re-check active request counts and error rates before proceeding.

---

## 6) Recovery verification

- [ ] Requests no longer visible in App Server Status
- [ ] MarkLogic CPU returns to baseline
- [ ] Rollbar timeout alerts stop for 15–30 min
- [ ] User-facing checks pass

---

## 7) Escalation to MarkLogic support

Escalate if:

- Requests repeatedly stuck in `cancelling`
- Requests hang despite configured timeouts
- Evidence of lock/deadlock or internal task non-termination

Include in support ticket:

- request-ids, host-id, app server id
- timestamps (UTC), logs around start and cancel attempt
- screenshots of App Server Status
- current timeout configuration values

---

## 8) Timeout configuration

MarkLogic app server timeout should be set **slightly lower** than the application read timeout so MarkLogic exits cleanly before the client gives up.

Use the team-owned internal operations source of truth for the current values in each environment.

| Layer                                | Recommended value                                                        |
| ------------------------------------ | ------------------------------------------------------------------------ |
| Application read timeout             | `<app_read_timeout>`                                                     |
| MarkLogic app server request timeout | `<marklogic_request_timeout>` (set slightly lower than app read timeout) |

## 9) Decision Guide

- If request count is high but draining and user impact is improving:
  - continue monitoring and avoid unnecessary manual cancellation.
- If long-running requests are accumulating and user impact continues:
  - proceed with cancellation and containment.
- If requests remain stuck in `cancelling` or repeatedly recur:
  - escalate to MarkLogic support with collected evidence.
- If evidence points to upstream traffic abuse rather than MarkLogic-only degradation:
  - hand off to traffic runbook investigation.

---

## 10) Incident record template

**Incident ID:**
**Date/Time (UTC):**
**Responder(s):**
**Environment:** prod / staging

**Trigger:**

- [ ] Rollbar timeout alert
- [ ] CPU alarm
- [ ] Long-running eval on dashboard
- [ ] User impact confirmed

**Alert links:**

- Rollbar:
- CloudWatch/Dalmatian:
- MarkLogic Monitoring:

**Requests captured:**

| request-id | host | app server | status | start time | elapsed |
| ---------- | ---- | ---------- | ------ | ---------- | ------- |

## **Actions taken (with timestamps):**

**Recovery confirmed at:**

**Root cause:**

**Follow-up tickets:**
