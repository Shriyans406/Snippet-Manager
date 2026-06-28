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
    CREATE TABLE IF NOT EXISTS favorites(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        file_id INTEGER UNIQUE,

        FOREIGN KEY(file_id)
        REFERENCES files(id)
    )
    """
)

connection.commit()

connection.close()

print(
    "Favorites table created successfully."
)