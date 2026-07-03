import sqlite3
import hashlib
import os

DB_PATH = "users.db"

def init_auth_db():
    """Initializes the SQLite database for user accounts if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    """Securely hashes passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Registers a new user. Returns True if successful, False if username exists."""
    init_auth_db()
    username = username.strip().lower()
    if not username or not password:
        return False, "Username and password cannot be empty."
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, "Registration successful! Please Sign In."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def verify_user(username, password):
    """Verifies user credentials for signing in."""
    init_auth_db()
    username = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[0] == hash_password(password):
        return True
    return False