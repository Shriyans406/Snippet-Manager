# Snippet Manager

Snippet Manager is a local code search tool for Linux. It scans your source files, stores them in SQLite, and gives you a simple web interface to search, open, and copy code quickly.

It is meant to solve a very common problem: code snippets end up scattered across old projects, notes, bookmarks, and random folders. Instead of searching manually every time, you can index your code once and find it again in seconds.

## What this project does

* scans folders for code files
* stores file metadata in SQLite
* stores file content for search
* lets you search from the terminal
* provides a Flask web interface
* shows code in a readable snippet viewer
* supports copy to clipboard
* adds syntax highlighting
* supports tags, favorites, and collections
* supports incremental updates and file watching

## How to use it

### 1. Set up the project

Make sure you are inside the project folder and your virtual environment is active.

Install the required Python packages:

```bash
pip install flask pygments watchdog
```

If you are starting from a fresh clone, also make sure SQLite is available on your system.

### 2. Choose what to scan

Open `config/settings.json` and set the directories you want Snippet Manager to scan.

Example:

```json
{
  "scan_directories": [
    "/home/vboxuser/projects"
  ],
  "supported_extensions": [
    ".py",
    ".js",
    ".ts",
    ".rs",
    ".c",
    ".cpp",
    ".java",
    ".css",
    ".html"
  ],
  "database_path": "../database/snippets.db",
  "web_port": 8000
}
```

### 3. Scan your files

Run the scanner to collect a list of code files:

```bash
python scanner/scan.py
```

This creates or refreshes the generated file list in the `data/` folder.

### 4. Build the database index

Create the metadata index:

```bash
python indexer/index_files.py
```

Then store the file contents:

```bash
python indexer/index_content.py
```

### 5. Search from the terminal

You can test search directly from the command line:

```bash
python search/search.py sqlite
```

You can also try filters such as:

```bash
python search/search.py "sqlite ext:py"
python search/search.py "sqlite lang:python"
python search/search.py "connect_db"
```

### 6. Start the web interface

Run the Flask app:

```bash
python webui/app.py
```

Then open the browser at:

```text
http://localhost:8000
```

From the web interface you can:

* search snippets
* open a snippet
* view code with syntax highlighting
* copy the code
* add tags
* mark snippets as favorites
* organize snippets into collections

### 7. Keep the index updated

If file watching is enabled, Snippet Manager can update the database when files change. Otherwise, you can refresh the index manually using the provided update script or the refresh button in the web UI.

## Project structure

* `scanner/` — scans folders and saves file lists
* `indexer/` — stores metadata and file content in SQLite
* `search_engine/` — query parsing and advanced search logic
* `webui/` — Flask app and HTML templates
* `utils/` — shared helpers like syntax highlighting
* `tags/` — tag storage and tag search
* `favorites/` — favorite snippets
* `snippet_collections/` — custom snippet collections
* `watcher/` — file watching and auto refresh
* `dashboard/` — status and summary helpers
* `database/` — SQLite database and connection helper
* `config/` — project settings
* `data/` — generated scan results
* `logs/` — runtime logs

## Requirements

* Python 3.13 or newer
* SQLite3
* Flask
* Pygments
* Watchdog

Some parts of the project may also use Bash and Rust.

## Typical workflow

1. Add your project folders to the scan list.
2. Run the scanner.
3. Build the database index.
4. Start the web app.
5. Search for a snippet.
6. Open it in the browser.
7. Copy it or organize it with tags, favorites, and collections.

## Notes

This is a local personal tool. It keeps your data on your machine and is designed to be simple, fast, and easy to extend.

## Development status

The project is being built in phases. Each phase adds a new piece of functionality and improves the overall workflow.

## Troubleshooting

* If the web app does not start, check that your virtual environment is active and Flask is installed.
* If a snippet page fails to open, make sure the database contains file content for that file.
* If the collections page shows a missing table error, run the collection table creation script again.
* If imports fail, make sure you are running commands from the project root.

## License

Add your preferred license here.
