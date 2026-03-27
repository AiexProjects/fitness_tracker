import sqlite3
import logging

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='a',
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")

class DatabaseManager:
    def __init__(self, db):
        self.db = db
        self.create_user_id_table()
        self.create_auth_service_table()


    def create_user_id_table(self):
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_id_db
                    (username TEXT UNIQUE, unique_user_id TEXT UNIQUE)
                """)

                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"UserID Table Creation Error: {e}")
        finally:
            if conn:
                conn.close()

    def create_auth_service_table(self):
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_service_db 
                    (unique_user_id TEXT UNIQUE, password_data TEXT)
                """)

                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database Table Creation Error: {e}")
        finally:
            if conn:
                conn.close()

    def assign_user_id(self, username, unique_user_id):
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO user_id_db 
                    (username, unique_user_id)
                    VALUES (?, ?)""", 
                    (username, unique_user_id,)
                )

                conn.commit()
                return True
        except sqlite3.IntegrityError:
            logging.debug(f"UserID assignment Failed: Username: {username} already exists")
            return False
        except sqlite3.Error as e:
            logging.error(f"Database Insert Error: {e}")
            return False

    def add_user(self, new_unique_user_id, new_password_data):
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO auth_service_db 
                    (unique_user_id, password_data)
                    VALUES (?, ?)""", 
                    (new_unique_user_id, new_password_data,)
                )

                conn.commit()
                return True
        except sqlite3.IntegrityError:
            logging.info(f"Sign-up attempt failed")
            return False
        except sqlite3.Error as e:
            logging.error(f"Database Insert Error: {e}")
            return False

    def get_user_id(self, username):
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT username, unique_user_id FROM user_id_db WHERE username=?
                """,
                (username,)
                )

                username_data = cursor.fetchone()

                if username_data:
                    user_id = username_data[1]

                    return user_id
                else:
                    logging.debug(f"Sign-in attempt failed: Username: {username} doesn't exist")
                    return None
        except sqlite3.Error as e:
            logging.error(f"Database Retrieve Error: {e}")
            return None

    
    def get_password_data(self, user_id):
        try:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT unique_user_id, password_data FROM auth_service_db WHERE unique_user_id=?
                """,
                (user_id,)
                )

                user_data = cursor.fetchone()

                if user_data:
                    password_data = user_data[1]

                    return password_data
                else:
                    logging.info(f"Sign-in attempt failed: Invalid username")
                    return None
        except sqlite3.Error as e:
            logging.error(f"Database Retrieve Error: {e}")
            return None
