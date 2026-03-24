import sqlite3
import logging

from auth_service import AuthService, signup, login

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='a',
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")

class DatabaseManager:
    def __init__(self, db):
        self.db = db
        self.create_table()

        self.new_username = signup

    def create_table(self):
        conn = None
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_service_db 
                    (username, password_data)
                """)

                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database Table Creation Error: {e}")
        finally:
            if conn:
                conn.close()

    def add_user(self, new_username, new_password_data):
        conn = None
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO auth_service_db 
                    (username UNIQUE, password_data)
                    VALUES (?, ?)""", 
                    (new_username, new_password_data)
                )

                conn.commit()
                return True
        except sqlite3.IntegrityError:
            logging.info(f"Sign-up attempt failed: Username: {new_username} already exists")
            return False
        except sqlite3.Error as e:
            logging.error(f"Database Insert Error: {e}")
            return False
    
    def get_password_data(self, username):
        conn = None
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT username, password_data FROM auth_service_db WHERE username='?',
                """,
                (username)
                )

                username_data = cursor.fetchone()

                if username_data[0]:
                    password_data = username_data[1]

                    return password_data
                else:
                    logging.info(f"Sign-in attempt failed: Username: {username} doesn't exist")
                    return None
        except sqlite3.Error as e:
            logging.error(f"Database Retrieve Error: {e}")
            return None
