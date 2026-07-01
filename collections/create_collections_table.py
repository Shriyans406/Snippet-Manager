import sqlite3
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

DATABASE_FILE = (
    PROJECT_ROOT /
    "database" /
    "snippets.db"
)

connection = sqlite3.connect(
    DATABASE_FILE
)

cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS collections(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS collection_files(

        collection_id INTEGER,

        file_id INTEGER,

        PRIMARY KEY(
            collection_id,
            file_id
        ),

        FOREIGN KEY(collection_id)
        REFERENCES collections(id),

        FOREIGN KEY(file_id)
        REFERENCES files(id)
    )
    """
)

connection.commit()

connection.close()

print(
    "Collections created successfully."
)