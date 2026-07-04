#import sqlite3
from pathlib import Path

from database.db_manager import (
    get_connection
)

#PROJECT_ROOT = (
 #   Path(__file__)
  #  .resolve()
   # .parent
    #.parent
#)

#DATABASE_FILE = (
 #   PROJECT_ROOT
  #  / "database"
   # / "snippets.db"
#)


def add_tag(
    file_id,
    tag
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tags
        (
            file_id,
            tag
        )
        VALUES
        (
            ?,
            ?
        )
        """,
        (
            file_id,
            tag
        )
    )

    connection.commit()

    connection.close()

    print(
        "Tag added"
    )


def get_tags(
    file_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT tag
        FROM tags
        WHERE file_id = ?
        """,
        (file_id,)
    )

    tags = cursor.fetchall()

    connection.close()

    return tags