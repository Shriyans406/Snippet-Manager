#import sqlite3
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

#DATABASE_FILE = (
 #   PROJECT_ROOT /
 #   "database" /
 #   "snippets.db"
#)

from database.db_manager import (
    get_connection
)

def add_favorite(file_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE
        INTO favorites(file_id)

        VALUES(?)
        """,
        (file_id,)
    )

    connection.commit()

    connection.close()


def remove_favorite(file_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE
        FROM favorites

        WHERE file_id=?
        """,
        (file_id,)
    )

    connection.commit()

    connection.close()


def get_all_favorites():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

        files.id,
        files.filename,
        files.path,
        files.extension

        FROM files

        JOIN favorites

        ON files.id=favorites.file_id

        ORDER BY files.filename
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


def is_favorite(file_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM favorites

        WHERE file_id=?
        """,
        (file_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None