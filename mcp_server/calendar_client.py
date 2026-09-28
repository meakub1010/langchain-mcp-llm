import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = Path("token.pickle")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def get_calendar_service():
    with open("token.pickle", "rb") as f:
         creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open("token.pickle", "wb") as f:
                pickle.dump(creds, f)
        else:
            raise RuntimeError(
                "Stored google credentials are invalid. re-run the script"
            )
    return build("calendar", "v3", credentials=creds)

