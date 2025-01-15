import sqlite3
from typing import List, Dict, Any


class Database:
    def __init__(self, db_name: str = "assistant.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                priority INTEGER,
                deadline TEXT,
                status TEXT
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                content TEXT,
                timestamp TEXT
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                text TEXT,
                timestamp TEXT
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                text TEXT,
                date TEXT
            )
        """
        )
        self.conn.commit()

    def add_task(
        self, title: str, description: str, priority: int, deadline: str, status: str
    ) -> int:
        self.cursor.execute(
            """
            INSERT INTO tasks (title, description, priority, deadline, status)
            VALUES (?, ?, ?, ?, ?)
        """,
            (title, description, priority, deadline, status),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        return [
            {
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "priority": task[3],
                "deadline": task[4],
                "status": task[5],
            }
            for task in tasks
        ]

    def add_note(self, content: str, timestamp: str) -> int:
        self.cursor.execute(
            "INSERT INTO notes (content, timestamp) VALUES (?, ?)", (content, timestamp)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_notes(self) -> List[Dict[str, Any]]:
        self.cursor.execute("SELECT * FROM notes")
        notes = self.cursor.fetchall()
        return [
            {"id": note[0], "content": note[1], "timestamp": note[2]} for note in notes
        ]

    def add_reminder(self, text: str, timestamp: str) -> int:
        self.cursor.execute(
            "INSERT INTO reminders (text, timestamp) VALUES (?, ?)", (text, timestamp)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_reminders(self) -> List[Dict[str, Any]]:
        self.cursor.execute("SELECT * FROM reminders")
        reminders = self.cursor.fetchall()
        return [
            {"id": reminder[0], "text": reminder[1], "timestamp": reminder[2]}
            for reminder in reminders
        ]

    def add_event(self, text: str, date: str) -> int:
        self.cursor.execute(
            "INSERT INTO events (text, date) VALUES (?, ?)", (text, date)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_events_by_date(self, date: str) -> List[Dict[str, Any]]:
        self.cursor.execute("SELECT * FROM events WHERE date = ?", (date,))
        events = self.cursor.fetchall()
        return [
            {"id": event[0], "text": event[1], "date": event[2]} for event in events
        ]

    def close(self):
        self.conn.close()
