from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools._shared import err

DATA_FILE = Path(__file__).parent.parent.parent / "helpdesk_data" / "tickets.json"

def ticket_status_lookup(ticket_id: str = "") -> dict[str, Any]:
    if not isinstance(ticket_id, str):
        return err("ticket_status_lookup", "invalid_ticket_id_type")
    
    tid = ticket_id.strip().upper()
    if not tid:
        return {"tool": "ticket_status_lookup", "error": "missing_ticket_id"}

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return err("ticket_status_lookup", "data_file_not_found")
    except json.JSONDecodeError:
        return err("ticket_status_lookup", "data_file_invalid")

    for ticket in data:
        if ticket.get("ticket_id") == tid:
            return {
                "tool": "ticket_status_lookup",
                "ticket_id": tid,
                "status": ticket.get("status"),
                "summary": ticket.get("summary"),
                "priority": ticket.get("priority"),
                "assignee": ticket.get("assignee"),
                "created_at": ticket.get("created_at"),
            }

    return {"tool": "ticket_status_lookup", "error": "not_found"}
