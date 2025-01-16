from langchain.tools import BaseTool
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from database import Database


class ReminderToolInput(BaseModel):
    query: str = Field(..., description="The reminder-related query or command")


class ReminderTool(BaseTool):
    name: str = "Reminder Manager"
    description: str = (
        "Use this tool to manage reminders, add new reminders, or check due reminders"
    )
    args_schema: type[BaseModel] = ReminderToolInput
    db: Database = Field(default_factory=Database)

    def __init__(self, db: Database) -> None:
        super().__init__(db=db)

    def _run(self, query: str) -> str:
        if "add reminder" in query.lower():
            reminder_text, timestamp = self.extract_reminder_info(query)
            self.db.add_reminder(reminder_text, timestamp)
            return "Reminder added successfully."
        elif "list reminders" in query.lower():
            reminders = self.db.get_all_reminders()
            if not reminders:
                return "No reminders found. Your reminder list is empty."
            return self.format_reminders(reminders)
        elif "check reminders" in query.lower():
            current_time = self.extract_current_time(query)
            due_reminders = self.db.get_due_reminders(current_time)
            if not due_reminders:
                return "No due reminders found."
            return self.format_reminders(due_reminders)
        else:
            return "I'm not sure how to handle that reminder request."

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("ReminderTool does not support async")

    def add_reminder(self, reminder_text: str, timestamp: str) -> str:
        self.db.add_reminder(reminder_text, timestamp)
        return "Reminder added successfully."

    def list_reminders(self) -> str:
        reminders = self.db.get_all_reminders()
        return self.format_reminders(reminders)

    def check_reminders(self, current_time: str) -> str:
        due_reminders = self.db.get_due_reminders(current_time)
        return self.format_reminders(due_reminders)

    @staticmethod
    def format_reminders(reminders: list[dict]) -> str:
        return "\n".join(
            f"{reminder['id']}: {reminder['text']} at {reminder['timestamp']}"
            for reminder in reminders
        )

    @staticmethod
    def extract_reminder_info(query: str) -> tuple:
        # Extract reminder text and timestamp from the query
        # This is a simple implementation and can be improved
        parts = query.split(" at ")
        if len(parts) == 2:
            reminder_text = parts[0].replace("add reminder ", "").strip()
            timestamp = parts[1].strip()
            return reminder_text, timestamp
        return "", ""

    @staticmethod
    def extract_current_time(query: str) -> str:
        # Use the current date and time provided
        return "2025-01-09 16:00:00"

    def parse_timestamp(self, timestamp: str) -> datetime:
        return datetime.strptime(timestamp, "%Y-%m-%d %I:%M %p")
