import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_FILE = PROJECT_ROOT / "config" / "settings.json"

OUTPUT_FILE = PROJECT_ROOT / "data" / "files.json"


def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def scan_directories(directories, extensions):

    discovered_files = []

    for directory in directories:

        root = Path(directory)

        if not root.exists():
            print(f"Directory not found: {directory}")
            continue

        for file_path in root.rglob("*"):

            if file_path.is_file():

                if file_path.suffix.lower() in extensions:

                    discovered_files.append(
                        {
                            "filename": file_path.name,
                            "path": str(file_path),
                            "extension": file_path.suffix,
                            "size": file_path.stat().st_size
                        }
                    )

    return discovered_files


def save_results(files):

    with open(OUTPUT_FILE, "w") as file:

        json.dump(
            files,
            file,
            indent=4
        )


def main():

    config = load_config()

    directories = config["scan_directories"]

    extensions = config["supported_extensions"]

    print("Starting scan...")
    print()

    files = scan_directories(
        directories,
        extensions
    )

    print(f"Found {len(files)} files")

    save_results(files)

    print(
        f"Results saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()