from langchain.tools import BaseTool
from database import Database
from typing import Any, Optional
from datetime import datetime
from pydantic import Field


class TaskTool(BaseTool):
    name: str = "Task Manager"
    description: str = "Use this tool to list, add, or manage tasks"
    db: Database = Field(default_factory=Database)

    def __init__(self, db: Database) -> None:
        super().__init__(db=db)

    def _run(self, query: str) -> str:
        if "add task" in query.lower():
            title = self.extract_title(query)
            priority = self.extract_priority(query)
            deadline = self.extract_deadline(query)
            self.db.add_task(title, "", priority, deadline, "New")
            return f"Added task: {title}"
        elif "list tasks" in query.lower():
            # Retrieve and format tasks
            tasks = self.db.get_all_tasks()
            return "\n".join(
                [
                    f"{task['id']}: {task['title']} (Priority: {task['priority']}, Status: {task['status']})"
                    for task in tasks
                ]
            )
        else:
            return "I'm not sure how to handle that task request."

    def _arun(self, query: str) -> Any:
        raise NotImplementedError("TaskTool does not support async")

    @staticmethod
    def extract_title(query: str) -> str:
        # Extract title from the query
        return query.split("add task")[1].strip()

    @staticmethod
    def extract_priority(query: str) -> int:
        # Extract priority from the query, default to medium (2)
        if "high priority" in query.lower():
            return 3
        elif "low priority" in query.lower():
            return 1
        return 2

    @staticmethod
    def extract_deadline(query: str) -> Optional[datetime]:
        # Extract deadline from the query
        if "due" in query.lower():
            date_str = query.split("due")[1].strip()
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                pass
        return None

    @staticmethod
    def format_task_list(
        tasks: list[tuple[int, str, str, int, Optional[datetime], str]]
    ) -> str:
        # Implement task list formatting
        return "\n".join(
            f"{id}: {title} (Priority: {priority}, Deadline: {deadline})"
            for id, title, _, priority, deadline, _ in tasks
        )
