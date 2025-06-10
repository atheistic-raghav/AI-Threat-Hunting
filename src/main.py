from modules.data_collection import (
    externalUsb_collector, internalUsb_collector, network_collector,
    process_collector, registry_collector, syslog_collector,
    system_collector, file_monitor, scheduled_tasks_collector,
    running_services_collector, installed_software_collector
)
from modules.threat_detection import rule_based_detector  # 🔥 Import Threat Detection

def run_data_collection():
    """Runs all data collection modules."""
    print("\n🚀 Starting Data Collection...\n")

    externalUsb_collector.collect_external_usb()
    internalUsb_collector.collect_internal_usb()
    network_collector.collect_network_info()
    process_collector.collect_processes()
    registry_collector.collect_registry_info()
    syslog_collector.collect_system_logs()
    system_collector.collect_system_info()
    file_monitor.scan_directory()
    scheduled_tasks_collector.get_scheduled_tasks()
    running_services_collector.get_running_services()
    installed_software_collector.collect_installed_software()

    print("\n✅ Data Collection Complete!\n")

def run_threat_detection():
    """Runs rule-based threat detection after data collection."""
    print("\n🚨 Running Rule-Based Threat Detection...\n")
    rule_based_detector.main()

if __name__ == "__main__":
    run_data_collection()   # ✅ Step 1: Collect Data
    run_threat_detection()  # ✅ Step 2: Detect Threats
    print("\n✅ System Execution Complete!\n")
