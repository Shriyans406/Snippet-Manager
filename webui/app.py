import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(
    str(PROJECT_ROOT)
)

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from tags.tag_manager import (
    add_tag,
    get_tags
)

from dashboard.status import (
    get_total_files
)

from dashboard.refresh_info import (
    get_refresh_time
)

from utils.highlighter import (
    highlight_code,
    get_style
)


from favorites.favorite_manager import (
    add_favorite,
    remove_favorite,
    get_all_favorites,
    is_favorite
)


import subprocess
import sqlite3

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
    "index.html",
    total_files=get_total_files(),
    refresh_time=get_refresh_time()
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

    code = result[5]

    if code is None:
        code = "File content unavailable."    

    highlighted = highlight_code(
     code,
     "python"
    )

    return render_template(
        "snippet.html",
        snippet=result,
        code=code,
        highlighted=highlighted,
        css=get_style(),
        tags=get_tags(file_id),
        favorite=is_favorite(file_id)
    )



@app.route("/refresh")
def refresh():

    subprocess.run(
        [
            "python",
            "indexer/update_changed_files.py"
        ]
    )

    return (
        "Index Refreshed"
    )

@app.route(
    "/add_tag",
    methods=["POST"]
)
def add_tag_route():

    file_id = int(
        request.form["file_id"]
    )

    tag = request.form["tag"].strip()

    if tag:

        add_tag(
            file_id,
            tag
        )

    return redirect(
        f"/snippet/{file_id}"
    )


@app.route("/favorite/<int:file_id>")
def favorite(file_id):

    if is_favorite(file_id):

        remove_favorite(file_id)

    else:

        add_favorite(file_id)

    return redirect(
        f"/snippet/{file_id}"
    )

@app.route("/favorites")
def favorites():

    results = get_all_favorites()

    return render_template(
        "favorites.html",
        results=results
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

    # TEST_PHASE_7

    # WATCHER_TEST