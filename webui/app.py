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

from snippet_collections.collection_manager import (
    create_collection,
    get_all_collections,
    add_file_to_collection,
    get_collection_files
)

from database.db_manager import (
    get_connection
)


import subprocess
import sqlite3

DATABASE_FILE = PROJECT_ROOT / "database" / "snippets.db"

app = Flask(__name__)


def search_database(query):

    connection = get_connection()

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

    connection = get_connection()

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
        highlighted=highlighted,
        css=get_style(),
        tags=get_tags(file_id),
        favorite=is_favorite(file_id),
        collections=get_all_collections()
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


@app.route(
    "/create_collection",
    methods=["POST"]
)
def create_collection_route():

    name = request.form["name"].strip()

    if name:

        create_collection(name)

    return redirect("/collections")


@app.route(
    "/add_to_collection",
    methods=["POST"]
)
def add_to_collection_route():

    file_id = int(
        request.form["file_id"]
    )

    collection_id = int(
        request.form["collection_id"]
    )

    add_file_to_collection(
        collection_id,
        file_id
    )

    return redirect(
        f"/snippet/{file_id}"
    )


@app.route("/collections")
def collections():

    return render_template(
        "collections.html",
        collections=get_all_collections()
    )

@app.route("/collection/<int:collection_id>")
def collection(collection_id):

    return render_template(
        "collection_files.html",
        files=get_collection_files(collection_id)
    )

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

    # TEST_PHASE_7

    # WATCHER_TEST