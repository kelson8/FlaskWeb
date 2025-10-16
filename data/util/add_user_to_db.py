import bcrypt
import sqlite3

# This can create a user without needing to do it with the website, useful for making admin users.
# I will probably not enable registration on this website.

db_path = "../instance/users.db"

import bcrypt
import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn):
    """Create the users table."""
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_users_table)
    except sqlite3.Error as e:
        print(e)


def insert_user(conn, username, hashed_password, role):
    """Insert a new user into the user table."""
    sql = ''' INSERT INTO user(username, password, role)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (username, hashed_password, role))
    conn.commit()
    return cur.lastrowid


def user_exists(conn, username):
    """Check if the user already exists in the database."""
    cur = conn.cursor()
    cur.execute("SELECT username FROM user WHERE username = ?", (username,))
    return cur.fetchone() is not None


def register_user(username, plain_password, role):
    """Register a new user."""
    with create_connection(db_path) as conn:
        create_table(conn)

        # Check if the user already exists
        if user_exists(conn, username):
            print("User already exists.")
            return None

        # Hash the password
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

        # Insert user into the database
        user_id = insert_user(conn, username, hashed_password.decode('utf-8'), role)

    return user_id


if __name__ == "__main__":
    username = input("Enter username: ")
    plain_password = input("Enter password: ")
    role = input("Enter role (admin/user): ")

    user_id = register_user(username, plain_password, role)

    if user_id is not None:
        print(f"User created with ID: {user_id}")
