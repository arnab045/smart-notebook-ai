from database.db_config import connect_db

def register_user(full_name, email, password):

    conn = connect_db()

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users (full_name, email, password)
        VALUES (?, ?, ?)
        """, (full_name, email, password))

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def login_user(email, password):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user