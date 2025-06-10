import pandas as pd
import os
from tabulate import tabulate  # 🆕 Added for better table formatting

NETWORK_BLACKLIST_DATA = "blacklist/blacklistnetworkdata.txt"
EXTERNALUSB_BLACKLIST_DATA = "blacklist/blacklistexternalusbdata.txt"
INSTALLEDSOFTWARE_BLACKLIST_DATA = "blacklist/blacklistinstalledsoftware.txt"
PROCESS_BLACKLIST_DATA = "blacklist/blacklistprocessdata.txt"
RUNNINGSERVICES_BLACKLIST_DATA = "blacklist/blacklistrunningservices.txt"
SCHEDULEDTASKS_BLACKLIST_DATA = "blacklist/blacklistscheduledtasks.txt"
INTERNALUSB_BLACKLIST_DATA = "blacklist/blacklistinternalusbdata.txt"


def load_csv(file_path):
    """Loads CSV data into a DataFrame."""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

def  load_network_blacklist():
    """Loads blacklist ips from a file"""
    if os.path.exists(NETWORK_BLACKLIST_DATA):
        with open(NETWORK_BLACKLIST_DATA,"r") as file:
            return set(ip.strip() for ip in file.readlines())
    return set()

def load_externalusb_blacklist():
    """Loads blacklist external usb from a file"""
    if os.path.exists(EXTERNALUSB_BLACKLIST_DATA):
        with open(EXTERNALUSB_BLACKLIST_DATA,"r") as file:
            return set(instanceId.strip() for instanceId in file.readlines())
    return set()

def load_internalnalusb_blacklist():
    """Loads blacklist internal usb from a file"""
    if os.path.exists(INTERNALUSB_BLACKLIST_DATA):
        with open(INTERNALUSB_BLACKLIST_DATA,"r") as file:
            return set(usbDevice.strip() for usbDevice in file.readlines())
    return set()

def load_installedsoftware_blacklist():
    """Loads blacklist ips from a file"""
    if os.path.exists(INSTALLEDSOFTWARE_BLACKLIST_DATA):
        with open(INSTALLEDSOFTWARE_BLACKLIST_DATA,"r") as file:
            return set(softwareName.strip() for softwareName in file.readlines())
    return set()

def load_process_blacklist():
    """Loads blacklist process from a file"""
    if os.path.exists(PROCESS_BLACKLIST_DATA):
        with open(PROCESS_BLACKLIST_DATA,"r") as file:
            return set(processId.strip() for processId in file.readlines())
    return set()

def load_runningservices_blacklist():
    """loads blacklist running services from a file"""
    if os.path.exists(RUNNINGSERVICES_BLACKLIST_DATA):
        with open(RUNNINGSERVICES_BLACKLIST_DATA,"r") as file:
            return set(serviceName.strip() for serviceName in file.readlines())
    return set()

def load_scheduledtasks_blacklist():
    """loads blacklist scheduled tasks from a file"""
    if os.path.exists(SCHEDULEDTASKS_BLACKLIST_DATA):
        with open(SCHEDULEDTASKS_BLACKLIST_DATA,"r") as file:
            return set(taskName.strip() for taskName in file.readlines())
    return set()

def detect_suspicious_externalusb():
    """Detect unauthorized external USB device connections."""
    df = load_csv("csv_collection/external_usb_devices.csv")
    blacklisted_externalusb = load_externalusb_blacklist()
    print(blacklisted_externalusb)
    return df[df["Instance ID"].isin(blacklisted_externalusb)]

def detect_suspicious_internalusb():
    """Detect unauthorized internal USB device connections."""
    df = load_csv("csv_collection/internal_usb_devices.csv")
    blacklisted_internalusb = load_internalnalusb_blacklist()
    print(blacklisted_internalusb)
    return df[df["USB_Device"].isin(blacklisted_internalusb)]

def detect_suspicious_network():
    """Identify unusual network connections."""
    df = load_csv("csv_collection/network_data.csv")
    blacklisted_ips = load_network_blacklist()
    print( blacklisted_ips)
    return df[df["Remote Address"].isin(blacklisted_ips)]

