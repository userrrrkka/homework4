import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit
)


class StudentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Студенты")
        self.setGeometry(100, 100, 400, 400)

        self.init_ui()
        self.create_table()

    # ---------- Интерфейс ----------
    def init_ui(self):
        # Поля ввода
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.grade_input = QLineEdit()

        # Метки
        name_label = QLabel("Name:")
        age_label = QLabel("Age:")
        grade_label = QLabel("Grade:")

        # Кнопки
        add_button = QPushButton("Добавить")
        show_button = QPushButton("Показать всех")

        # Вывод
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        # Layout ввода
        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(age_label)
        layout.addWidget(self.age_input)

        layout.addWidget(grade_label)
        layout.addWidget(self.grade_input)

        # Layout кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(show_button)

        layout.addLayout(button_layout)
        layout.addWidget(self.output_area)

        self.setLayout(layout)

        # Связь сигналов с методами
        add_button.clicked.connect(self.add_student)
        show_button.clicked.connect(self.show_all_students)

    # ---------- Подключение к БД ----------
    def connect_db(self):
        return sqlite3.connect("students.db")

    # ---------- Создание таблицы ----------
    def create_table(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                grade TEXT
            )
        """)
        conn.commit()
        conn.close()

    # ---------- Добавление записи ----------
    def add_student(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        grade = self.grade_input.text().strip()

        if not name or not age or not grade:
            self.output_area.setText("Пожалуйста, заполните все поля.")
            return

        try:
            age = int(age)
        except ValueError:
            self.output_area.setText("Возраст должен быть числом.")
            return

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
                       (name, age, grade))
        conn.commit()
        conn.close()

        self.output_area.setText(f"Добавлен студент: {name}, {age} лет, класс {grade}")
        self.name_input.clear()
        self.age_input.clear()
        self.grade_input.clear()

    # ---------- Получение всех записей ----------
    def show_all_students(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()

        if rows:
            result = "\n".join([f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Класс: {row[3]}" for row in rows])
        else:
            result = "Нет данных."

        self.output_area.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentApp()
    window.show()
    sys.exit(app.exec())
