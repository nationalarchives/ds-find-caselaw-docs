# Observability and Monitoring Guide

Top-level reference for where to find logs, metrics, alerts, and incident investigation paths across the caselaw platform.

## Scope

This guide covers:

- PUI web application (ECS service)
- EUI web application (ECS service)
- Ingest/ingester (Lambda)
- Document cleansing process (CloudWatch logs)
- PDF generator process (ECS task with CloudWatch logs)
- MarkLogic platform and app servers
- Edge and traffic controls (WAF, ALB)

## Assumptions

- Responders have read access to AWS accounts, log platforms, and alerting channels.
- Environment-specific values are maintained in internal operational documentation.
- All times are handled in UTC during incident response.

## Service Signal Map

| Component                | Primary logs                                     | Metrics and health                                        | Errors and alerting                       |
| ------------------------ | ------------------------------------------------ | --------------------------------------------------------- | ----------------------------------------- |
| PUI web app              | App logs (central log platform), CloudWatch logs | ECS Container Insights, service health                    | Rollbar, team alerting channel(s)         |
| EUI web app              | App logs (central log platform), CloudWatch logs | ECS Container Insights, service health                    | Rollbar, team alerting channel(s)         |
| Ingest/ingester (Lambda) | CloudWatch logs                                  | Lambda metrics (invocations, duration, errors, throttles) | Rollbar, CloudWatch alarms                |
| Document cleansing       | CloudWatch logs                                  | Process/job-level CloudWatch metrics where configured     | Rollbar, CloudWatch alarms                |
| PDF generator (ECS task) | CloudWatch logs                                  | ECS task health and task-level metrics                    | Rollbar, CloudWatch alarms                |
| MarkLogic                | App server and error logs (central log platform) | MarkLogic monitoring/admin views, host CPU                | Rollbar timeouts, CloudWatch alarms       |
| WAF and ALB              | WAF logs, ALB access logs                        | WAF traffic overview, ALB target metrics                  | CloudWatch alarms and alerting channel(s) |

## Key Dashboards and Consoles

| Surface                       | Where to look                                  | Use for                                            |
| ----------------------------- | ---------------------------------------------- | -------------------------------------------------- |
| CloudWatch Logs Insights      | AWS Console -> CloudWatch -> Logs Insights     | Ad-hoc queries and timeline correlation            |
| CloudWatch Metrics and Alarms | AWS Console -> CloudWatch -> Metrics/Alarms    | Validate trigger conditions and incident window    |
| ECS Service Health            | AWS Console -> ECS -> service/task views       | CPU, memory, running tasks, task restarts          |
| Lambda Monitoring             | AWS Console -> Lambda -> function monitoring   | Error rates, throttles, duration spikes            |
| WAF Web ACL                   | AWS Console -> WAF -> Web ACLs                 | Edge traffic patterns, sampled requests            |
| MarkLogic Monitoring/Admin    | Internal MarkLogic monitoring/admin interfaces | Active requests, request cancellation, host health |
| Rollbar                       | Rollbar project views                          | Exception timelines and fingerprints               |

## Baselines and Threshold Ownership

Public runbooks intentionally omit exact operational thresholds and identifiers.

Before acting on incidents, confirm the current environment values for:

- traffic and burst thresholds;
- rate-limit rule identifiers;
- service scaling minima/maxima;
- timeout settings per component.

Use the team-owned internal operations source of truth for these values.

## Incident Response Workflow

1. Confirm incident window in UTC and record start time.
2. Identify impacted component(s) from alerts and user impact reports.
3. Pull correlated evidence from logs, metrics, and Rollbar for the same time window.
4. Follow the component-specific runbook for deep investigation and containment.
5. Verify recovery with service health and user-facing checks.
6. Record timeline, actions, and follow-up items.

## Component-Specific Runbooks

- Traffic anomalies and bot patterns: [Traffic Spike and Bot Investigation](./traffic-spike-bot-investigation.md)
- MarkLogic degradation and stuck requests: [MarkLogic Incident Response](./marklogic-incident-response.md)

## Coverage Gaps and Escalation

If a component is impacted and no dedicated runbook exists yet:

1. Use this guide to gather logs/metrics/alerts for the affected component.
2. Open an incident ticket with captured evidence and UTC timeline.
3. Escalate to the owning engineering team.
4. Create or update a dedicated runbook as a post-incident action.
