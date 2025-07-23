import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout


class GreetingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приветствие")
        self.init_ui()

    def init_ui(self):
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя")
        self.greeting_label = QLabel("")

        self.name_input.returnPressed.connect(self.update_greeting)

        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.greeting_label)
        self.setLayout(layout)

    def update_greeting(self):
        name = self.name_input.text().strip()
        if name:
            self.greeting_label.setText(f"Привет, {name}!")
        else:
            self.greeting_label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GreetingApp()
    window.show()
    sys.exit(app.exec())
