from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt
from ai_agent import AIAgent


class NoteTab(QWidget):
    def __init__(self, ai_agent: AIAgent):
        super().__init__()
        self.ai_agent = ai_agent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.note_input = QTextEdit(self)
        self.note_input.setPlaceholderText("Write your note here...")
        layout.addWidget(self.note_input)

        self.summarize_button = QPushButton("Summarize Note", self)
        self.summarize_button.clicked.connect(self.summarize_note)
        layout.addWidget(self.summarize_button)

        self.summary_label = QLabel("", self)
        self.summary_label.setWordWrap(True)
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.summary_label)

        self.setLayout(layout)

    def summarize_note(self):
        note_content = self.note_input.toPlainText()
        if note_content.strip():
            response = self.ai_agent.process_query(
                f"Summarize this note: {note_content}"
            )
            self.summary_label.setText(f"Summary: {response}")
        else:
            self.summary_label.setText("Please write a note to summarize.")
