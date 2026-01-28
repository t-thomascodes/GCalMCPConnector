from datetime import datetime, timedelta
import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from dateutil.parser import isoparse
from googleapiclient.discovery import build


# Scopes for read/write access
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Paths
CLIENT_SECRET_FILE = os.environ["GOOGLE_CLIENT_SECRET_FILE"]
TOKEN_DIR = Path(".auth")
TOKEN_FILE = TOKEN_DIR / "gcal_token.json"


def get_creds():
    creds = None
    TOKEN_DIR.mkdir(exist_ok=True)

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def create_test_event():
    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)

    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(minutes=60)

    event = {
        "summary": "Test event from MCP prototype2",
        "description": "Created by Python via Google Calendar API.",
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "America/New_York"
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "America/New_York"
        },
    }

    created = service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="all"
    ).execute()

    print("Created:", created.get("htmlLink"))


allevents = []



EASTERN_TZ = ZoneInfo("America/New_York")

def _parse_to_eastern(dt_str: str) -> datetime:
    """
    Converts Google Calendar date/dateTime strings into
    timezone-aware datetimes in America/New_York.
    """
    dt = isoparse(dt_str)

    if dt.tzinfo is None:
        # All-day event (YYYY-MM-DD)
        # Interpret as local midnight Eastern Time
        dt = datetime(
            dt.year, dt.month, dt.day,
            tzinfo=EASTERN_TZ
        )
    else:
        # Timed event, convert to Eastern
        dt = dt.astimezone(EASTERN_TZ)

    return dt


def list_events_next_7_days(cal_id):
    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)

    now_utc = datetime.now(timezone.utc)
    end_utc = now_utc + timedelta(days=7)

    events_result = service.events().list(
        calendarId=cal_id,
        timeMin=now_utc.isoformat(),
        timeMax=end_utc.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=2500
    ).execute()

    for ev in events_result.get("items", []):
        start = ev.get("start", {})
        end_ = ev.get("end", {})

        start_raw = start.get("dateTime") or start.get("date")
        end_raw = end_.get("dateTime") or end_.get("date")

        start_dt = _parse_to_eastern(start_raw)
        end_dt = _parse_to_eastern(end_raw)

        allevents.append({
            "calendar_id": cal_id,
            "summary": ev.get("summary", "(no title)"),
            "start": start_dt,
            "end": end_dt,
            "all_day": "date" in start and "date" in end_,
        })




if __name__ == "__main__":
    list_events_next_7_days("primary")
    list_events_next_7_days("x")

    sorted_events = sorted(allevents, key=lambda e: e["start"])

    for e in sorted_events:
        print(
            f"{e['start'].isoformat()} → {e['end'].isoformat()} | "
            f"{e['summary']} ({e['calendar_id']})"
        )



