---
name: check_service_status
track: core
kind: local_status
provider: mock_status_page
requires_env: []
inputs: [service, environment]
outputs: [service, environment, status, incident, checked_at]
side_effect: false
---
# check_service_status

Reads the deterministic mock status page for a named shared service and
environment. It is for organization-wide VPN, email, SSO, Wi-Fi, or printing
state; it does not diagnose a single employee device or return troubleshooting
instructions. Both `service` and the exact `production`/`staging` environment
must be present in the model call. Ask a clarification question for any other or
ambiguous environment.
