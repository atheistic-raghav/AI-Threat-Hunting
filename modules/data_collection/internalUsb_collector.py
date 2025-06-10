import pandas as pd
import subprocess
import re
from utils.save_to_csv import save_to_csv

def collect_internal_usb():
    """Collects internal USB device information with cleaned IDs."""
    try:
        command = ["wmic", "path", "Win32_USBControllerDevice", "get", "Dependent"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        lines = result.stdout.strip().split("\n")[1:]  # Ignore header
        data = []

        for line in lines:
            match = re.search(r'Win32_PnPEntity.DeviceID="(USB\\[^"]+)"', line)
            if match:
                device_id = match.group(1)
                data.append({
                    "USB_Device": device_id,
                    "Timestamp": pd.Timestamp.now()
                })

        if data:
            save_to_csv(data, "csv_collection/internal_usb_devices.csv")
            print(f"✅ {len(data)} USB devices saved!")
        else:
            print("⚠️ No USB devices found.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing WMIC command: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    collect_internal_usb()
