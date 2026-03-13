import sqlite3
import bcrypt

class AuthManager:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    email TEXT
                )
            ''')
            conn.commit()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def create_user(self, username, password, email=None):
        hashed_pw = self.hash_password(password)
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (username, hashed_pw, email)
                )
                conn.commit()
            return True, "User created successfully!"
        except sqlite3.IntegrityError:
            return False, "Username already exists."
        except Exception as e:
            return False, f"Error: {str(e)}"

    def authenticate_user(self, username, password):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT password FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                if self.check_password(password, row[0]):
                    return True, "Login successful!"
            return False, "Invalid username or password."
