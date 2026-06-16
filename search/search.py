import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT=Path(__file__).resolve().parent.parent
DATABASE_FILE=PROJECT_ROOT / "database" / "snippets.db"


def search_database(query):
    connection=sqlite3.connect(
        DATABASE_FILE
    )

    cursor=connection.cursor()

    search_term=f"%{query}%"

    cursor.execute(
        """
        SELECT
            filename,
            path,
            extension,
            line_count
        
        FROM files

        WHERE


            filename LIKE ?
            OR path LIKE ?
            OR content LIKE ?

        LIMIT 20
        """,
        (
            search_term,
            search_term,
            search_term
        )
    )

    results=cursor.fetchall()

    connection.close()

    return results


def print_results(results):
    print()
    print ("="*60)

    print(
        f"Found{len(results)} matches"
    )

    print("="*60)

    for index, result in enumerate(results, start=1):

        filename, path, extension, lines=result

        print()

        print(f"[{index}] {filename}")

        print(f"Path      :  {path}")

        print(f"Extension      :  {extension}")

        print(f"Lines      :  {lines}")

    print()

def main():

    if len(sys.argv)<2:
        print(
            "Usage:"
        )

        print(
            "python serach/search.py keyword"
        )

        return 

    query= " ".join(sys.argv[1:])

    results=search_database(
        query
    )

    print_results(
        results
    )


if __name__ == "__main__":
    main()


