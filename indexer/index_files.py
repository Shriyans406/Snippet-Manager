import json
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

JSON_FILE = PROJECT_ROOT / "data" / "files.json"

DATABASE_FILE = PROJECT_ROOT / "database" / "snippets.db"


def load_files():

    with open(JSON_FILE, "r") as file:
        return json.load(file)


def connect_database():

    return sqlite3.connect(DATABASE_FILE)


def insert_files(connection, files):

    cursor = connection.cursor()

    inserted = 0

    for file in files:

        try:

            cursor.execute(
                """
                INSERT OR IGNORE INTO files
                (
                    filename,
                    path,
                    extension,
                    size
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    file["filename"],
                    file["path"],
                    file["extension"],
                    file["size"]
                )
            )

            inserted += 1

        except Exception as error:

            print(error)

    connection.commit()

    return inserted


def main():

    print("Loading scan results...")

    files = load_files()

    print(f"Loaded {len(files)} records")

    connection = connect_database()

    inserted = insert_files(
        connection,
        files
    )

    connection.close()

    print(f"Indexed {inserted} files")


if __name__ == "__main__":
    main()