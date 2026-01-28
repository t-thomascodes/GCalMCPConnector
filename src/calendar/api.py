"""Google Calendar API functions."""
import os
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse

from googleapiclient.discovery import build

from .auth import get_creds
from .utils import EASTERN_TZ, parse_to_eastern


def fetch_events(cal_id: str, time_start: str, time_end: str) -> list[dict]:
    """Fetch events from a calendar within a time range."""
    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)

    start_dt = isoparse(time_start)
    end_dt = isoparse(time_end)

    # Convert to UTC if they have timezone info, otherwise assume UTC
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    else:
        start_dt = start_dt.astimezone(timezone.utc)
    
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    else:
        end_dt = end_dt.astimezone(timezone.utc)

    events_result = service.events().list(
        calendarId=cal_id,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=2500
    ).execute()

    events = []
    for ev in events_result.get("items", []):
        start = ev.get("start", {})
        end_ = ev.get("end", {})

        start_raw = start.get("dateTime") or start.get("date")
        end_raw = end_.get("dateTime") or end_.get("date")

        events.append({
            "calendar_id": cal_id,
            "event_id": ev.get("id"),
            "summary": ev.get("summary", "(no title)"),
            "start": parse_to_eastern(start_raw),
            "end": parse_to_eastern(end_raw),
            "all_day": "date" in start and "date" in end_,
        })

    return events


def create_event(
    title: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    calendar_id: str = "primary",
    send_updates: str = "all"
) -> dict:
    """Create a new calendar event."""
    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_date.isoformat(),
            "timeZone": "America/New_York"
        },
        "end": {
            "dateTime": end_date.isoformat(),
            "timeZone": "America/New_York"
        },
    }

    created = service.events().insert(
        calendarId=calendar_id,
        body=event,
        sendUpdates=send_updates
    ).execute()
    
    return created


def delete_event(
    event_id: str,
    calendar_id: str = "primary",
    send_updates: str = "all"
) -> None:
    """Delete a calendar event by ID."""
    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)
    service.events().delete(
        calendarId=calendar_id,
        eventId=event_id,
        sendUpdates=send_updates
    ).execute()


def delete_event_by_title_and_date(
    title: str,
    date: str,
    send_updates: str = "all"
) -> dict:
    """Find and delete event(s) by title and date."""
    # Parse date and determine search window
    date_dt = isoparse(date)
    if date_dt.tzinfo is None:
        date_dt = date_dt.replace(tzinfo=EASTERN_TZ)
    else:
        date_dt = date_dt.astimezone(EASTERN_TZ)
    
    # Determine if date-only or datetime
    is_date_only = "T" not in date.upper() or (date_dt.hour == 0 and date_dt.minute == 0)
    
    # Set search window
    if is_date_only:
        time_start = datetime(date_dt.year, date_dt.month, date_dt.day, tzinfo=EASTERN_TZ).isoformat()
        time_end = datetime(date_dt.year, date_dt.month, date_dt.day, 23, 59, 59, tzinfo=EASTERN_TZ).isoformat()
    else:
        time_start = (date_dt - timedelta(minutes=30)).isoformat()
        time_end = (date_dt + timedelta(minutes=30)).isoformat()
    
    # Get calendars to search
    cal_ids = [
        os.environ.get("GCAL_PRIMARY_ID", "primary"),
        os.environ.get("GCAL_SECONDARY_ID", "primary"),
    ]
    cal_ids = list(dict.fromkeys(cal_ids))  # remove duplicates
    
    # Fetch events using existing function
    all_events = []
    for cal_id in cal_ids:
        all_events.extend(fetch_events(cal_id, time_start, time_end))
    
    # Find matches
    matches = []
    for event in all_events:
        if title.lower() in event["summary"].lower():
            if is_date_only:
                if event["start"].date() == date_dt.date():
                    matches.append(event)
            else:
                if abs((event["start"] - date_dt).total_seconds()) <= 1800:
                    matches.append(event)
    
    if not matches:
        raise ValueError(f"No events found matching '{title}' on {date}")
    
    # Delete matches
    deleted = []
    for event in matches:
        delete_event(event["event_id"], event["calendar_id"], send_updates)
        deleted.append({"title": event["summary"], "start": event["start"].isoformat()})
    
    return {
        "status": "success",
        "message": f"Deleted {len(deleted)} event(s)",
        "deleted": deleted
    }
