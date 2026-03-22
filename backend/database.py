import sqlite3
import logging

conn = sqlite3.connect('fitness_tracker.db')
cur = conn.cursor()

cur.execute("""
    CREATE TABLE auth_service_db (username, hash_password_hex, salt_hex, iterations)
""")
            
conn.commit()

conn.close()
