from mcp.server.fastmcp import FastMCP
from mcp_server.tools.query_database import query_database as _query_database
from mcp_server.tools.search_documents import search_documents as _search_documents
from mcp_server.tools.extract_to_db import extract_to_db as _extract_to_db


from mcp_server.tools.manage_appointment import create_appointment as _create_appointment
from mcp_server.tools.manage_appointment import find_appointments as _find_appointments
from mcp_server.tools.manage_appointment import cancel_appointment as _cancel_appointment
from mcp_server.tools.manage_appointment import reschedule_appointment as _reschedule_appointment
from mcp_server.tools.manage_appointment import create_recurring_event as _create_recurring_event

mcp = FastMCP("langchain-mcp-llm")


@mcp.tool()
def query_database(question: str) -> dict:
    return _query_database(question)

@mcp.tool()
def search_documents(query: str, top_k: int = 5) -> dict:
    """Find documents chunk related to natural language query, for answering questions from ingested files."""
    return _search_documents(query, top_k)

@mcp.tool()
def extract_to_db(source_file: str, text: str) -> dict:
    """"""
    return _extract_to_db(source_file, text)

# google calendar api
@mcp.tool()
def create_appointment(event_name: str, start_time: str, duration_minuites: int = 30 ) -> dict:
    """Schedule a calendar appointment with the given name/subject.
        start_time must be an ISO 8601 datetime string (e.g. '2026-10-01T14:00:00').
        duration_minutes defaults to 30 if not specified.
        IMPORTANT: if the request is ambiguous or contradictory, ask before creating multiple events."""
    return _create_appointment(event_name, start_time, duration_minuites)

@mcp.tool()
def create_recurring_event(
        event_name: str,
        start_time: str,
        duration_minutes: int = 30,
        frequency: str = "WEEKLY",
        by_day: list[str] | None = None,
        until: str | None = None,
        count: str | None = None,
) -> dict:
    """Create a single recurring calendar event (e.g. "every weekday", "every Friday until December").
       ALWAYS use this instead of calling create_appointment multiple times for a repeating schedule —
       this creates one true recurring series that Google Calendar manages natively, rather than many
       separate individual events, and can be cancelled/rescheduled with one call instead of many.

       Parameters:
       - start_time: ISO 8601 datetime of the FIRST occurrence (e.g. '2026-10-02T12:30:00').
       - frequency: 'DAILY', 'WEEKLY', or 'MONTHLY'.
       - by_day: list of two-letter weekday codes for which days it repeats on, e.g. ['FR'] for every Friday,
         or ['MO','TU','WE','TH','FR'] for every weekday. Omit for daily/monthly recurrence with no specific day.
       - until: ISO date (e.g. '2026-12-31') — the recurrence ends on or before this date. Use this for
         requests like "until the end of the year" or "through December".
       - count: number of occurrences instead of an end date — use this for requests like "for the next 10 weeks".
       You must provide exactly one of `until` or `count`, never both, and never neither — every recurring
       event must have a defined end."""

    return _create_recurring_event(
        event_name,
        start_time,
        duration_minutes,
        frequency,
        by_day,
        until,
        count)

@mcp.tool()
def find_events(query: str, days_ahead: int = 60) -> dict:
    """Search calendar events. Two ways to use this:
        Keyword search for an upcoming event by title (e.g. to find an event_id before cancelling/rescheduling):
       provide `query` (e.g. "HR Meeting"). Searches from now through `days_ahead` days ahead (default 60).
       Returns a list of matching events with event_id, summary, and start_time.
    """
    return _find_appointments(query, days_ahead)

@mcp.tool()
def cancel_event(event_id: str) -> dict:
    """Cancel/delete an existing calendar event, given its event_id.
    IMPORTANT: this is a destructive action that notifies any invitees the event was canceled.
    Always call the find_events first to locate the correct event_id, show the matched event to the user,
    and get their explicit confirmation before call this tool. Never cancel an event you found ambiguous or weren't asked to cancel.
    """
    return _cancel_appointment(event_id)

@mcp.tool()
def reschedule_event(event_id: str, new_start_time: str, durations_minutes: int = 30) -> dict:
    """Re-schedule a calendar appointment with the given name/subject or envent id.
    IMPORTANT: this is an impactful change, first use find events to verify if the event to be changed exist.
    then continue to reschedule the existing event"""
    return _reschedule_appointment(event_id, new_start_time, durations_minutes)

if __name__ == "__main__":
    mcp.run(transport="stdio")


# test running mcp server using below command
# uv run python -m mcp_server.server