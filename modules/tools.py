import shutil
import platform

def tools_menu():
    print("\n--- TOOL DETECTOR ---")
    print("[1] Scan common tools")
    print("[0] Back")

def check_tool(tool_name):
    return shutil.which(tool_name) is not None

def show_result(tool, exists):
    if exists:
        print(f"[✔] {tool} is installed")
    else:
        print(f"[✘] {tool} NOT found")

def suggest_install(tool):
    os_name = platform.system()

    if os_name == "Windows":
        print(f"    → Install {tool} manually or via Chocolatey")
    elif os_name == "Linux":
        print(f"    → sudo apt install {tool}")
    else:
        print("    → OS not supported")

def run_tools():
    tools = ["nmap", "whois", "netstat", "ipconfig"]

    while True:
        tools_menu()
        choice = input("\nSelect option > ")

        if choice == "0":
            break

        if choice == "1":
            print("\nScanning tools...\n")
            for tool in tools:
                exists = check_tool(tool)
                show_result(tool, exists)
                if not exists:
                    suggest_install(tool)

            input("\nPress Enter to continue...")
        else:
            print("Invalid option!")