import pandas as pd
import subprocess
import csv
from io import StringIO
from utils.save_to_csv import save_to_csv

def collect_installed_software():
    """Collects details of installed software on Windows efficiently."""
    try:
        # PowerShell command to get installed software from registry
        command = ('powershell -Command "Get-ItemProperty '
                   '-Path \'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*\','
                   '\'HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*\' '
                   '| Select-Object DisplayName, DisplayVersion, Publisher '
                   '| ConvertTo-Csv -NoTypeInformation"')

        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")

        # Convert CSV output into structured data
        csv_data = list(csv.DictReader(StringIO(result.stdout)))

        data = []
        for row in csv_data:
            if row["DisplayName"]:  # Skip empty software names
                data.append({
                    "Software Name": row["DisplayName"].strip(),
                    "Version": row.get("DisplayVersion", "").strip(),
                    "Vendor": row.get("Publisher", "").strip(),
                    "Timestamp": pd.Timestamp.now()
                })

        # Save only if software is found
        if data:
            save_to_csv(data, "csv_collection/installed_software.csv")
            print(f"✅ Installed software list saved! ({len(data)} records)")
        else:
            print("⚠️ No installed software detected!")

    except Exception as e:
        print(f"❌ Error collecting installed software: {e}")

if __name__ == "__main__":
    collect_installed_software()
