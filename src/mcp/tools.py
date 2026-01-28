"""MCP tool helper functions."""
import os
from ..calendar import fetch_events


def list_events_across_calendars(time_start: str, time_end: str) -> dict:
    """List events across all configured calendars."""
    cal_ids = [
        os.environ.get("GCAL_PRIMARY_ID", "primary"),
        os.environ.get("GCAL_SECONDARY_ID", "primary"),
    ]
    # Remove duplicates while preserving order
    cal_ids = list(dict.fromkeys(cal_ids))

    all_events = []
    for cal_id in cal_ids:
        all_events.extend(fetch_events(cal_id, time_start, time_end))

    all_events.sort(key=lambda e: e["start"])

    return {
        "events": [
            {
                "calendar": e["calendar_id"],
                "summary": e["summary"],
                "start": e["start"].isoformat(),
                "end": e["end"].isoformat(),
                "all_day": e["all_day"],
                "event_id": e["event_id"]
            }
            for e in all_events
        ]
    }
