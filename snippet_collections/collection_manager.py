#import sqlite3
from pathlib import Path

#PROJECT_ROOT = (
 #   Path(__file__).resolve().parent.parent
#)

#DATABASE_FILE = (
 #   PROJECT_ROOT /
  #  "database" /
   # "snippets.db"
#)
from database.db_manager import (
    get_connection
)

def create_collection(name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE
        INTO collections(name)

        VALUES(?)
        """,
        (name,)
    )

    connection.commit()

    connection.close()


def get_all_collections():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name

        FROM collections

        ORDER BY name
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def add_file_to_collection(
    collection_id,
    file_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE
        INTO collection_files

        VALUES(
            ?,
            ?
        )
        """,
        (
            collection_id,
            file_id
        )
    )

    connection.commit()

    connection.close()


def get_collection_files(
    collection_id
):

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

        JOIN collection_files

        ON files.id =
        collection_files.file_id

        WHERE
        collection_files.collection_id=?
        """,
        (collection_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows