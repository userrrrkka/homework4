import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel


class GreetingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приветствие")
        self.init_ui()

    def init_ui(self):
        # Создаем элементы интерфейса
        self.input_field = QLineEdit()
        self.label = QLabel("Введите ваше имя и нажмите Enter")

        # Подключаем сигнал returnPressed к методу обновления метки
        self.input_field.returnPressed.connect(self.update_greeting)

        # Создаем и задаем вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def update_greeting(self):
        name = self.input_field.text().strip()
        if name:
            self.label.setText(f"Привет, {name}!")
        else:
            self.label.setText("Пожалуйста, введите имя")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GreetingApp()
    window.show()
    sys.exit(app.exec())
