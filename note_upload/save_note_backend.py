from database.db_config import connect_db

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