def detect_suspicious_installed_software():
    """Flag newly installed or suspicious software."""
    df = load_csv("csv_collection/installed_software.csv")
    blacklisted_software = load_installedsoftware_blacklist()
    print( blacklisted_software)
    return df[df["Software Name"].isin(blacklisted_software)]

def detect_suspicious_processes():
    """Identify suspicious processes."""
    df = load_csv("csv_collection/process_data.csv")
    blacklisted_process = load_process_blacklist()
    print(blacklisted_process)
    df["PID"] = df["PID"].astype(str)
    return df[df["PID"].isin(blacklisted_process)]

def detect_running_services():
    """Check for suspicious running services."""
    df = load_csv("csv_collection/running_services.csv")
    blacklisted_runningservices = load_runningservices_blacklist()
    print(blacklisted_runningservices)
    return df[df["Service Name"].isin(blacklisted_runningservices)]

def detect_suspicious_scheduled_tasks():
    """Identify unauthorized or malicious scheduled tasks."""
    df = load_csv("csv_collection/scheduled_tasks.csv")
    blacklisted_scheduledtasks = load_scheduledtasks_blacklist()
    print(blacklisted_scheduledtasks)
    return df[df["Task Name"].isin(blacklisted_scheduledtasks)]

def detect_suspicious_files():
    """Detect unauthorized file modifications."""
    df = load_csv("csv_collection/file_monitor.csv")
    return df[df["Size (KB)"] > 100000]  # Flag files > 100MB

def detect_suspicious_registry_changes():
    """Identify registry changes linked to malware."""
    df = load_csv("csv_collection/registry_data.csv")
    return df[df["Registry Entry"].str.contains("runonce", case=False, na=False)]

def detect_suspicious_system_logs():
    """Identify critical or warning level system logs."""
    df = load_csv("csv_collection/windows_logs.csv")
    return df[df["Level"].str.contains("Critical|Error|Warning", case=False, na=False)]

def detect_system_anomalies():
    """Check for anomalies in system information like unexpected IP changes."""
    df = load_csv("csv_collection/system_info.csv")
    suspicious_ips = ["192.168.1.50", "10.0.0.150"]
    return df[df["IP Address"].isin(suspicious_ips)]

def main():
    """Run all rule-based detections and display results in table format."""
    
    ExternalUSB_Devices =  detect_suspicious_externalusb()
    InternalUSB_Devices = detect_suspicious_internalusb()
    Network_Connections = detect_suspicious_network()
    Installed_Software = detect_suspicious_installed_software()
    File_Changes = detect_suspicious_files()
    Running_Processes = detect_suspicious_processes()
    Registry_Changes= detect_suspicious_registry_changes()
    Running_Services= detect_running_services()
    Scheduled_Tasks = detect_suspicious_scheduled_tasks()
    System_Logs = detect_suspicious_system_logs()
    System_Info = detect_system_anomalies()
    # for category, df in detectors.items():
    #     if not df.empty:
    #         print(f"\n🚨 [ALERT] Suspicious {category} detected:")
    #         print(tabulate(df, headers="keys", tablefmt="grid"))
    #     else:
    #         print(f"\n✅ [OK] No suspicious {category} found.")

    
    if not ExternalUSB_Devices.empty:
        print("Suspicious External USB activity detected!")
        print(ExternalUSB_Devices)

    if not InternalUSB_Devices.empty:
        print("Suspicious Internal USB activity detected!")
        print(InternalUSB_Devices)

    if not Network_Connections.empty:
        print("Threat detected: Blacklisted IP found in network activity!")
        print(Network_Connections)
    
    if not Installed_Software.empty:
        print("Suspicious installed software detected!")
        print(Installed_Software)

    if not Running_Processes.empty:
        print("Suspicious running process detected!")
        print(Running_Processes)

    if not File_Changes.empty:
        print("Unauthorized file modifications detected!")
        print(File_Changes)

    if not Running_Services.empty:
        print("Suspicious running services detected!")
        print(Running_Services)

    if not Scheduled_Tasks.empty:
        print("Suspicious scheduled tasks detected!")
        print(Scheduled_Tasks)
    


if __name__ == "__main__":
    main()
