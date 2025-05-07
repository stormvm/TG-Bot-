
import sqlite3
from contextlib import contextmanager
from typing import Generator, Any, List, Optional
import json
DATABASE_PATH = 'bot\settings\database.db'
# Устанавливаем соединение с базой данных
connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Support (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    photos TEXT,  -- JSON строка с массивом file_ids
    videos TEXT,  -- JSON строка с массивом file_ids
    text TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
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
def save_support_message(
    user_id: int, 
    photos: Optional[List[str]] = None,
    videos: Optional[List[str]] = None,
    text: Optional[str] = None
) -> int:
    """
    Сохраняет сообщение в поддержку
    """
    print("Saving to DB:", {  # Debug print
        "user_id": user_id,
        "photos": photos,
        "videos": videos,
        "text": text
    })
    
    with get_db() as cursor:
        photos_json = json.dumps(photos) if photos else None
        videos_json = json.dumps(videos) if videos else None
        
        cursor.execute(
            """
            INSERT INTO Support (user_id, photos, videos, text)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, photos_json, videos_json, text)
        )
        return cursor.lastrowid
def get_support_message(message_id: int) -> Optional[dict]:
    """Получает сообщение по ID"""
    with get_db() as cursor:
        cursor.execute("SELECT * FROM Support WHERE id = ?", (message_id,))
        row = cursor.fetchone()
        if not row:
            return None
            
        return {
            'id': row[0],
            'user_id': row[1],
            'photos': json.loads(row[2]) if row[2] else None,
            'videos': json.loads(row[3]) if row[3] else None,
            'text': row[4],
            'status': row[5],
            'created_at': row[6]
        }
        