import sqlite3
from database.db_config import connect_db

def create_tables():

    conn = connect_db()

    cursor = conn.cursor()

    #User table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT,

        email TEXT UNIQUE,

        password TEXT,

        bio TEXT DEFAULT '',

        university TEXT DEFAULT '',

        department TEXT DEFAULT '',

        skills TEXT DEFAULT ''                    
    )
    """)

    #notes_table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        title TEXT,

        subject TEXT,

        content TEXT,

        original_file_path TEXT,

        pdf_path TEXT,

        file_type TEXT,       

        is_public INTEGER DEFAULT 0
    )
    """) 

    conn.commit()

    conn.close() 
def get_user_notes(user_email):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, subject FROM notes WHERE user_email = ?",
        (user_email,)
    )

    notes = cursor.fetchall()

    conn.close()

    return notes
def get_note_by_id(note_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            title,
            subject,
            content,
            pdf_path

        FROM notes

        WHERE id = ?
        """,
        (note_id,)
    )

    note = cursor.fetchone()

    conn.close()

    return note

def create_user(name, email, password):

    connection = sqlite3.connect("smart_notebook.db")
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (

                full_name,
                email,
                password,
                bio,
                university,
                department,
                skills

            )

            VALUES (?, ?, ?, '', '', '', '')
            """,
            (
                name,
                email,
                password
            )
        )

        connection.commit()

        return True

    except:

        return False

    finally:

        connection.close()


def login_user(email, password):

    connection = sqlite3.connect("smart_notebook.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = ? AND password = ?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user 

# =========================
# CREATE COMMUNITY TABLES
# =========================

def create_community_tables():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            note_id INTEGER,

            user_email TEXT,

            comment TEXT
        )
        """
    )

    conn.commit()

    conn.close()


# =========================
# MAKE NOTE PUBLIC
# =========================

def make_note_public(note_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notes
        SET is_public = 1
        WHERE id = ?
        """,
        (note_id,)
    )

    conn.commit()

    conn.close()


# =========================
# GET PUBLIC NOTES
# =========================

def get_public_notes():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, subject, content, user_email
        FROM notes
        WHERE is_public = 1
        """
    )

    notes = cursor.fetchall()

    conn.close()

    return notes


# =========================
# SEARCH PUBLIC NOTES
# =========================

def search_public_notes(keyword):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, subject, content, user_email
        FROM notes

        WHERE is_public = 1

        AND (

            title LIKE ?

            OR subject LIKE ?

            OR content LIKE ?

        )
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    notes = cursor.fetchall()

    conn.close()

    return notes


# =========================
# ADD COMMENT
# =========================

def add_comment(
    note_id,
    user_email,
    comment
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO comments (
            note_id,
            user_email,
            comment
        )
        VALUES (?, ?, ?)
        """,
        (
            note_id,
            user_email,
            comment
        )
    )

    conn.commit()

    conn.close()


# =========================
# GET COMMENTS
# =========================

def get_comments(note_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_email, comment
        FROM comments
        WHERE note_id = ?
        """,
        (note_id,)
    )

    comments = cursor.fetchall()

    conn.close()

    return comments

# =========================
# CREATE LIKES TABLE
# =========================

def create_like_table():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS likes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            note_id INTEGER,

            user_email TEXT
        )
        """
    )

    conn.commit()

    conn.close()


# =========================
# ADD LIKE
# =========================

def like_note(note_id, user_email):

    conn = connect_db()

    cursor = conn.cursor()

    # prevent duplicate like
    cursor.execute(
        """
        SELECT *
        FROM likes
        WHERE note_id = ?
        AND user_email = ?
        """,
        (note_id, user_email)
    )

    existing = cursor.fetchone()

    if not existing:

        cursor.execute(
            """
            INSERT INTO likes (
                note_id,
                user_email
            )
            VALUES (?, ?)
            """,
            (
                note_id,
                user_email
            )
        )

        conn.commit()

    conn.close()


