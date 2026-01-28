"""Google Calendar authentication and credentials management."""
import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CLIENT_SECRET_FILE = os.environ["GOOGLE_CLIENT_SECRET_FILE"]
TOKEN_DIR = Path("/tmp/.auth")
TOKEN_FILE = TOKEN_DIR / "gcal_token.json"


def get_creds() -> Credentials:
    """Get or refresh Google Calendar API credentials."""
    TOKEN_DIR.mkdir(exist_ok=True)
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())

    return creds
