from langchain.tools import BaseTool
from database import Database
from typing import Any
from pydantic import Field


class ScheduleTool(BaseTool):
    name: str = "Schedule Manager"
    description: str = (
        "Manage schedule, add new events, or list events for a specific date"
    )
    db: Database = Field(default_factory=Database)

    def __init__(self, db: Database) -> None:
        super().__init__(db=db)

    def _run(self, query: str) -> str:
        if "add event" in query.lower():
            event_text, event_date = self.extract_event_info(query)
            self.db.add_event(event_text, event_date)
            return "Event added successfully."
        elif "list events" in query.lower():
            date = self.extract_date(query)
            events = self.db.get_events_by_date(date)
            if not events:
                return "No events found. Your event list is empty."
            return self.format_events(events)
        else:
            return "I'm not sure how to handle that schedule request."

    def _arun(self, query: str) -> Any:
        raise NotImplementedError("ScheduleTool does not support async")

    @staticmethod
    def extract_event_info(query: str) -> tuple:
        # Extract event text and date from the query
        parts = query.split(" on ")
        if len(parts) == 2:
            event_text = parts[0].replace("add event ", "").strip()
            event_date = parts[1].strip()
            return event_text, event_date
        return "", ""

    @staticmethod
    def extract_date(query: str) -> str:
        # Extract date from the query
        if "for" in query.lower():
            return query.split("for")[1].strip()
        return ""

    @staticmethod
    def format_events(events: list) -> str:
        return "\n".join(
            [f"{event['id']}: {event['text']} on {event['date']}" for event in events]
        )
