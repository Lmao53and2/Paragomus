import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class ChatWindow(QWidget):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Agent Assistant")

        self.layout = QVBoxLayout()

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)

        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.handle_user_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_user_input)

        self.layout.addWidget(self.chat_box)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    def handle_user_input(self):
        user_text = self.input_line.text().strip()
        if not user_text:
            return

        self.chat_box.append(f"You: {user_text}")
        self.input_line.clear()

        response = self.agent.ask(user_text)
        response_text = response.content if hasattr(response, "content") else str(response)
        self.chat_box.append(f"Assistant: {response_text}")
