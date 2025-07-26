import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'detections.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create table for weapon detections
    c.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weapon_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            camera_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL,
            image_path TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_detection(weapon_type, confidence, camera_id, image_path=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Ensure the values are of the correct type
        weapon_type = str(weapon_type)
        confidence = float(confidence)
        camera_id = int(camera_id)
        
        c.execute('''
            INSERT INTO detections (weapon_type, confidence, camera_id, timestamp, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (weapon_type, confidence, camera_id, timestamp, image_path))
        
        detection_id = c.lastrowid
        
        conn.commit()
        conn.close()
        
        print(f"Successfully logged detection {detection_id} to database")
        return detection_id
    except Exception as e:
        print(f"Database error in log_detection: {str(e)}")
        raise

def get_recent_detections(limit=10, weapon_type=None, minutes=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    query = 'SELECT * FROM detections WHERE 1=1'
    params = []
    
    if weapon_type:
        query += ' AND weapon_type = ?'
        params.append(weapon_type)
    
    if minutes:
        query += ' AND timestamp >= datetime("now", "-? minutes")'
        params.append(minutes)
    
    query += ' ORDER BY timestamp DESC'
    
    if limit:
        query += ' LIMIT ?'
        params.append(limit)
    
    c.execute(query, params)
    detections = c.fetchall()
    conn.close()
    
    return detections
