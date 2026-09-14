---
name: inspect_device
track: core
kind: local_inventory
provider: mock_device_inventory
requires_env: []
inputs: [asset_id, check]
outputs: [asset_id, check, device, diagnostics, snapshot_at]
side_effect: false
---
# inspect_device

Looks up one company asset and returns its stored diagnostic snapshot. A valid
explicit asset ID is required; never infer it from a person's name, department,
device type, or another record. Supported checks are `all`, `network`, `vpn`,
`security`, `hardware`, and `software`. This tool does not read shared-service
status and does not send internal data to public search. Use `clarify` when the
asset ID is absent or ambiguous.
