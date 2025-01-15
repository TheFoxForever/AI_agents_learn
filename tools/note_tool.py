from langchain.tools import BaseTool
from database import Database
from typing import Any
from pydantic import Field


class NoteTool(BaseTool):
    name: str = "Note Manager"
    description: str = "Manage notes, add new notes, or get note summaries"
    db: Database = Field(default_factory=Database)

    def __init__(self, db: Database) -> None:
        super().__init__(db=db)

    def _run(self, query: str) -> str:
        if "add note" in query.lower():
            note_content = self.extract_note_content(query)
            self.db.add_note(note_content, "")
            return "Note added successfully."
        elif "summarize note" in query.lower():
            note_id = self.extract_note_id(query)
            note_content = self.db.get_note_content(note_id)
            summary = self.summarize(note_content)
            return f"Summary: {summary}"
        elif "list notes" in query.lower():
            notes = self.db.get_all_notes()
            return self.format_notes(notes)
        else:
            return "I'm not sure how to handle that note request."

    def _arun(self, query: str) -> Any:
        raise NotImplementedError("NoteTool does not support async")

    @staticmethod
    def extract_note_content(query: str) -> str:
        # Extract note content from the query
        return query.split("add note")[1].strip()

    @staticmethod
    def extract_note_id(query: str) -> int:
        # Implement note ID extraction logic
        return 1

    @staticmethod
    def summarize(content: str) -> str:
        return content[:50] + "..." if len(content) > 50 else content

    @staticmethod
    def format_notes(notes: list) -> str:
        return "\n".join([f"{note['id']}: {note['content']}" for note in notes])
