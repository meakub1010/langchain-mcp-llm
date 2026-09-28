# from mcp_server.calendar_client import get_calendar_service
# from datetime import datetime, timedelta
#
# service = get_calendar_service()
#
#
# # start = datetime.now() + timedelta(hours=1)
# # end = start + timedelta(minutes=30)
#
#
# # specific date and time
# start = datetime(2026, 9, 27, 22, 15)
# end = datetime(2026, 9, 27, 23, 0)
#
# event = {
#     "summary": "Test event",
#     "start": {"dateTime": start.isoformat(), "timeZone": "America/New_York"},
#     "end": {"dateTime": end.isoformat(), "timeZone": "America/New_York"},
# }
#
# result = service.events().insert(calendarId="primary", body=event).execute()
# print("Created:", result["id"], result.get("htmlLink"))


from mcp_server.tools.manage_appointment import create_appointment

# create
result = create_appointment( "Hello Event", "2026-09-28T14:30:00", 45)
print("created:", result)