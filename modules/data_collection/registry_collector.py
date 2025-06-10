import pandas as pd
import subprocess
from utils.save_to_csv import save_to_csv

def collect_registry_info():
    """Collects registry startup items."""
    command = 'reg query HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    data = []
    for line in result.stdout.split("\n"):
        if line.strip():
            data.append({"Registry Entry": line.strip(), "Timestamp": pd.Timestamp.now()})

    save_to_csv(data, "csv_collection/registry_data.csv")

if __name__ == "__main__":
    collect_registry_info()
