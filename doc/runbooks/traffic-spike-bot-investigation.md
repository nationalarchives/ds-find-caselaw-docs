# Traffic Spike and Bot Investigation (WAF Logs Insights)

Use this runbook when traffic volume spikes unexpectedly and you need to quickly determine whether the cause is legitimate demand, bot activity, or malicious probing.

These queries are designed to help you:

- identify top request sources;
- detect burst traffic patterns;
- spot clients attempting to evade rate limits;
- find indicators of coordinated bot behavior; and
- review how WAF managed rules are being triggered.

## Assumptions

This public runbook assumes:

- WAF logging is enabled and accessible to the responder.
- You are running queries against the correct environment-specific WAF log group.
- Environment-specific values (for example thresholds, rule IDs, and log destination names) are maintained separately in internal operational documentation.

## Important Limitation

WAF logging was not enabled during the July 2026 incident. These queries only work when WAF logs are available.

## Prerequisites

- WAF logging must be enabled.
- Logs must be sent to your configured WAF log destination.
- Open CloudWatch Logs Insights and select the relevant WAF log group before running queries.

## Preflight

Before running queries, confirm:

- incident time window in UTC (start time, latest observed impact, current time);
- impacted environment;
- required read access to CloudWatch Logs Insights and WAF views;
- where to retrieve internal values for placeholders used in this runbook.

## Internal Values Required

This public runbook uses placeholders. Retrieve current environment values from the team-owned internal operations source of truth before relying on threshold-based interpretation.

Required values include:

- `<burst_threshold>`
- `<lower_bound>` and `<upper_bound>`
- `<window_count_threshold>`
- `<min_rotating_ips>`
- `<your-rate-limit-rule-id>`

## Investigation Sequence

Run the queries in this order:

1. Top request contributors (Section 1)
2. Burst behavior (Section 2)
3. Near-threshold repeat traffic (Section 3)
4. JA3-based rotation patterns (Section 4)
5. Malicious payload indicators (Section 5)
6. Rule match context (Sections 6 and 7)

Capture notable findings with timestamp, IP/JA3, path, and query used.

## 1. Top IPs by Total Requests

Start here for an initial high-level view of which clients are generating the most traffic.

```sql
fields httpRequest.clientIp as ip
| stats count() as total_req, count_distinct(httpRequest.uri) as unique_paths by ip
| sort total_req desc
| limit 50
```

## 2. Burst Offenders (Max and Average per 5 Minutes)

Use this to find clients producing short, intense request bursts.

```sql
fields httpRequest.clientIp as ip
| stats count() as req_per_5m by bin(5m) as t, ip
| stats max(req_per_5m) as max_burst, avg(req_per_5m) as avg_per_5m, count() as total_windows by ip
| filter max_burst >= <burst_threshold>
| sort max_burst desc
| limit 50
```

## 3. Rate-Limit Evaders (Consistently Just Under Limit)

This highlights clients that repeatedly sit below blocking thresholds, which can indicate deliberate evasion.

```sql
fields httpRequest.clientIp as ip
| stats count() as req_per_5m by bin(5m) as t, ip
| filter req_per_5m >= <lower_bound> and req_per_5m <= <upper_bound>
| stats count() as consistent_windows by ip
| filter consistent_windows >= <window_count_threshold>
| sort consistent_windows desc
| limit 50
```

## 4. IP-Rotating Bots via JA3 Fingerprint

Use JA3 to identify possible bot clusters that rotate source IPs while keeping similar TLS client fingerprints.

```sql
fields httpRequest.clientIp as ip, ja3Fingerprint as ja3
| stats count() as req, count_distinct(ip) as unique_ips by ja3
| filter unique_ips >= <min_rotating_ips>
| sort unique_ips desc
| limit 50
```

## 5. SQL Injection Probe Detection

This query looks for common SQLi-like patterns in query strings.

```sql
fields httpRequest.clientIp as ip, httpRequest.uri as path, httpRequest.args as qs
| filter qs like /(?i)(union|select|concat|%27|--|%23)/
| stats count() as hits by ip, path
| sort hits desc
| limit 100
```

## 6. Managed Rules Triggered in Count Mode

Use this to understand which managed rules are matching when configured in `COUNT` mode.

```sql
fields terminatingRuleId, action
| filter action = "COUNT"
| stats count() as matched by terminatingRuleId
| sort matched desc
```

## 7. IPs Hitting the Rate-Limit Block Rule

Use this to identify who is being blocked by the rate-limiting rule and which paths are most affected.

```sql
fields httpRequest.clientIp as ip, httpRequest.uri as path, terminatingRuleId
| filter terminatingRuleId = "<your-rate-limit-rule-id>"
| stats count() as blocks by ip, path
| sort blocks desc
| limit 50
```

## Decision and Next Actions

Use the following guide to decide what to do next:

- If top contributors are diverse and patterns look organic, continue monitoring and check backend capacity/performance runbooks.
- If one or more sources show sustained bursts or threshold evasion patterns, escalate to the owning platform/security responder and apply environment-specific mitigation from the team-owned internal operations source of truth.
- If SQLi or scanner-style activity is observed, escalate as a potential security event, preserve evidence, and request security review.
- If WAF data is unavailable, use ALB/access logs and application logs for interim triage, then log the observability gap in the incident record.

## Containment Checklist

- [ ] Potential abusive sources identified and recorded.
- [ ] Mitigation decision approved by incident lead/on-call owner.
- [ ] Mitigation applied using internal procedures.
- [ ] Impact monitored for regression (errors, latency, service health).
- [ ] Security escalation raised when malicious probing is indicated.

## Recovery and Closure Criteria

Only close this runbook activity when all apply:

- [ ] Request rate returns to expected baseline for the period.
- [ ] Error rates stabilize.
- [ ] No ongoing burst/evasion pattern in repeated checks.
- [ ] User-facing impact has cleared.
- [ ] Incident timeline and evidence have been recorded.

## Incident Record Minimum Data

- incident ID
- UTC timeline of key events
- impacted services and user impact summary
- top offending IPs/JA3 fingerprints and paths
- mitigation actions taken
- outcome and follow-up actions
