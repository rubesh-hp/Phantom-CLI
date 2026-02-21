from modules.hashing import run_hashing
from modules.tools import run_tools
from modules.passwords import run_password_analyzer
from modules.network_scanner import run_network_scanner
def main_menu():
    print("\n========================")
    print("     PHANTOM CLI")
    print("========================")
    print("[1] Hashing Module")
    print("[2] Tool Detector")
    print("[3] Password Analyzer")
    print("[4] Network Scanner")
    print("[5] Web Attacks")
    print("[6] Smart Inspector")
    print("[0] Exit")

def main():
    while True:
        main_menu()
        choice = input("\nSelect an option > ")

        if choice == "1":
            run_hashing()
            input("Press Enter to return...")
        elif choice == "2":
            run_tools()
            input("Press Enter to return...")
        elif choice == "3":
            run_password_analyzer()
            input("Press Enter to return...")
        elif choice == "4":
            run_network_scanner()
            input("Press Enter to return...")
        elif choice == "5":
            from modules.web_attacks import run_web_attacks
            run_web_attacks()
            input("Press Enter to return...")   
        elif choice == "6":
            from modules.smart_inspector import run_smart_inspector
            run_smart_inspector()
            input("Press Enter to return...")
        elif choice == "0":
            print("\nExiting... 👋")
            break
        else:
            print("\nInvalid option!")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main()