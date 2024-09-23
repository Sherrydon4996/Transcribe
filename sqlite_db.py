import sqlite3
import bcrypt
from datetime import datetime
import json
import streamlit as st


def create_database():
    connection = sqlite3.connect('transcribed_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            amount REAL DEFAULT 10,
            audio_filename TEXT,
            srt_file TEXT,
            json_file TEXT,
            password TEXT,
            current_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            username TEXT,
            email TEXT,
            amount REAL DEFAULT 0,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
         )
     ''')
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS user_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            full_name TEXT,
            comment TEXT,
            comment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
         )
     ''')
    # USER COMMENTS DATABASE TO BE ADDED

    connection.commit()
    connection.close()


create_database()


def save_credentials_to_database(full_name, username, email, new_password):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute('''INSERT INTO user_details
                          (full_name, username, email, password)
                          VALUES (?, ?, ?, ?)''',
                       (full_name, username, email, hashed_password))
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError as e:
        st.error(f"Database Integrity Error: {e}")
        return False


def get_logins(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select password from user_details where username=?", (username,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
    except Exception as e:
        st.error(f"Error: {e}")


def update_password(new_password, username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()

        # First, check if the user exists
        cursor.execute("SELECT * FROM user_details WHERE username=?", (username,))
        results = cursor.fetchone()

        if results is None:
            connection.close()
            return False  # User not found

        # If we're here, the user exists, so update the password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE user_details SET password=? WHERE username=?", (hashed_password, username))
        connection.commit()
        connection.close()
        return True  # Password updated successfully

    except Exception as e:
        st.error(f"Error: {e}")
        return False


def check_duplicate_registrations(username, email):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_details WHERE username=? OR email=?", (username, email))
        results = cursor.fetchall()
        connection.close()
        if results:
            return False  # Duplicate found
        return True
    except Exception as e:
        st.error(f"Error: {e}")


def save_login_history(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select full_name, username, email, current_time, amount from user_details where username=?",
                       (username,))
        results = cursor.fetchone()
        if results:
            cursor.execute(
                "insert into login_history(full_name, username, email, login_time, amount) values(?,?,?,?,?)",
                results)
            connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def get_full_name(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT full_name, email FROM user_details WHERE username=?", (username,))
        results = cursor.fetchone()
        connection.close()
        if results:
            return results
        else:
            return None, None  # Return None, None if no results found
    except Exception as e:
        st.error(f"Error retrieving user details: {e}")
        return None, None  # Return None, None in case of an exception


def get_user_balance(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select amount from user_details where username=?", (username,))
        results = cursor.fetchone()
        connection.close()
        if results:
            return results[0]
    except Exception as e:
        st.error(f"Error: {e}")


def update_balance(sign, amount, username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute(f"update user_details set amount = amount {sign} ? where username= ?", (amount, username))
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def save_json_file(json_file, username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("update user_details set json_file=? where username=?", (json_file, username))
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def get_all_user_details():
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select * from user_details")
        results = cursor.fetchall()
        connection.close()
        if results:
            return results
    except Exception as e:
        st.error(f"Error: {e}")


def get_login_history():
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select * from login_history")
        results = cursor.fetchall()
        connection.close()
        if results:
            return results
    except Exception as e:
        st.error(f"Error: {e}")


def delete_user(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("delete from user_details where username=?", (username,))
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def clear_login_history():
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("delete from login_history")
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def get_json_database(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select json_file from user_details where username=?", (username,))
        results = cursor.fetchone()
        connection.close()
        if results and results[0] is not None:
            json_data = json.loads(results[0])
            return json_data
    except Exception as e:
        st.error(f"Error: {e}")


def save_audio_filename(audio_file, username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("update user_details set audio_filename=? where username=?", (audio_file, username,))
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def get_audio_filename(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select audio_filename from user_details where username=?", (username,))
        results = cursor.fetchone()
        connection.close()
        if results:
            return results[0]
    except Exception as e:
        st.error(f"Error: {e}")


def save_srt_file(srt_file, username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("update user_details set srt_file=? where username=?", (srt_file, username,))
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def get_srt_file(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select srt_file from user_details where username=?", (username,))
        results = cursor.fetchone()
        connection.close()
        if results:
            return results[0]
    except Exception as e:
        st.error(f"Error: {e}")


def save_user_comments(username, full_name, comment):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("insert into user_comments(username, full_name, comment) values(?,?,?)",
                       (username, full_name, comment))
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error: {e}")


def user_commented(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select * from user_comments where username=?",
                       (username,))
        results = cursor.fetchone()
        connection.close()
        if results is not None:
            return True
        return False
    except Exception as e:
        st.error(f"Error: {e}")


def delete_comment(username):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("delete from user_comments where username=?",
                       (username,))
        connection.commit()
    except Exception as e:
        st.error(f"Error: {e}")


def filter_abusive_comments(username, comment):
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("update user_comments set comment=? where username=?",
                       (comment, username))
        connection.commit()
    except Exception as e:
        st.error(f"Error: {e}")


def retrieve_user_comments():
    try:
        connection = sqlite3.connect('transcribed_data.db')
        cursor = connection.cursor()
        cursor.execute("select * from user_comments")
        results = cursor.fetchall()
        connection.close()
        if results:
            return results
        return None

    except Exception as e:
        st.error(f"Error: {e}")
