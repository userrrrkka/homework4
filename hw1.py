import sqlite3

# Создание подключения и таблицы
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Удалим таблицу, если она уже существует (для тестирования)
cursor.execute("DROP TABLE IF EXISTS students")

# Создание таблицы
cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE,
    grade INTEGER
)
''')

conn.commit()

# Пример данных для вставки
students_data = [
    ('John', 22, 'john@example.com', 88),
    ('Emily', 19, 'emily@example.com', 92),
    ('Michael', 24, 'michael@example.com', 75),
    ('Sarah', 20, 'sarah@example.com', 85),
    ('David', 21, 'david@example.com', 90),
    ('Anna', 18, 'anna@example.com', 95),
    ('James', 23, 'james@example.com', 70),
    ('Laura', 25, 'laura@example.com', 100),
    ('Daniel', 17, 'daniel@example.com', 65),
    ('Olivia', 20, 'olivia@example.com', 80)
]

# Добавление данных
cursor.executemany('''
INSERT INTO students (name, age, email, grade)
VALUES (?, ?, ?, ?)
''', students_data)

conn.commit()

# Ввод минимального возраста
min_age = int(input("Введите минимальный возраст: "))

# Запрос к базе
cursor.execute('''
SELECT * FROM students WHERE age >= ?
''', (min_age,))

# Вывод результатов
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Email: {row[3]}, Grade: {row[4]}")

conn.close()
