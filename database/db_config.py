import sqlite3
import os

def connect_db():

    print(
        "DB PATH:",
        os.path.abspath(
            "smart_notebook.db"
        )
    )

    conn = sqlite3.connect(
        "smart_notebook.db"
    )

    return conn