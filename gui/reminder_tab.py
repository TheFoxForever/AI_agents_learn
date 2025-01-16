from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import QDateTime, QTimer
from ai_agent import AIAgent


class ReminderTab(QWidget):
    def __init__(self, ai_agent: AIAgent):
        super().__init__()
        self.ai_agent = ai_agent
        self.reminders = []
        self.init_ui()
        QTimer.singleShot(
            0, self.update_reminder_list
        )  # Defer schedule loading until after the UI is initialized

    def init_ui(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.reminder_input = QLineEdit(self)
        self.reminder_input.setPlaceholderText("Enter reminder...")
        input_layout.addWidget(self.reminder_input)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Time (HH:MM)")
        input_layout.addWidget(self.time_input)

        layout.addLayout(input_layout)

        self.add_button = QPushButton("Add Reminder", self)
        self.add_button.clicked.connect(self.add_reminder)
        layout.addWidget(self.add_button)

        self.reminder_list = QListWidget(self)
        layout.addWidget(self.reminder_list)

        self.setLayout(layout)

        # Set up a timer to check reminders every minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(60000)  # 60000 milliseconds = 1 minute

    def add_reminder(self):
        reminder_text = self.reminder_input.text()
        time_text = self.time_input.text()
        if reminder_text and time_text:
            try:
                reminder_time = QDateTime.currentDateTime().addSecs(
                    self.parse_time(time_text)
                )
                self.reminders.append((reminder_text, reminder_time))
                self.reminder_list.addItem(
                    f"{reminder_text} - {reminder_time.toString('hh:mm')}"
                )
                self.reminder_input.clear()
                self.time_input.clear()
            except ValueError:
                self.ai_agent.process_query("Invalid time format. Please use HH:MM.")

    def parse_time(self, time_str):
        hours, minutes = map(int, time_str.split(":"))
        return hours * 3600 + minutes * 60

    def check_reminders(self):
        current_time = QDateTime.currentDateTime()
        for reminder, time in self.reminders:
            if current_time >= time:
                self.ai_agent.process_query(f"Reminder: {reminder}")
                self.reminders.remove((reminder, time))
                self.update_reminder_list()

    def update_reminder_list(self):
        self.reminder_list.clear()
        for reminder, time in self.reminders:
            self.reminder_list.addItem(f"{reminder} - {time.toString('hh:mm')}")
