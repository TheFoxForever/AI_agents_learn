from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QPushButton,
    QComboBox,
    QDateEdit,
)
from PyQt6.QtCore import Qt, QDate
from ai_agent import AIAgent


class TaskTab(QWidget):
    def __init__(self, ai_agent: AIAgent):
        super().__init__()
        self.ai_agent = ai_agent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Task list
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

        # Input area
        input_layout = QHBoxLayout()

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter task...")
        input_layout.addWidget(self.task_input)

        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(["Low", "Medium", "High"])
        input_layout.addWidget(self.priority_combo)

        self.deadline_edit = QDateEdit(self)
        self.deadline_edit.setDate(QDate.currentDate())
        self.deadline_edit.setCalendarPopup(True)
        input_layout.addWidget(self.deadline_edit)

        self.add_button = QPushButton("Add Task", self)
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.add_button)

        layout.addLayout(input_layout)

        # Control buttons
        control_layout = QHBoxLayout()

        self.complete_button = QPushButton("Mark Complete", self)
        self.complete_button.clicked.connect(self.mark_complete)
        control_layout.addWidget(self.complete_button)

        self.delete_button = QPushButton("Delete Task", self)
        self.delete_button.clicked.connect(self.delete_task)
        control_layout.addWidget(self.delete_button)

        layout.addLayout(control_layout)

        self.setLayout(layout)

        # Populate initial task list
        self.refresh_tasks()

    def add_task(self):
        task_text = self.task_input.text()
        priority = self.priority_combo.currentText()
        deadline = self.deadline_edit.date().toString(Qt.DateFormat.ISODate)

        if task_text:
            response = self.ai_agent.process_query(
                f"Add task: {task_text} with priority {priority} and deadline {deadline}"
            )
            self.task_input.clear()
            self.refresh_tasks()

    def mark_complete(self):
        current_item = self.task_list.currentItem()
        if current_item:
            task_text = current_item.text()
            response = self.ai_agent.process_query(
                f"Mark task as complete: {task_text}"
            )
            self.refresh_tasks()

    def delete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            task_text = current_item.text()
            response = self.ai_agent.process_query(f"Delete task: {task_text}")
            self.refresh_tasks()

    def refresh_tasks(self):
        self.task_list.clear()
        response = self.ai_agent.process_query("List all tasks")
        try:
            tasks = response.items()
            for task in tasks:
                if task.strip():  # Avoid adding empty items
                    self.task_list.addItem(task)
            if self.task_list.count() == 0:
                self.task_list.addItem("No tasks found")
        except AttributeError:
            return response
