---
name: format_incident_report
track: core
kind: local_formatter
requires_env: []
inputs: [findings, template, incident_title]
outputs: [template, markdown, finding_count]
side_effect: false
---
# format_incident_report

Formats findings already collected by other tools. It does not inspect devices,
check service status, search knowledge/policy/the public web, or create tickets.
Each model-provided finding must contain a short `label` and factual `detail`.
Use the requested `brief`, `technical`, or `handoff` template and preserve the
current incident title. When the user requests formatting only, do not re-fetch
evidence.
