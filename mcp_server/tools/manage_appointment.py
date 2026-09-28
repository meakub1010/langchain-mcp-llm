from datetime import datetime, timedelta

from mcp_server.calendar_client import get_calendar_service


def create_appointment(event_name: str, start_time: str, duration_minutes: int = 30):
    if "T" not in start_time:
        return {
            "created": False,
            "error": "start_time must include a specific time, not just a date "
                     "(e.g. '2026-12-11T14:00:00', not '2026-12-11'). Please ask the user for a time."
        }
    try:
        start = datetime.fromisoformat(start_time)
        end = start + timedelta(minutes=duration_minutes)
    except ValueError as e:
        return {"created": False, "error": str(e)}

    event = {
        "summary": event_name,
        "start": {"dateTime": start.isoformat(), "timeZone": "America/New_York"},
        "end": {"dateTime": end.isoformat(), "timeZone": "America/New_York"},
    }

    try:
        calendar = get_calendar_service()
        result = calendar.events().insert(calendarId="primary", body=event, sendUpdates="all").execute()
    except Exception as e:
        return {"created": False, "error": str(e)}
    print(f"result: \n {result} \n\n")
    return {
        "created": True,
        "event_id": result["id"],
        "event_link": result.get("htmlLink"),
        "start_time": start.isoformat(),
    }
def reschedule_appointment():
    pass
def cancel_appointment():
    pass