"""SQLite database helper for storing inspection records."""
import sqlite3
import os
import json
from datetime import datetime
from config.settings import DB_PATH

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_id TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            image_name TEXT NOT NULL,
            defect_count INTEGER NOT NULL,
            defect_names TEXT,
            detections_json TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_inspection(inspection_id, image_name, defect_count, defect_names, detections, status):
    """Inserts an inspection record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO inspections (inspection_id, timestamp, image_name, defect_count, defect_names, detections_json, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        inspection_id,
        timestamp,
        image_name,
        defect_count,
        ", ".join(defect_names) if isinstance(defect_names, list) else str(defect_names),
        json.dumps(detections),
        status
    ))
    conn.commit()
    conn.close()

def get_all_inspections():
    """Fetches all inspections ordered by timestamp descending."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, inspection_id, timestamp, image_name, defect_count, defect_names, status, detections_json FROM inspections ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_inspection_by_id(inspection_id):
    """Fetches a specific inspection record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, inspection_id, timestamp, image_name, defect_count, defect_names, status, detections_json FROM inspections WHERE inspection_id = ?", (inspection_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_all_inspections():
    """Clears all records."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inspections")
    conn.commit()
    conn.close()

