import pandas as pd
import platform
import socket
import psutil
from utils.save_to_csv import save_to_csv

def collect_system_info():
    """Collects basic system information."""
    data = {
        "OS": platform.system(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "Boot Time": pd.Timestamp(psutil.boot_time(), unit="s"),
        "Timestamp": pd.Timestamp.now()
    }

    save_to_csv([data], "csv_collection/system_info.csv")

if __name__ == "__main__":
    collect_system_info()
