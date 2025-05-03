import sqlite3
from contextlib import contextmanager
from typing import Generator, Any

DATABASE_PATH = 'database.db'
# Устанавливаем соединение с базой данных
connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
balance INTEGER NOT NULL,
last_msg_sup TEXT
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()


@contextmanager
def get_db() -> Generator[sqlite3.Cursor, None, None]:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

# Example database functions using the context manager
def add_user(user_id: int) -> None:
    with get_db() as cursor:
        # Проверяем существует ли пользователь
        cursor.execute("SELECT id FROM Users WHERE id = ?", (user_id,))
        if cursor.fetchone() is None:
            # Если пользователя нет - добавляем
            cursor.execute(
                "INSERT INTO Users (id, balance, last_msg_sup) VALUES (?, ?, ?)",
                (user_id, 0, None)
            )


def get_user(user_id: int) -> Any:
    with get_db() as cursor:
        cursor.execute("SELECT * FROM USERS WHERE id = ?", (user_id,))
        return cursor.fetchone()

def update_user_balance(user_id: int, amount: int,funk: str) -> bool:
    with get_db() as cursor:
        if funk == "+":
          cursor.execute("UPDATE USERS SET balance = balance + ? WHERE id = ?", (amount, user_id))
        elif funk == "-":  
          all_users = cursor.execute("SELECT * FROM USERS WHERE id = ?", (user_id,)).fetchone()
          if all_users[1] >= amount:
            cursor.execute("UPDATE USERS SET balance = balance - ? WHERE id = ?", (amount, user_id))
          else:
            return "Недастаточно средств"       

def update_last_time_user(user_id: int, last_msg_sup: str) -> None:
    with get_db() as cursor:
        cursor.execute("UPDATE Users SET last_msg_sup = ? WHERE id = ?", (last_msg_sup, user_id))        