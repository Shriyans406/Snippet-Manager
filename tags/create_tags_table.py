import sqlite3
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATABASE_FILE = (
    PROJECT_ROOT
    / "database"
    / "snippets.db"
)


connection = sqlite3.connect(
    DATABASE_FILE
)

cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tags (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        file_id INTEGER NOT NULL,

        tag TEXT NOT NULL,

        FOREIGN KEY(file_id)
        REFERENCES files(id)
    )
    """
)

connection.commit()

connection.close()

print(
    "Tags table created"
)