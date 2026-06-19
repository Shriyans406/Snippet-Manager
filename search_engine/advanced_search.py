import sqlite3

from pathlib import Path

from query_parser import (
    parse_query
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


LANGUAGE_MAP = {

    "python": ".py",

    "javascript": ".js",

    "rust": ".rs",

    "c": ".c",

    "cpp": ".cpp"
}


def search(query):

    parsed = parse_query(
        query
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    sql = """

    SELECT

        id,
        filename,
        path,
        extension,
        line_count

    FROM files

    WHERE

        content LIKE ?

    """

    params = [
        f"%{parsed['text']}%"
    ]

    if parsed["extension"]:

        sql += (
            " AND extension = ?"
        )

        params.append(
            "." +
            parsed["extension"]
        )

    if parsed["language"]:

        ext = LANGUAGE_MAP.get(
            parsed["language"]
        )

        if ext:

            sql += (
                " AND extension = ?"
            )

            params.append(
                ext
            )

    sql += """

    ORDER BY

        CASE

            WHEN filename LIKE ?
            THEN 1

            ELSE 2

        END

    """

    params.append(
        f"%{parsed['text']}%"
    )

    cursor.execute(
        sql,
        params
    )

    results = cursor.fetchall()

    connection.close()

    return results