import subprocess
import pandas as pd
import csv
from datetime import datetime
from utils.save_to_csv import save_to_csv

def get_scheduled_tasks():
    """Fetches Windows Scheduled Tasks."""

    try:
        command = [
            "powershell", 
            "-Command", 
            "Get-ScheduledTask | Select-Object TaskName, TaskPath, State | ConvertTo-Csv -NoTypeInformation"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        lines = result.stdout.strip().split("\n")[1:]  # Ignore headers
        tasks = []

        for line in csv.reader(lines):  # More reliable CSV parsing
            if len(line) >= 3:
                tasks.append({
                    "Task Name": line[0].strip().strip('"'),  # Clean up potential quotes
                    "Task Path": line[1].strip().strip('"'),
                    "State": line[2].strip(),
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        if tasks:
            save_to_csv(tasks, "csv_collection/scheduled_tasks.csv")
            print(f"✅ {len(tasks)} scheduled tasks saved!")
        else:
            print("⚠️ No scheduled tasks found.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing PowerShell command: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    get_scheduled_tasks()
