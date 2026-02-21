import re
import random
import string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return "".join(random.choice(chars) for _ in range(length))

def password_menu():
    print("\n--- PASSWORD ANALYZER ---")
    print("[1] Check password strength")
    print("[2] Generate password")
    print("[0] Back")

def analyze_password(password):
    score = 0
    feedback = []

    length = len(password)

    # Length check
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("Too short (use at least 8–12 characters)")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("No uppercase letters")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("No lowercase letters")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("No numbers")

    # Symbols
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("No symbols")

    # Common weak patterns
    if password.lower() in ["password", "123456", "admin", "qwerty"]:
        feedback.append("Very common password (easily cracked)")
        score = 0

    return score, feedback

def strength_label(score):
    if score <= 2:
        return "WEAK ❌"
    elif score <= 4:
        return "MEDIUM ⚠️"
    else:
        return "STRONG ✅"

def run_password_analyzer():
    while True:
        password_menu()
        choice = input("\nSelect option > ")

        if choice == "0":
            break

        if choice == "1":
            pwd = input("Enter password to analyze > ")
            score, feedback = analyze_password(pwd)

            print("\nPassword Strength:", strength_label(score))

            if feedback:
                print("Issues found:")
                for f in feedback:
                    print(" -", f)
            else:
                print("Good job! Password looks strong.")

            input("\nPress Enter to continue...")
        elif choice == "2":
             length = input("Enter password length (default 12) > ")
             length = int(length) if length.isdigit() else 12
             
             pwd = generate_password(length)
             score, _ = analyze_password(pwd)

             print("\nGenerated Password:", pwd)
             print("Strength:", strength_label(score))

             input("\nPress Enter to continue...")
        else:
            print("Invalid option!")