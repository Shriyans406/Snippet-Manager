import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_ROOT / "database" / "snippets.db"


def connect_database():

    return sqlite3.connect(DATABASE_FILE)


def update_content(connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, path
        FROM files
        """
    )

    rows = cursor.fetchall()

    updated = 0

    for file_id, path in rows:

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                content = file.read()

            line_count = len(
                content.splitlines()
            )

            cursor.execute(
                """
                UPDATE files
                SET content = ?,
                    line_count = ?
                WHERE id = ?
                """,
                (
                    content,
                    line_count,
                    file_id
                )
            )

            updated += 1

        except Exception as error:

            print(
                f"Skipped {path}"
            )

            print(error)

    connection.commit()

    return updated


def main():

    print(
        "Starting content indexing..."
    )

    connection = connect_database()

    updated = update_content(
        connection
    )

    connection.close()

    print(
        f"Indexed content for {updated} files"
    )


if __name__ == "__main__":
    main()