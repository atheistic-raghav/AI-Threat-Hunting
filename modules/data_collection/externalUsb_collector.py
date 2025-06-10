# import pandas as pd
# import subprocess
# from utils.save_to_csv import save_to_csv

# def collect_external_usb():
#     """Collects information about external USB devices, even on Windows 11."""
    
#     try:
#         # Use PowerShell to list external USB devices
#         command = 'powershell "Get-PnpDevice -Class USB | Select-Object Name,Status,InstanceId"'
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)

#         data = []
#         lines = result.stdout.strip().split("\n")[2:]  # Ignore headers

#         for line in lines:
#             parts = line.split()
#             if len(parts) >= 3:
#                 device_name = " ".join(parts[:-2])  # Handles multi-word device names
#                 status = parts[-2]
#                 instance_id = parts[-1]

#                 data.append({
#                     "Device Name": device_name,
#                     "Status": status,
#                     "Instance ID": instance_id,
#                     "Timestamp": pd.Timestamp.now()
#                 })

#         # If no devices found, print a warning instead of saving an empty CSV
#         if not data:
#             print("⚠️ No external USB devices detected!")
#         else:
#             save_to_csv(data, "csv_collection/external_usb_devices.csv")

#     except Exception as e:
#         print(f"❌ Error collecting external USB data: {e}")

# if __name__ == "__main__":
#     collect_external_usb()
import pandas as pd
import subprocess
import csv
from io import StringIO
from utils.save_to_csv import save_to_csv

def collect_external_usb():
    """Collects information about external USB devices, even on Windows 11."""

    try:
        # PowerShell command with CSV output
        command = ('powershell -Command "Get-PnpDevice -PresentOnly | '
                   'Where-Object { $_.InstanceId -match \'USB\' } | '
                   'Select-Object Name,Status,InstanceId | ConvertTo-Csv -NoTypeInformation"')

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Convert CSV output into structured data
        csv_data = list(csv.DictReader(StringIO(result.stdout)))

        # Process & structure data
        data = []
        for row in csv_data:
            data.append({
                "Device Name": row["Name"].strip(),
                "Status": row["Status"].strip(),
                "Instance ID": row["InstanceId"].strip(),
                "Timestamp": pd.Timestamp.now()
            })

        # Save only if devices are found
        if not data:
            print("⚠️ No external USB devices detected!")
        else:
            save_to_csv(data, "csv_collection/external_usb_devices.csv")

    except Exception as e:
        print(f"❌ Error collecting external USB data: {e}")

if __name__ == "__main__":
    collect_external_usb()
