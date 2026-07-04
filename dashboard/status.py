import sqlite3

from pathlib import Path

from database.db_manager import (
    get_connection
)


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


def get_total_files():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM files
        """
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total