import sys
import os
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon, QCloseEvent
from PyQt6.QtCore import QSize
from .task_tab import TaskTab
from .schedule_tab import ScheduleTab
from .query_tab import QueryTab
from .note_tab import NoteTab
from .reminder_tab import ReminderTab
from ai_agent import AIAgent


class MainWindow(QMainWindow):
    def __init__(self, ai_agent: AIAgent) -> None:
        super().__init__()
        self.ai_agent: AIAgent = ai_agent
        self.init_ui()

    def init_ui(self) -> None:
        print("init_ui called")
        self.setWindowTitle("AI Personal Assistant")
        self.setGeometry(50, 50, 600, 400)

        self.tab_widget: QTabWidget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.addTab(TaskTab(self.ai_agent), "Tasks")
        self.tab_widget.addTab(ScheduleTab(self.ai_agent), "Schedule")
        self.tab_widget.addTab(QueryTab(self.ai_agent), "Quick Query")
        self.tab_widget.addTab(NoteTab(self.ai_agent), "Notes")
        self.tab_widget.addTab(ReminderTab(self.ai_agent), "Reminders")

    def closeEvent(self, event: QCloseEvent) -> None:
        # Implement any cleanup needed when closing the application
        event.accept()
