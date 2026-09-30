from mcp.server.fastmcp import FastMCP
from mcp_server.tools.query_database import query_database as _query_database
from mcp_server.tools.search_documents import search_documents as _search_documents
from mcp_server.tools.extract_to_db import extract_to_db as _extract_to_db


from mcp_server.tools.manage_appointment import create_appointment as _create_appointment
from mcp_server.tools.manage_appointment import find_appointments as _find_appointments
from mcp_server.tools.manage_appointment import cancel_appointment as _cancel_appointment
from mcp_server.tools.manage_appointment import reschedule_appointment as _reschedule_appointment


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