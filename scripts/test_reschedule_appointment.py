from mcp_server.tools.manage_appointment import create_appointment, reschedule_appointment

# create a fresh test event at a known time
created = create_appointment("Reschedule Test", "2026-10-05T09:00:00", 30)
print("Created:", created)

# now actually move it somewhere different
result = reschedule_appointment(event_id=created["event_id"], new_start_time="2026-10-07T15:00:00", duration_minutes=60)
print("Rescheduled:", result)