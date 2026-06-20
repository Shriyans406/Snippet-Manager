import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(
    FileSystemEventHandler
):

    def on_modified(
        self,
        event
    ):

        if event.is_directory:

            return

        print()

        print(
            "=" * 50
        )

        print(
            "File changed:"
        )

        print(
            event.src_path
        )

        print()

        print(
            "Updating database..."
        )

        try:

            subprocess.run(
                [
                    "python",
                    "indexer/update_changed_files.py"
                ]
            )

            print(
                "Update complete"
            )

        except Exception as error:

            print(
                error
            )


observer = Observer()

handler = ChangeHandler()

observer.schedule(
    handler,
    path=".",
    recursive=True
)

observer.start()

print()

print(
    "Watcher Started"
)

print(
    "Monitoring Files..."
)

print()

try:

    while True:

        time.sleep(
            1
        )

except KeyboardInterrupt:

    observer.stop()

observer.join()