# =========================
# COUNT LIKES
# =========================

def count_likes(note_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM likes
        WHERE note_id = ?
        """,
        (note_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count 

# =========================
# UPDATE PROFILE
# =========================

def update_profile(
    email,
    bio,
    university,
    department,
    skills
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users

        SET

            bio = ?,
            university = ?,
            department = ?,
            skills = ?

        WHERE email = ?
        """,
        (
            bio,
            university,
            department,
            skills,
            email
        )
    )

    conn.commit()

    conn.close()


# =========================
# GET PROFILE
# =========================

def get_profile(email):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            name,
            email,
            bio,
            university,
            department,
            skills

        FROM users

        WHERE email = ?
        """,
        (email,)
    )

    profile = cursor.fetchone()

    conn.close()

    return profile

# =========================
# GET USER BASIC INFO
# =========================

def get_user_basic_info(email):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            name,
            university,
            department

        FROM users

        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user 

# =========================
# GET PUBLIC NOTES OF USER
# =========================

def get_public_notes_by_user(email):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            title,
            subject,
            content

        FROM notes

        WHERE user_email = ?
        AND is_public = 1
        """,
        (email,)
    )

    notes = cursor.fetchall()

    conn.close()

    return notes 

# =========================
# CREATE FOLLOW TABLE
# =========================

def create_follow_table():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS follows (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            follower_email TEXT,

            following_email TEXT
        )
        """
    )

    conn.commit()

    conn.close()


# =========================
# FOLLOW USER
# =========================

def follow_user(
    follower_email,
    following_email
):

    conn = connect_db()

    cursor = conn.cursor()

    # Prevent duplicate follow

    cursor.execute(
        """
        SELECT *
        FROM follows

        WHERE follower_email = ?
        AND following_email = ?
        """,
        (
            follower_email,
            following_email
        )
    )

    existing = cursor.fetchone()

    if not existing:

        cursor.execute(
            """
            INSERT INTO follows (

                follower_email,
                following_email

            )
            VALUES (?, ?)
            """,
            (
                follower_email,
                following_email
            )
        )

        conn.commit()

    conn.close()


# =========================
# UNFOLLOW USER
# =========================

def unfollow_user(
    follower_email,
    following_email
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM follows

        WHERE follower_email = ?
        AND following_email = ?
        """,
        (
            follower_email,
            following_email
        )
    )

    conn.commit()

    conn.close()


# =========================
# CHECK FOLLOWING
# =========================

def is_following(
    follower_email,
    following_email
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM follows

        WHERE follower_email = ?
        AND following_email = ?
        """,
        (
            follower_email,
            following_email
        )
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# =========================
# FOLLOWER COUNT
# =========================

def get_follower_count(email):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM follows

        WHERE following_email = ?
        """,
        (email,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# =========================
# FOLLOWING COUNT
# =========================

def get_following_count(email):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM follows

        WHERE follower_email = ?
        """,
        (email,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# =========================
# SAVE NOTE
# =========================

def save_note(
    user_email,
    title,
    subject,
    content,
    original_file_path,
    pdf_path,
    file_type
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notes (

            user_email,
            title,
            subject,
            content,
            original_file_path,
            pdf_path,
            file_type

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_email,
            title,
            subject,
            content,
            original_file_path,
            pdf_path,
            file_type
        )
    )

    conn.commit()

    conn.close()


import os


def get_note_page_images(pdf_path):

    if not pdf_path:
        return []

    image_folder = "note_upload/page_images"

    if not os.path.exists(image_folder):
        return []

    pdf_name = os.path.splitext(
        os.path.basename(pdf_path)
    )[0]

    images = []

    for file in sorted(
        os.listdir(image_folder)
    ):

        if file.startswith(pdf_name):

            images.append(
                f"note_upload/page_images/{file}"
            )

    return images