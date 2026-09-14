---
name: lookup_user
track: core
kind: local_directory
provider: mock_employee_directory
requires_env: []
inputs: [employee_id]
outputs: [employee, snapshot_at]
side_effect: false
---
# lookup_user

Looks up one fictional employee by employee ID and returns support-safe work
metadata. Assigned asset IDs are inside the returned `employee` object, not a
separate top-level field. Use only an explicit `EMP-...` identifier; do not
guess an employee from a name, team, or department. It never returns
credentials or secrets, and a missing identifier must be handled with
`clarify`.
