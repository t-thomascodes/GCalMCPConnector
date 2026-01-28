"""MCP server entry point for Google Calendar integration."""
from mcp.server.fastmcp import FastMCP
from dateutil.parser import isoparse

from src.calendar import create_event, delete_event_by_title_and_date
from src.mcp import list_events_across_calendars

mcp = FastMCP("CalIntegration", json_response=True)


@mcp.tool()
def list_events_in_time_frame(time_start: str, time_end: str) -> dict:
    """
    List all events across configured calendars from time_start to time_end.
    Returns JSON only.

    User Timezone: Eastern Time (America/New_York)
    - Eastern Standard Time (EST): UTC-5
    - Eastern Daylight Time (EDT): UTC-4

    Time Format: Use ISO 8601 format with timezone offset
    - Format: YYYY-MM-DDTHH:MM:SS-05:00 (EST) or YYYY-MM-DDTHH:MM:SS-04:00 (EDT)
    - Examples:
    - Start of day: 2026-01-28T00:00:00-05:00
    - End of day: 2026-01-28T23:59:59-05:00

    Note: If specific times are not provided, queries should default to:
    - start: beginning of start_date (00:00:00) with appropriate timezone offset
    - end: end of end_date (23:59:59) with appropriate timezone offset
    This ensures all events within the date range are captured in the user's local timezone.
    """
    return list_events_across_calendars(time_start=time_start, time_end=time_end)


@mcp.tool()
def create_event_tool(title: str, description: str, start: str, end: str) -> dict:
    """
    Create an event based on the title, description, start, and end provided.
    Start and end should be ISO format datetime strings (e.g., "2026-01-28T10:00:00-05:00").
    """
    start_dt = isoparse(start)
    end_dt = isoparse(end)
    
    create_event(title, description, start_dt, end_dt)
    
    return {
        "status": "success",
        "message": f"Event '{title}' created successfully",
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat()
    }


@mcp.tool()
def delete_event(title: str, date: str) -> dict:
    """
    Delete an event by title and date.
    Searches for events matching the title on the given date and deletes them.
    
    Args:
        title: Event title (case-insensitive partial match)
        date: Date in ISO format - "2026-01-28" or "2026-01-28T10:00:00-05:00"
    """
    return delete_event_by_title_and_date(title, date)


if __name__ == "__main__":
    # Use the same transport you plan to use with Claude.
    # If Claude expects stdio, use default: mcp.run()
    mcp.run()
