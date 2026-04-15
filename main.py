import os
import shutil
import time
import sys
import threading
import tkinter as tk
import platform
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE_DIR = Path.home() / "Downloads"
CURRENT_SCRIPT = Path(sys.argv[0]).resolve()
OS_SYSTEM = platform.system()

CATEGORIES = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".tiff", ".psd"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v", ".mpeg"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".midi"],
    "Documents": [
        ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".txt", ".pptx", ".ppt", ".csv", ".md",
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".exe", ".msi", ".bat", ".cmd", ".ps1", ".dll",
        ".py", ".lua", ".js", ".html", ".css", ".json", ".ini", ".cfg", ".xml", ".sql"
    ]
}

def show_windows_toast(filename, category):
    def _toast():
        root = tk.Tk()
        root.overrideredirect(True) 
        root.attributes("-topmost", True) 
        root.configure(bg="#121212") 
        
        w, h = 320, 80
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        
        x = ws - w - 20
        y = hs - h - 60
        root.geometry(f"{w}x{h}+{x}+{y}")
        
        tk.Label(root, text="[ System: Auto-Organizer ]", fg="#8A2BE2", bg="#121212", font=("Consolas", 10, "bold")).pack(pady=5)
        tk.Label(root, text=f"File: {filename}\nDestination: {category}", fg="#FFFFFF", bg="#121212", font=("Consolas", 9)).pack()
        
        root.after(3500, root.destroy)
        root.mainloop()
        
    threading.Thread(target=_toast, daemon=True).start()

def notify(filename, category):
    if OS_SYSTEM == "Windows":
        show_windows_toast(filename, category)
    elif OS_SYSTEM == "Linux":
        try:
            subprocess.run(["notify-send", "-a", "Auto-Organizer", f"Moved file: {filename}", f"Destination: {category}"])
        except Exception:
            pass

class OrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.process_file(event)

    def on_moved(self, event):
        self.process_file(event, is_moved=True)

    def process_file(self, event, is_moved=False):
        if event.is_directory:
            return
        
        time.sleep(0.5) 
        filepath = Path(event.dest_path if is_moved else event.src_path)

        if not filepath.exists():
            return

        if filepath.suffix.lower() in [".crdownload", ".part", ".tmp"] or filepath.resolve() == CURRENT_SCRIPT:
            return

        extension = filepath.suffix.lower()

        for folder_name, exts in CATEGORIES.items():
            if extension in exts:
                target_dir = Path.home() / folder_name
                target_dir.mkdir(exist_ok=True)
                
                final_destination = target_dir / filepath.name
                counter = 1
                
                while final_destination.exists():
                    final_destination = target_dir / f"{filepath.stem}_{counter}{filepath.suffix}"
                    counter += 1
                
                try:
                    shutil.move(str(filepath), str(final_destination))
                    notify(filepath.name, folder_name)
                except Exception:
                    pass
                return

def start_observer():
    event_handler = OrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, str(SOURCE_DIR), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_observer()