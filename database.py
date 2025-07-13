import sqlite3
from typing import Dict, Optional, Any

DB_PATH = "telegram_bot.db"

def init_database():
    """Initialize the database and create the users table"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                parent_name TEXT NOT NULL,
                child_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade TEXT NOT NULL,
                goal TEXT NOT NULL,
                timezone TEXT NOT NULL,
                contact TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("created database ..")
        conn.commit()

def save_user_profile(user_id: int, profile_data: Dict[str, Any]) -> bool:
    """Save or update user profile"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO user_profiles 
                (user_id, parent_name, child_name, age, grade, goal, timezone, contact, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                user_id,
                profile_data['parent_name'],
                profile_data['child_name'],
                profile_data['age'],
                profile_data['grade'],
                profile_data['goal'],
                profile_data['timezone'],
                profile_data['contact']
            ))

            conn.commit()
            return True

    except (sqlite3.Error, KeyError) as e:
        print(f"Error saving profile: {e}")
        return False

def get_user_profile(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user profile by user_id"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, parent_name, child_name, age, grade, goal, 
                       timezone, contact, created_at, updated_at
                FROM user_profiles 
                WHERE user_id = ?
            ''', (user_id,))

            row = cursor.fetchone()
            if row:
                return {
                    'user_id': row[0],
                    'parent_name': row[1],
                    'child_name': row[2],
                    'age': row[3],
                    'grade': row[4],
                    'goal': row[5],
                    'timezone': row[6],
                    'contact': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                }
            return None

    except sqlite3.Error as e:
        print(f"Error getting profile: {e}")
        return None


# Initialize database when module is imported
init_database()
