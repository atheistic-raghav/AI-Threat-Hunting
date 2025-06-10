import subprocess
import pandas as pd
import csv
from datetime import datetime
from utils.save_to_csv import save_to_csv

def get_running_services():
    """Fetches only running Windows services and saves them to a CSV file."""
    try:
        command = [
            "powershell", 
            "-Command", 
            "Get-Service | Where-Object { $_.Status -eq 'Running' } | Select-Object DisplayName, Name, Status | ConvertTo-Csv -NoTypeInformation"
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        lines = result.stdout.strip().split("\n")[1:]  # Ignore headers
        services = []

        for line in csv.reader(lines):  # Safer CSV parsing
            if len(line) >= 3:
                services.append({
                    "Service Name": line[0].strip(),
                    "Short Name": line[1].strip(),
                    "Status": line[2].strip(),
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        if services:
            save_to_csv(services, "csv_collection/running_services.csv")
            print(f"✅ {len(services)} running services saved!")
        else:
            print("⚠️ No running services found.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing PowerShell command: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    get_running_services()
