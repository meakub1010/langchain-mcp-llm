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
def reschedule_appointment(event_id: int, new_start_time: str, duration_minutes: int = 30):
    try:
        start = datetime.fromisoformat(new_start_time)
        end = start + timedelta(minutes=duration_minutes)
    except ValueError as e:
        return {"re-scheduled": False, "error": str(e)}

    try:
        calendar = get_calendar_service()
        result = calendar.events().patch(
            calendarId="primary",
            eventId=event_id,
            body={
                "start": {"dateTime": start.isoformat(), "timeZone": "America/New_York"},
                "end": {"dateTime": end.isoformat(), "timeZone": "America/New_York"},
            },
            sendUpdates="all",
        ).execute()
    except Exception as e:
        return {"re-scheduled": False, "error": str(e)}

    return {"re-scheduled": True, "event_id": result["id"], "new_start_time": start.isoformat(), "event_link": result["htmlLink"]}
def cancel_appointment(event_id:str):
    try:
        calendar = get_calendar_service()
        calendar.events().delete(calendarId="primary", eventId=event_id, sendUpdates="all").execute()
    except Exception as e:
        return {"cancelled": False, "error": str(e)}

    return {"cancelled": True, "event_id": event_id}

def find_appointments(query: str, days_ahead: int = 60) -> dict:
    try:
        calendar = get_calendar_service()
        now_dt = datetime.utcnow()
        later_dt = now_dt + timedelta(days=days_ahead)
        now = now_dt.isoformat() + "Z"
        later = later_dt.isoformat() + "Z"

        result = calendar.events().list(
            calendarId="primary",
            q=query,
            timeMin=now,
            timeMax=later,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
    except Exception as e:
        return {"Found": False, "error": str(e)}

    events = [
        {
            "event_id": e["id"],
            "summary": e["summary"],
            "start_time": e.get("start", {}).get("dateTime"),
        }
        for e in result.get("items", [])
    ]

    return {"found": len(events) > 0, "events": events}
