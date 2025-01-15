from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QCalendarWidget,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import QDate
from ai_agent import AIAgent


class ScheduleTab(QWidget):
    def __init__(self, ai_agent: AIAgent):
        super().__init__()
        self.ai_agent = ai_agent
        self.schedule = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget(self)
        self.calendar.selectionChanged.connect(self.update_schedule_display)
        layout.addWidget(self.calendar)

        self.schedule_display = QTextEdit(self)
        self.schedule_display.setReadOnly(True)
        layout.addWidget(self.schedule_display)

        input_layout = QHBoxLayout()
        self.event_input = QTextEdit(self)
        self.event_input.setPlaceholderText("Enter event details...")
        input_layout.addWidget(self.event_input)

        self.add_button = QPushButton("Add Event", self)
        self.add_button.clicked.connect(self.add_event)
        input_layout.addWidget(self.add_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)

    def update_schedule_display(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        if selected_date in self.schedule:
            self.schedule_display.setText("\n".join(self.schedule[selected_date]))
        else:
            self.schedule_display.setText("No events scheduled for this date.")

    def add_event(self):
        event_text = self.event_input.toPlainText()
        if event_text:
            selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            if selected_date not in self.schedule:
                self.schedule[selected_date] = []
            self.schedule[selected_date].append(event_text)
            self.update_schedule_display()
            self.event_input.clear()
            self.ai_agent.process_query(
                f"Added event to schedule on {selected_date}: {event_text}"
            )
