# ticket_status_lookup

Look up the status, assignee, and priority of an existing IT support ticket by its ticket ID.

## Capabilities

- Queries the local `tickets.json` store.
- Returns details such as `status`, `summary`, `priority`, and `assignee`.

## Limitations

- Cannot search by user or keyword; requires a specific `ticket_id` (e.g., "TKT-101").
- Does not modify ticket status; this is a read-only tool.

## Input

| Argument | Type | Description |
|---|---|---|
| `ticket_id` | string | The ID of the ticket to lookup, e.g., "TKT-101". |

## Error handling

- Returns `missing_ticket_id` if the argument is empty.
- Returns `not_found` if the ticket ID does not exist in the database.
