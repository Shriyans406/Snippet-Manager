import subprocess


subprocess.Popen(
    [
        "python",
        "watcher/file_watcher.py"
    ]
)

subprocess.run(
    [
        "python",
        "webui/app.py"
    ]
)