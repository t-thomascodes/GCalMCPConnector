"""Calendar utility functions for timezone handling."""
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil.parser import isoparse

EASTERN_TZ = ZoneInfo("America/New_York")


def parse_to_eastern(dt_str: str) -> datetime:
    """Parse ISO datetime string and convert to Eastern timezone."""
    dt = isoparse(dt_str)

    if dt.tzinfo is None:
        return datetime(dt.year, dt.month, dt.day, tzinfo=EASTERN_TZ)

    return dt.astimezone(EASTERN_TZ)
