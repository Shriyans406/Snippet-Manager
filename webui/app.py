from flask import Flask
from flask import render_template
from flask import request

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_ROOT / "database" / "snippets.db"

app = Flask(__name__)


def search_database(query):

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    search_term = f"%{query}%"

    cursor.execute(
        """
        SELECT
            id,
            filename,
            path,
            extension,
            line_count

        FROM files

        WHERE

            filename LIKE ?
            OR path LIKE ?
            OR content LIKE ?

        LIMIT 50
        """,
        (
            search_term,
            search_term,
            search_term
        )
    )

    results = cursor.fetchall()

    connection.close()

    return results


def get_file_by_id(file_id):

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            path,
            extension,
            line_count,
            content

        FROM files

        WHERE id = ?
        """,
        (file_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/search")
def search():

    query = request.args.get(
        "q",
        ""
    )

    results = search_database(
        query
    )

    return render_template(
        "results.html",
        query=query,
        results=results
    )


@app.route("/snippet/<int:file_id>")
def snippet(file_id):

    result = get_file_by_id(
        file_id
    )

    return render_template(
        "snippet.html",
        snippet=result
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )