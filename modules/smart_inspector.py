import os
import sys
import subprocess
import hashlib
import datetime
import importlib.util
import shutil
import socket
import platform
import psutil
import webbrowser

# ===============================
# Ensure requests is installed
# ===============================
def ensure_requests():
    if importlib.util.find_spec("requests") is None:
        print("❌ 'requests' library not found.")
        choice = input("Install requests now? (Y/N) > ").lower()
        if choice == "y":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        else:
            print("Module cannot run without requests.")
            sys.exit(1)

ensure_requests()
import requests

# ===============================
# GLOBAL SETTINGS
# ===============================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

GLOBAL_HEADERS = {}
GLOBAL_PROXY = None

# ===============================
# UTILITY FUNCTIONS
# ===============================
def log_event(data):
    filename = os.path.join(LOG_DIR, f"smartinspector_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {data}\n")

def sha256_file(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return None

# ===============================
# LEGAL GATE
# ===============================
def legal_gate():
    print("""
⚠️  LEGAL WARNING – SYSTEM SCANS ⚠️

This module reads local files, processes, and network info.
Use ONLY on systems you OWN or have EXPLICIT permission for.

Type EXACTLY:
I TAKE FULL RESPONSIBILITY
""")
    return input("> ").strip() == "I TAKE FULL RESPONSIBILITY"

# ===============================
# SMART INSPECTOR MENU
# ===============================
def smart_inspector_menu():
    print("\n--- SMART INSPECTOR ---")
    print("[1] Local Malware Scan")
    print("[2] Port & Service Scan")
    print("[3] Process Inspector")
    print("[4] Smart Response Diffing")
    print("[5] Environment / Tool Check")
    print("[0] Back")

# ===============================
# FEATURE 1: LOCAL MALWARE SCAN
# ===============================
KNOWN_HASHES = {
    # Example safe demo hashes (replace with actual malware hashes if you maintain a db)
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Empty file / benign"
}

def local_malware_scan():
    path = input("Enter folder path to scan > ").strip()
    if not os.path.exists(path):
        print("❌ Path not found.")
        return
    print("\nScanning files...")
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            h = sha256_file(full_path)
            status = KNOWN_HASHES.get(h, "Unknown / Safe") if h else "Error"
            print(f"{full_path} -> {status}")
            log_event(f"MALWARE_SCAN | {full_path} | {status}")

# ===============================
# FEATURE 2: PORT & SERVICE SCAN
# ===============================
COMMON_PORTS = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS"}

def port_service_scan():
    target = input("Enter IP or hostname (default=localhost) > ").strip() or "127.0.0.1"
    print(f"\nScanning common ports on {target}...")
    for port, name in COMMON_PORTS.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((target, port))
            print(f"OPEN - {port} ({name})")
            log_event(f"PORT_SCAN | {target}:{port} OPEN ({name})")
        except:
            print(f"CLOSED - {port} ({name})")
            log_event(f"PORT_SCAN | {target}:{port} CLOSED ({name})")
        finally:
            s.close()

# ===============================
# FEATURE 3: PROCESS INSPECTOR
# ===============================
def process_inspector():
    print("\nListing top processes by CPU usage...")
    for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
        try:
            print(f"{p.info['pid']:5} | {p.info['name'][:25]:25} | {p.info['username'][:15]:15} | CPU={p.info['cpu_percent']}")
            log_event(f"PROCESS_INSPECT | PID={p.info['pid']} | NAME={p.info['name']} | USER={p.info['username']} | CPU={p.info['cpu_percent']}")
        except:
            continue

# ===============================
# FEATURE 4: SMART RESPONSE DIFFING (Demo)
# ===============================
SMART_HISTORY_FILE = os.path.join(LOG_DIR, "smart_diff_history.txt")

def smart_response_diff():
    url = input("Enter URL for diff check > ").strip()
    try:
        r = requests.get(url, headers=GLOBAL_HEADERS, proxies=GLOBAL_PROXY, timeout=5)
        content_hash = hashlib.sha256(r.content).hexdigest()
        old_hash = None
        if os.path.exists(SMART_HISTORY_FILE):
            with open(SMART_HISTORY_FILE, "r") as f:
                old_hash = f.readline().strip()
        with open(SMART_HISTORY_FILE, "w") as f:
            f.write(content_hash)
        if old_hash:
            status = "CHANGED" if old_hash != content_hash else "UNCHANGED"
            print(f"Content status: {status}")
            log_event(f"SMART_DIFF | URL={url} | {status}")
        else:
            print("History saved for next comparison.")
    except Exception as e:
        print(f"❌ Error fetching URL: {e}")

# ===============================
# FEATURE 5: ENVIRONMENT / TOOL CHECK
# ===============================
TOOLS = ["sqlmap", "nmap", "python", "pip"]

def environment_check():
    print("\n--- Environment & Tool Check ---")
    for t in TOOLS:
        path = shutil.which(t)
        status = f"Found at {path}" if path else "NOT found"
        print(f"{t:10} | {status}")
        log_event(f"ENV_CHECK | {t} | {status}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    log_event(f"ENV_CHECK | OS={platform.system()} | Python={platform.python_version()}")

# ===============================
# MAIN LOOP
# ===============================
def run_smart_inspector():
    if not legal_gate():
        print("Access denied.")
        return

    while True:
        smart_inspector_menu()
        choice = input("> ").strip()
        if choice == "0":
            break
        elif choice == "1":
            local_malware_scan()
        elif choice == "2":
            port_service_scan()
        elif choice == "3":
            process_inspector()
        elif choice == "4":
            smart_response_diff()
        elif choice == "5":
            environment_check()
        input("\nPress Enter to continue...")