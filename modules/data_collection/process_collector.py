import pandas as pd
import psutil
from utils.save_to_csv import save_to_csv

def collect_processes():
    """Collects running process details."""
    data = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):  # ✅ Correct way
        try:
            process_info = proc.info
            data.append({
                "PID": str(process_info["pid"]),  # Convert PID to string
                "Process Name": process_info["name"],
                "User": process_info["username"],
                "Timestamp": pd.Timestamp.now()
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    save_to_csv(data, "csv_collection/process_data.csv")

if __name__ == "__main__":
    collect_processes()
