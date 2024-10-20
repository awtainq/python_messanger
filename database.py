import sqlite3
import json
import datetime
import uuid
import hashlib

class DatabaseManager:
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        self.connection = sqlite3.connect(self.db_file_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.initial_users()
        self.initial_chats()
        self.initial_messages()
        self.initial_comments()

    def initial_users(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                login TEXT,
                password_hash TEXT,
                salt TEXT)
        """)
        self.commit()

    def initial_chats(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Chats (
                id INTEGER PRIMARY KEY,
                name TEXT)
        """)
        self.commit()

    def initial_messages(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Messages (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                message TEXT,
                user_id INTEGER,
                likes JSON DEFAULT NULL,
                time DATETIME)
        """)
        self.commit()

    def initial_comments(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Comments (
                id INTEGER PRIMARY KEY,
                message_id INTEGER,
                user_id INTEGER,
                comment TEXT,
                time DATETIME)
        """)
        self.commit()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
        
    def messages_get(self, chat_id):
        return self.cursor.execute("""
            SELECT Messages.message, Users.login, Messages.time, Messages.id
            FROM Messages 
            JOIN Users ON Messages.user_id = Users.user_id 
            WHERE Messages.chat_id = ? 
            ORDER BY Messages.time
        """, (chat_id,)).fetchall()
        
    def chat_names_get(self):
        return self.cursor.execute("SELECT name, id FROM Chats").fetchall()
    
    def chat_add(self, chatname):
        self.cursor.execute("INSERT INTO Chats (name) VALUES (?)", (chatname,))
        self.commit()
        
    def like_message(
        self, message_id, user_id):
        self.cursor.execute("SELECT likes FROM Messages WHERE id = ?", (message_id,))
        result = self.cursor.fetchone()

        likes = json.loads(result[0]) if result[0] else []
        if user_id in likes:
            likes.remove(user_id)
        else:
            likes.append(user_id)
        self.cursor.execute("UPDATE Messages SET likes = ? WHERE id = ?", (json.dumps(likes), message_id))
        self.commit()
        
    def get_likes_count(self, message_id):
        self.cursor.execute("SELECT likes FROM Messages WHERE id = ?", (message_id,))
        result = self.cursor.fetchone()
        if result is None:
            return 0
        likes = json.loads(result[0]) if result[0] else []
        return len(likes)
    
    def get_comments(self, message_id):
        return self.cursor.execute("""
            SELECT Comments.comment, Users.login, Comments.time
            FROM Comments 
            JOIN Users ON Comments.user_id = Users.user_id 
            WHERE Comments.message_id = ? 
            ORDER BY Comments.time
        """, (message_id,)).fetchall()
        
    def comment_message(self, message_id, comment_text, user_id):
        current_time = datetime.datetime.now()
        self.cursor.execute("INSERT INTO Comments (message_id, comment, user_id, time) VALUES (?, ?, ?, ?)",
            (message_id, comment_text, user_id, current_time))
        self.commit()
        
    def message_add(self, chat_id, message_text, user_id):
        current_time = datetime.datetime.now()
        self.cursor.execute("INSERT INTO Messages (chat_id, message, user_id, time) VALUES (?, ?, ?, ?)",
            (chat_id, message_text, user_id, current_time))
        self.commit()
        
    def sign_in(self, user, password):
        for user_id, username, hashed_password, salt in self.cursor.execute("SELECT user_id, login, password_hash, salt FROM Users").fetchall():
            if user == username:
                if hashed_password == hash_password(password, salt):
                    return user_id, username
        return None
    
    def check_name(self, username):
        return self.cursor.execute("SELECT login FROM Users WHERE login = ?", (username,)).fetchone()
    
    def sign_up(self, username, password):
        salt = uuid.uuid4().hex
        self.cursor.execute("INSERT INTO Users (login, password_hash, salt) VALUES (?, ?, ?)", (username, hash_password(password, salt), salt))
        self.commit()
        return self.cursor.execute("SELECT user_id, login FROM Users WHERE login = ?", (username,)).fetchone()

def hash_password(password, salt):
        return hashlib.sha256((salt.encode() + password.encode())).hexdigest()
    