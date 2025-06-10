import pandas as pd
import subprocess
import re
from utils.save_to_csv import save_to_csv

def get_default_gateway():
    """Finds the default gateway (router's IP) using ipconfig, handling multi-line output."""
    command = "ipconfig"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    lines = result.stdout.split("\n")
    for i in range(len(lines)):
        if "Default Gateway" in lines[i]:
            # Check the current and next line for an IPv4 address
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", lines[i]) or \
                    (i + 1 < len(lines) and re.search(r"(\d+\.\d+\.\d+\.\d+)", lines[i + 1]))

            if match:
                return match.group(1)
    return "Unknown"

def collect_network_info():
    """Collects active network connections and finds the router's IP."""
    command = "netstat -ano"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    data = []
    for line in result.stdout.split("\n"):
        parts = line.split()
        if len(parts) >= 5:
            data.append({
                "Protocol": parts[0],
                "Local Address": parts[1],
                "Remote Address": parts[2],
                "Status": parts[3],
                "PID": parts[4],
                "Timestamp": pd.Timestamp.now()
            })
    
    # Get the router IP and add it to the CSV as a separate row
    router_ip = get_default_gateway()
    data.append({
        "Protocol": "N/A",
        "Local Address": "Your System",
        "Remote Address": router_ip,
        "Status": "Router IP",
        "PID": "N/A",
        "Timestamp": pd.Timestamp.now()
    })

    save_to_csv(data, "csv_collection/network_data.csv")

if __name__ == "__main__":
    collect_network_info()
