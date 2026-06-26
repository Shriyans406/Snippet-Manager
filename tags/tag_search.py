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


def search_by_tag(
    tag
):

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            files.id,
            files.filename

        FROM files

        JOIN tags

        ON files.id = tags.file_id

        WHERE tags.tag = ?
        """,
        (tag,)
    )

    results = cursor.fetchall()

    connection.close()

    return results