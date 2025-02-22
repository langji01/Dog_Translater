import sqlite3
from datetime import datetime

class DogTranslatorDB:
    def __init__(self):
        self.conn = sqlite3.connect('dog_records.db')
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                emotion TEXT,
                confidence REAL,
                audio_path TEXT,
                features TEXT
            )
        ''')
        self.conn.commit()
    
    def save_record(self, result, audio_path=None):
        sql = '''INSERT INTO recordings 
                (timestamp, emotion, confidence, audio_path, features)
                VALUES (?, ?, ?, ?, ?)'''
        self.conn.execute(sql, (
            datetime.now(),
            result['primary_emotion'][0],
            result['primary_emotion'][1],
            audio_path,
            str(result['emotions'])
        ))
        self.conn.commit() 