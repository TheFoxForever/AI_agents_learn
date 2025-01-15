from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from ai_agent import AIAgent


class QueryTab(QWidget):
    def __init__(self, ai_agent: AIAgent):
        super().__init__()
        self.ai_agent = ai_agent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter your query here...")
        layout.addWidget(self.query_input)

        self.submit_button = QPushButton("Submit Query", self)
        self.submit_button.clicked.connect(self.submit_query)
        layout.addWidget(self.submit_button)

        self.response_display = QTextEdit(self)
        self.response_display.setReadOnly(True)
        layout.addWidget(self.response_display)

        self.setLayout(layout)

    def submit_query(self):
        query = self.query_input.text()
        if query.strip():
            response = self.ai_agent.process_query(query)
            self.response_display.setText(response)
        else:
            self.response_display.setText("Please enter a query.")
