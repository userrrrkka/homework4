import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox
)


DB_NAME = "students.db"


class StudentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление студентами")
        self.resize(700, 500)
        self.init_ui()
        self.init_db()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ввод имени, возраста, оценки
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.id_input = QLineEdit()  # для удаления/обновления по ID
        self.filter_age_input = QLineEdit()

        self.grade_input = QComboBox()
        self.grade_input.addItems(["A", "B", "C", "D", "E", "F"])

        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Age:"))
        form_layout.addWidget(self.age_input)
        form_layout.addWidget(QLabel("Grade:"))
        form_layout.addWidget(self.grade_input)

        layout.addLayout(form_layout)

        # Строка для ID и фильтра по возрасту
        id_filter_layout = QHBoxLayout()
        id_filter_layout.addWidget(QLabel("ID (для удаления/обновления):"))
        id_filter_layout.addWidget(self.id_input)
        id_filter_layout.addWidget(QLabel("Возраст >"))
        id_filter_layout.addWidget(self.filter_age_input)
        layout.addLayout(id_filter_layout)

        # Кнопки
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.show_btn = QPushButton("Показать всех")
        self.delete_btn = QPushButton("Удалить по ID")
        self.update_btn = QPushButton("Обновить по ID")
        self.filter_btn = QPushButton("Фильтр по возрасту")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.show_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.filter_btn)

        layout.addLayout(btn_layout)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Grade"])
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Подключаем кнопки к методам
        self.add_btn.clicked.connect(self.add_student)
        self.show_btn.clicked.connect(self.show_students)
        self.delete_btn.clicked.connect(self.delete_student)
        self.update_btn.clicked.connect(self.update_student)
        self.filter_btn.clicked.connect(self.filter_students)

    def init_db(self):
        # Создаем таблицу, если не существует
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade TEXT NOT NULL
                )
            """)
            con.commit()

    def add_student(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        grade = self.grade_input.currentText()

        if not name or not age:
            QMessageBox.warning(self, "Ошибка", "Поля Name и Age должны быть заполнены.")
            return
        if not age.isdigit():
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом.")
            return

        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, int(age), grade))
            con.commit()

        QMessageBox.information(self, "Успех", f"Студент {name} добавлен.")
        self.clear_inputs()
        self.show_students()

    def show_students(self):
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
        self.fill_table(rows)

    def delete_student(self):
        id_text = self.id_input.text().strip()
        if not id_text or not id_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный ID для удаления.")
            return

        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE id = ?", (int(id_text),))
            con.commit()
            if cur.rowcount == 0:
                QMessageBox.information(self, "Инфо", f"Студент с ID {id_text} не найден.")
            else:
                QMessageBox.information(self, "Успех", f"Студент с ID {id_text} удалён.")
                self.show_students()

    def update_student(self):
        id_text = self.id_input.text().strip()
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        grade = self.grade_input.currentText()

        if not id_text or not id_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный ID для обновления.")
            return
        if not name or not age:
            QMessageBox.warning(self, "Ошибка", "Поля Name и Age должны быть заполнены для обновления.")
            return
        if not age.isdigit():
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом.")
            return

        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?",
                (name, int(age), grade, int(id_text))
            )
            con.commit()
            if cur.rowcount == 0:
                QMessageBox.information(self, "Инфо", f"Студент с ID {id_text} не найден.")
            else:
                QMessageBox.information(self, "Успех", f"Студент с ID {id_text} обновлён.")
                self.show_students()

    def filter_students(self):
        age_text = self.filter_age_input.text().strip()
        if not age_text or not age_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный возраст для фильтра.")
            return

        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM students WHERE age > ?", (int(age_text),))
            rows = cur.fetchall()
        self.fill_table(rows)

    def fill_table(self, rows):
        self.table.setRowCount(0)
        for row_data in rows:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.name_input.clear()
        self.age_input.clear()
        self.id_input.clear()
        self.filter_age_input.clear()
        self.grade_input.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StudentApp()
    win.show()
    sys.exit(app.exec())
