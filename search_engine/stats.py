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
    SELECT COUNT(*)
    FROM files
    """
)

print(
    "Total Files:",
    cursor.fetchone()[0]
)

connection.close()