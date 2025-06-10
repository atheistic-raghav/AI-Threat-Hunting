import pandas as pd
import subprocess
import re
from utils.save_to_csv import save_to_csv

def collect_system_logs():
    """Collects Windows event logs and structures the data."""
    command = 'wevtutil qe System /c:10 /rd:true /f:text'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    data = []
    log_entry = {}
    
    for line in result.stdout.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # Extract key fields from logs
        if line.startswith("Log Name:"):
            log_entry["Log Name"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Date:"):
            log_entry["Timestamp"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Event ID:"):
            log_entry["Event ID"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Task:"):
            log_entry["Task"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Level:"):
            log_entry["Level"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Opcode:"):
            log_entry["Opcode"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Keyword:"):
            log_entry["Keyword"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Description:"):
            log_entry["Description"] = line.split(": ", 1)[1] if ": " in line else ""
        elif line.startswith("Event[" ):
            # Store the previous log entry and start a new one
            if log_entry:
                data.append(log_entry)
            log_entry = {"Log Entry": line}
    
    # Append the last log entry
    if log_entry:
        data.append(log_entry)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Convert Timestamp to datetime format if it exists
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    
    # Save to CSV
    save_to_csv(df, "csv_collection/windows_logs.csv")

if __name__ == "__main__":
    collect_system_logs()
