from mcp_server.tools.manage_appointment import create_recurring_event

result = create_recurring_event(
    event_name="Recurrence Debug Test",
    start_time="2026-10-02T12:30:00",
    duration_minutes=60,
    frequency="WEEKLY",
    by_day=["FR"],
    until="2026-12-25",
)
print(result)