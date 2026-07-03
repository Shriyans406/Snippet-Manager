from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_ROOT / "database" / "snippets.db"

SCAN_RESULTS = PROJECT_ROOT / "database" / "files.json"

LOG_DIRECTORY = PROJECT_ROOT / "logs"

SUPPORTED_EXTENSIONS = [
    ".py",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".json",
    ".xml",
    ".yaml",
    ".yml",
    ".md",
    ".sh",
    ".rs"
]