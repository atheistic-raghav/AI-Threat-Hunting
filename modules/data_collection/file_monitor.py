import os
import time
import hashlib
import pandas as pd
from utils.save_to_csv import save_to_csv

# Allow user to define directory dynamically
MONITOR_DIR = "C:\\Users\\Public\\Documents"

def get_file_hash(filepath, chunk_size=8192):
    """Generate SHA-256 hash of a file in chunks (memory efficient)."""
    try:
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError, OSError):
        return None  # Return None if file cannot be accessed

def scan_directory(directory=MONITOR_DIR):
    """Scan directory and return file metadata safely."""
    data = []
    
    if not os.path.exists(directory):
        print(f"❌ Error: Directory '{directory}' not found!")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                file_size = os.path.getsize(filepath)
                file_hash = get_file_hash(filepath)
                data.append({
                    "Filename": file,
                    "Path": filepath,
                    "Size (KB)": round(file_size / 1024, 2),
                    "Hash": file_hash,
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
            except (PermissionError, FileNotFoundError, OSError):
                print(f"⚠️ Skipping inaccessible file: {filepath}")

    if data:
        save_to_csv(data, "csv_collection/file_monitor.csv")
        print(f"✅ File monitoring data saved! ({len(data)} files)")
    else:
        print("⚠️ No accessible files found in the directory.")

if __name__ == "__main__":
    scan_directory()
