import sqlite3
import uuid
import os
from typing import List

from pydantic import BaseModel, Field, HttpUrl

class NotFound(Exception):
    pass

class ShortenedURL(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str
    short_url: str

    @classmethod
    def get_by_id(cls, id: str):
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM url_shortener WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # return cls(id=row[0], url=row[1], short_url=row[2])
            return cls(**row)
        
        raise NotFound

    @classmethod
    def get_by_short_url(cls, short_url: str):
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM url_shortener WHERE short_url = ?', (short_url,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(**row)
        
        raise NotFound

    @classmethod
    def get_by_url(cls, url: str):
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM url_shortener WHERE url = ?', (url,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(**row)
        
        raise NotFound
    
    @classmethod
    def list(cls) -> List:
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM url_shortener')
        rows = cursor.fetchall()
        conn.close()
        return [cls(**row) for row in rows]

    def save(self) -> "ShortenedURL":
        conn = sqlite3.connect(os.getenv('DATABASE_NAME', 'database.db'))
        cursor = conn.cursor()
        cursor.execute('INSERT INTO url_shortener (id, url, short_url) VALUES (?, ?, ?)', (self.id, self.url, self.short_url))
        conn.commit()
        conn.close()
        return self

    @classmethod
    def create_table(cls,database_name='database.db'):
        conn = sqlite3.connect(database_name)
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS url_shortener (
                id TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                short_url TEXT NOT NULL
            )
        ''')
        conn.close()