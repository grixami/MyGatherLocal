from dotenv import dotenv_values
import os
import mysql.connector
import hashlib

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

def createTables(): # Ran every time when the webapp starts so it ensures tables are created
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bio TEXT,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                is_admin BOOLEAN
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_host INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (event_host) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_managers (
                event_id INT NOT NULL,
                user_id INT NOT NULL,
                PRIMARY KEY (event_id, user_id),
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_atendees (
                event_id INT NOT NULL,
                user_id INT NOT NULL,
                PRIMARY KEY (event_id, user_id),
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()

    except mysql.connector.Error as e:
        print(f"Error >> {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def addUser(username: str, password: str, is_admin: bool): # inserts a user into the database, password md5 hashed
    try:
        password_md5 = hashlib.md5(password.encode()).hexdigest()
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password, is_admin)
            VALUES (%s, %s, %s)
        """, (username, password_md5, is_admin))

        conn.commit()

    except mysql.connector.Error as e:
        print(f"Error >> {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def checkPassword(username: str, password: str) -> bool: # compares md5 hash of the password the user entered to the stored password and returns if it is correct or not
    try:
        password_md5 = hashlib.md5(password.encode()).hexdigest()
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))

        response = cursor.fetchone()
        
        if response is None:
            return(False, "User not found")

        stored_pass = response[0]

        conn.commit()

        if password_md5 == stored_pass:
            return(True, "Password Correct")
        else:
            return(True, "Password Incorrect")
        
        

    except mysql.connector.Error as e:
        print(f"Error >> {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()