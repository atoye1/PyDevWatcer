import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

####################################################
#     main.py 파일을 감시하고 변동시 재시작하는 watcher    #
####################################################


class MyHandler(FileSystemEventHandler):

    def __init__(self, target_files):
        self.target_files = target_files
        self.current_process = None

    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.src_path in self.target_files:
            print(f"Change detected: {event.src_path}")
            if self.current_process:
                self.current_process.terminate()
            self.current_process = restart_application()


def restart_application():
    # Replace 'your_app.py' with the main script or entry point of your PySide application.
    return subprocess.Popen(["python", "main.py"])


if __name__ == "__main__":
    target_files = ['main.py']
    target_files = [os.getcwd() + '/' + i for i in target_files]
    event_handler = MyHandler(target_files)
    observer = Observer()
    # Replace 'your_project_directory' with the path to your project directory.
    observer.schedule(
        event_handler, path=os.getcwd(), recursive=True)
    observer.start()
    event_handler.current_process = restart_application()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
