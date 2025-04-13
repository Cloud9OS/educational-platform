import sqlite3
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
from src.utils.security import Security

@dataclass
class User:
    id: int
    username: str
    password: str
    salt: str
    role: str  # 'admin', 'teacher', or 'student'
    language: str = "ar"  # Default to Arabic

@dataclass
class Lesson:
    id: int
    title: str
    title_ar: str
    description: str
    description_ar: str
    image_path: str
    video_path: str
    created_by: int
    created_at: datetime

class Database:
    def __init__(self, db_path: str = "edu_platform.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.create_default_admin()

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    role TEXT NOT NULL,
                    language TEXT NOT NULL DEFAULT 'ar'
                )
            """)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    title_ar TEXT NOT NULL,
                    description TEXT NOT NULL,
                    description_ar TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    video_path TEXT NOT NULL,
                    created_by INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def create_default_admin(self):
        """Create default admin user if it doesn't exist"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                salt = Security.generate_salt()
                hashed_password = Security.hash_password("admin123", salt)
                cursor.execute("""
                    INSERT INTO users (username, password, salt, role, language)
                    VALUES (?, ?, ?, ?, ?)
                """, ("admin", hashed_password, salt, "admin", "ar"))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating default admin: {e}")

    def verify_user(self, username: str, password: str) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row:
                user = User(*row)
                if Security.verify_password(password, user.salt, user.password):
                    return user
            return None

    def add_user(self, username: str, password: str, role: str, language: str) -> Optional[User]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if username already exists
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return None
                
                salt = Security.generate_salt()
                hashed_password = Security.hash_password(password, salt)
                
                # Insert new user
                cursor.execute(
                    "INSERT INTO users (username, password, salt, role, language) VALUES (?, ?, ?, ?, ?)",
                    (username, hashed_password, salt, role, language)
                )
                
                # Get the newly created user
                user_id = cursor.lastrowid
                cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                row = cursor.fetchone()
                
                if row:
                    conn.commit()
                    return User(*row)
                return None
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def update_user(self, user_id: int, username: str, role: str, language: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if the new username is already taken by another user
                cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
                if cursor.fetchone():
                    return False
                
                cursor.execute(
                    "UPDATE users SET username = ?, role = ?, language = ? WHERE id = ?",
                    (username, role, language, user_id)
                )
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def delete_user(self, user_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # First delete all lessons created by this user
                cursor.execute("DELETE FROM lessons WHERE created_by = ?", (user_id,))
                # Then delete the user
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def get_users(self) -> List[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY username")
            return [User(*row) for row in cursor.fetchall()]

    def get_user(self, user_id: int) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(*row)
            return None

    def update_user_language(self, user_id: int, language: str) -> bool:
        """Update user's language preference"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE users SET language = ? WHERE id = ?
            """, (language, user_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user language: {e}")
            return False

    def add_lesson(self, lesson: Lesson) -> Optional[Lesson]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO lessons 
                    (title, title_ar, description, description_ar, image_path, video_path, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (lesson.title, lesson.title_ar, lesson.description, lesson.description_ar,
                     lesson.image_path, lesson.video_path, lesson.created_by)
                )
                conn.commit()
                return Lesson(
                    id=cursor.lastrowid,
                    title=lesson.title,
                    title_ar=lesson.title_ar,
                    description=lesson.description,
                    description_ar=lesson.description_ar,
                    image_path=lesson.image_path,
                    video_path=lesson.video_path,
                    created_by=lesson.created_by,
                    created_at=datetime.now()
                )
        except sqlite3.Error:
            return None

    def update_lesson(self, lesson: Lesson) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """UPDATE lessons SET 
                    title = ?, title_ar = ?, description = ?, description_ar = ?,
                    image_path = ?, video_path = ? WHERE id = ?""",
                    (lesson.title, lesson.title_ar, lesson.description, lesson.description_ar,
                     lesson.image_path, lesson.video_path, lesson.id)
                )
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def delete_lesson(self, lesson_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def get_lessons(self, teacher_id: Optional[int] = None) -> List[Lesson]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if teacher_id:
                cursor.execute("""
                    SELECT * FROM lessons 
                    WHERE created_by = ? 
                    ORDER BY created_at DESC
                """, (teacher_id,))
            else:
                cursor.execute("SELECT * FROM lessons ORDER BY created_at DESC")
            
            return [Lesson(
                id=row[0],
                title=row[1],
                title_ar=row[2],
                description=row[3],
                description_ar=row[4],
                image_path=row[5],
                video_path=row[6],
                created_by=row[7],
                created_at=datetime.strptime(row[8], "%Y-%m-%d %H:%M:%S") if row[8] else None
            ) for row in cursor.fetchall()]

    def get_lesson(self, lesson_id: int) -> Optional[Lesson]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,))
            row = cursor.fetchone()
            if row:
                return Lesson(
                    id=row[0],
                    title=row[1],
                    title_ar=row[2],
                    description=row[3],
                    description_ar=row[4],
                    image_path=row[5],
                    video_path=row[6],
                    created_by=row[7],
                    created_at=datetime.strptime(row[8], "%Y-%m-%d %H:%M:%S") if row[8] else None
                )
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()
                if row:
                    return User(*row)
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None 