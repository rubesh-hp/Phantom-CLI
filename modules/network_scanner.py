import subprocess
import socket
import shutil
import platform
import os

# ---------------- MENU ----------------
def network_menu():
    print("\n--- NETWORK SCANNER ---")
    print("[1] Ping Scan")
    print("[2] Port Scan (Nmap)")
    print("[3] Service Version Scan")
    print("[4] OS Detection")
    print("[5] Default Port Scanner (Python)")
    print("[0] Back")

# ---------------- NMAP DETECTION ----------------
def detect_nmap():
    # Try PATH first
    nmap_path = shutil.which("nmap")
    
    # Windows common folders fallback
    if not nmap_path and platform.system() == "Windows":
        possible_paths = [
            r"C:\Program Files (x86)\Nmap\nmap.exe",
            r"C:\Program Files\Nmap\nmap.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                nmap_path = path
                break

    return nmap_path

# ---------------- NMAP RUNNER ----------------
def run_nmap(args):
    nmap_path = detect_nmap()
    if not nmap_path:
        print("❌ Nmap is not installed or not in PATH")
        print("👉 Install Nmap and add it to PATH:")
        print("   https://nmap.org/download.html")
        return
    
    try:
        subprocess.run([nmap_path] + args)
    except Exception as e:
        print("❌ Error running Nmap:", e)

# ---------------- FEATURES ----------------

# 1️⃣ Ping Scan
def ping_scan():
    target = input("Enter IP or Subnet (e.g. 192.168.1.0/24) > ")
    run_nmap(["-sn", target])

# 2️⃣ Basic Port Scan
def port_scan():
    target = input("Enter target IP/domain > ")
    run_nmap([target])

# 3️⃣ Service Version Scan
def service_version_scan():
    target = input("Enter target IP/domain > ")
    run_nmap(["-sV", target])

# 4️⃣ OS Detection
def os_detection():
    target = input("Enter target IP/domain > ")
    run_nmap(["-O", target])

# 5️⃣ Pure Python Port Scanner
def python_port_scanner():
    target = input("Enter target IP > ")
    start_port = int(input("Start port > "))
    end_port = int(input("End port > "))

    print("\nScanning ports...\n")
    try:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))

            if result == 0:
                print(f"[OPEN] Port {port}")

            sock.close()

    except KeyboardInterrupt:
        print("\nScan stopped by user.")

# ---------------- MAIN LOOP ----------------
def run_network_scanner():
    while True:
        network_menu()
        choice = input("\nSelect option > ")

        if choice == "0":
            break
        elif choice == "1":
            ping_scan()
        elif choice == "2":
            port_scan()
        elif choice == "3":
            service_version_scan()
        elif choice == "4":
            os_detection()
        elif choice == "5":
            python_port_scanner()
        else:
            print("Invalid option!")

        input("\nPress Enter to continue...")