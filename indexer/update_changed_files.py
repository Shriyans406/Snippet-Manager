import sqlite3
from pathlib import Path

from database.db_manager import (
    get_connection
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_ROOT / "database" / "snippets.db"


def main():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            path,
            last_modified
        FROM files
        """
    )

    rows = cursor.fetchall()

    updated = 0

    for file_id, path, db_modified in rows:

        try:

            file_path = Path(path)

            if not file_path.exists():
                continue

            current_modified = (
                file_path.stat().st_mtime
            )

            if current_modified != db_modified:

                with open(
                    file_path,
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

                    SET
                        content=?,
                        line_count=?,
                        last_modified=?

                    WHERE id=?
                    """,
                    (
                        content,
                        line_count,
                        current_modified,
                        file_id
                    )
                )

                updated += 1

        except Exception as error:

            print(error)

    connection.commit()

    connection.close()

    print(
        f"Updated {updated} changed files"
    )


if __name__ == "__main__":
    main()