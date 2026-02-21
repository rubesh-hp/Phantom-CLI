import sys
import subprocess
import importlib.util
import shutil
import time
import hashlib
import datetime
import os
import webbrowser

# ===============================
# DEPENDENCY CHECK (requests)
# ===============================

def ensure_requests():
    if importlib.util.find_spec("requests") is None:
        print("❌ 'requests' library not found.")
        print("👉 Required for Web Attacks module.")
        choice = input("Install now? (Y/N) > ").lower()
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

GLOBAL_PROXY = None
GLOBAL_HEADERS = {}
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ===============================
# LEGAL GATE
# ===============================

def legal_gate():
    print("""
⚠️  LEGAL WARNING – REAL WEB TRAFFIC ⚠️

This module sends REAL HTTP requests.
Use ONLY on systems you OWN or have EXPLICIT permission for.

Type EXACTLY:
I TAKE FULL RESPONSIBILITY
""")
    return input("> ").strip() == "I TAKE FULL RESPONSIBILITY"

# ===============================
# MENU
# ===============================

def web_attack_menu():
    print("\n--- WEB ATTACKS ---")
    print("[1] Intruder (Clusterbomb)")
    print("[2] Repeater")
    print("[3] SQLMap")
    print("[4] Proxy Settings")
    print("[5] Header Manager")
    print("[0] Back")

# ===============================
# UTILITIES
# ===============================

def log_event(data):
    filename = f"{LOG_DIR}/attack_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(data + "\n")

def response_fingerprint(response):
    body_hash = hashlib.sha256(response.content).hexdigest()
    return response.status_code, len(response.content), body_hash

# ===============================
# DEPENDENCY CHECK (SQLMAP)
# ===============================

def check_sqlmap():
    sqlmap = shutil.which("sqlmap")
    if sqlmap:
        return sqlmap

    print("""
❌ sqlmap not found
👉 Recommended:
   pip install sqlmap
   OR
   sudo apt install sqlmap

Do you want me to open the install guide? (Y/N)
""")
    if input("> ").lower() == "y":
        webbrowser.open("https://github.com/sqlmapproject/sqlmap")
    return None

# ===============================
# HEADER MANAGER
# ===============================

def header_manager():
    global GLOBAL_HEADERS

    print("\n--- HEADER MANAGER ---")
    if not GLOBAL_HEADERS:
        print("(No headers set)")
    else:
        for k, v in GLOBAL_HEADERS.items():
            print(f"{k}: {v}")

    print("\n[1] Add / Update header")
    print("[2] Remove header")
    print("[3] Clear all headers")
    print("[0] Back")

    choice = input("> ")

    if choice == "1":
        GLOBAL_HEADERS[input("Header name > ")] = input("Header value > ")
    elif choice == "2":
        GLOBAL_HEADERS.pop(input("Header name > "), None)
    elif choice == "3":
        GLOBAL_HEADERS.clear()

# ===============================
# INTRUDER – CLUSTERBOMB
# ===============================
def intruder_clusterbomb():
    url = input("Target URL (use {A} and {B}) > ").strip()
    p1 = input("Payload list 1 (comma separated) > ").split(",")
    p2 = input("Payload list 2 (comma separated) > ").split(",")

    # -------- SAFE DELAY INPUT --------
    while True:
        delay_input = input("Delay between requests (seconds, default=0) > ").strip()
        if delay_input == "":
            delay = 0.0
            break
        try:
            delay = float(delay_input)
            if delay < 0:
                print("❌ Delay cannot be negative.")
                continue
            break
        except ValueError:
            print("❌ Invalid number. Example: 0, 0.5, 1")

    baseline = None
    print("\n🚀 Clusterbomb started\n")

    for a in p1:
        for b in p2:
            attack_url = url.replace("{A}", a.strip()).replace("{B}", b.strip())
            try:
                r = requests.get(
                    attack_url,
                    headers=GLOBAL_HEADERS,
                    proxies=GLOBAL_PROXY,
                    timeout=10
                )

                status, length, body_hash = response_fingerprint(r)

                if baseline is None:
                    baseline = (status, length)

                diff = "DIFF" if (status, length) != baseline else "SAME"

                output = f"[{status}] LEN={length} HASH={body_hash[:8]} [{diff}]"
                print(output, attack_url)
                log_event(output + " " + attack_url)

                time.sleep(delay)

            except Exception as e:
                print(f"[ERROR] {attack_url} -> {e}")

# ===============================
# REPEATER
# ===============================

def repeater():
    method = input("Method (GET/POST) > ").upper()
    url = input("URL > ")
    data = input("Body (empty if none) > ")

    r = requests.post(url, data=data, headers=GLOBAL_HEADERS, proxies=GLOBAL_PROXY) \
        if method == "POST" else \
        requests.get(url, headers=GLOBAL_HEADERS, proxies=GLOBAL_PROXY)

    status, length, body_hash = response_fingerprint(r)
    print(f"\nStatus: {status}\nLength: {length}\nHash: {body_hash}\n")
    print(r.text[:1000])

# ===============================
# SQLMAP
# ===============================

def sqlmap_runner():
    sqlmap = check_sqlmap()
    if not sqlmap:
        return

    target = input("Target URL > ")
    if input("Type RUN to continue > ") == "RUN":
        subprocess.run([sqlmap, "-u", target, "--batch"])

# ===============================
# PROXY SETTINGS
# ===============================

def proxy_settings():
    global GLOBAL_PROXY
    proxy = input("Proxy URL or empty to disable > ").strip()
    GLOBAL_PROXY = {"http": proxy, "https": proxy} if proxy else None

# ===============================
# MAIN LOOP
# ===============================

def run_web_attacks():
    if not legal_gate():
        print("Access denied.")
        return

    while True:
        web_attack_menu()
        choice = input("> ")

        if choice == "0":
            break
        elif choice == "1":
            intruder_clusterbomb()
        elif choice == "2":
            repeater()
        elif choice == "3":
            sqlmap_runner()
        elif choice == "4":
            proxy_settings()
        elif choice == "5":
            header_manager()

        input("\nPress Enter to continue...")