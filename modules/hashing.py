import hashlib
import os
import re
import hmac

# MENU 

def hashing_menu():
    print("\n--- HASHING MODULE ---")
    print("[1] Generate Hash")
    print("[2] Identify Hash Type")
    print("[3] File Hash Checker")
    print("[4] Hash Comparison")
    print("[5] Wordlist Hash Checker")
    print("[6] HMAC Generator")
    print("[0] Back")

# HASH GENERATOR 

def generate_hash(text, algo):
    data = text.encode()

    if algo == "md5":
        return hashlib.md5(data).hexdigest()
    elif algo == "sha1":
        return hashlib.sha1(data).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(data).hexdigest()
    elif algo == "sha512":
        return hashlib.sha512(data).hexdigest()

# HASH IDENTIFIER 

def identify_hash(hash_value):
    h = hash_value.strip().lower()

    if re.fullmatch(r"[a-f0-9]{32}", h):
        return "MD5"
    elif re.fullmatch(r"[a-f0-9]{40}", h):
        return "SHA1"
    elif re.fullmatch(r"[a-f0-9]{64}", h):
        return "SHA256"
    elif re.fullmatch(r"[a-f0-9]{128}", h):
        return "SHA512"
    else:
        return "Unknown / Unsupported hash"

# FILE HASH CHECKER

def file_hash_checker():
    path = input("Enter file path > ").strip()

    if not os.path.isfile(path):
        print("File not found!")
        return

    with open(path, "rb") as f:
        data = f.read()

    print("\nMD5   :", hashlib.md5(data).hexdigest())
    print("SHA256:", hashlib.sha256(data).hexdigest())
    print("SHA512:", hashlib.sha512(data).hexdigest())

# HASH COMPARISON 

def hash_comparison():
    path = input("Enter file path > ").strip()
    known_hash = input("Enter known hash > ").strip().lower()

    if not os.path.isfile(path):
        print("File not found!")
        return

    algo = identify_hash(known_hash)

    if algo == "Unknown / Unsupported hash":
        print("Unsupported hash type")
        return

    with open(path, "rb") as f:
        data = f.read()

    if algo == "MD5":
        calc = hashlib.md5(data).hexdigest()
    elif algo == "SHA1":
        calc = hashlib.sha1(data).hexdigest()
    elif algo == "SHA256":
        calc = hashlib.sha256(data).hexdigest()
    elif algo == "SHA512":
        calc = hashlib.sha512(data).hexdigest()

    print("\nCalculated Hash:", calc)

    if calc == known_hash:
        print("Integrity Check: MATCH ✅")
    else:
        print("Integrity Check: MISMATCH ❌")

#  WORDLIST HASH CHECKER 

def wordlist_checker():
    target = input("Enter hash to crack > ").strip().lower()
    wordlist = input("Enter wordlist path > ").strip()

    if not os.path.isfile(wordlist):
        print("Wordlist not found!")
        return

    algo = identify_hash(target)

    if algo == "Unknown / Unsupported hash":
        print("Unsupported hash type")
        return

    print("\nCracking using", algo, "...")

    with open(wordlist, "r", errors="ignore") as f:
        for word in f:
            word = word.strip()

            if algo == "MD5":
                hashed = hashlib.md5(word.encode()).hexdigest()
            elif algo == "SHA1":
                hashed = hashlib.sha1(word.encode()).hexdigest()
            elif algo == "SHA256":
                hashed = hashlib.sha256(word.encode()).hexdigest()
            elif algo == "SHA512":
                hashed = hashlib.sha512(word.encode()).hexdigest()

            if hashed == target:
                print("PASSWORD FOUND ✅:", word)
                return

    print("Password not found in wordlist ❌")

# HMAC GENERATOR

def hmac_generator():
    message = input("Enter message > ").encode()
    key = input("Enter secret key > ").encode()

    print("\nChoose algorithm:")
    print("[1] HMAC-SHA256")
    print("[2] HMAC-SHA1")

    choice = input("Select > ")

    if choice == "1":
        digest = hmac.new(key, message, hashlib.sha256).hexdigest()
        print("\nHMAC-SHA256:", digest)

    elif choice == "2":
        digest = hmac.new(key, message, hashlib.sha1).hexdigest()
        print("\nHMAC-SHA1:", digest)

    else:
        print("Invalid option")

# MAIN CONTROLLER 

def run_hashing():
    while True:
        hashing_menu()
        choice = input("\nSelect option > ")

        if choice == "0":
            break

        elif choice == "1":
            text = input("Enter text to hash > ")
            print("\nMD5   :", generate_hash(text, "md5"))
            print("SHA1  :", generate_hash(text, "sha1"))
            print("SHA256:", generate_hash(text, "sha256"))
            print("SHA512:", generate_hash(text, "sha512"))
            input("\nPress Enter to continue...")

        elif choice == "2":
            h = input("Enter hash value > ")
            print("\nDetected Hash Type:", identify_hash(h))
            input("\nPress Enter to continue...")

        elif choice == "3":
            file_hash_checker()
            input("\nPress Enter to continue...")

        elif choice == "4":
            hash_comparison()
            input("\nPress Enter to continue...")

        elif choice == "5":
            wordlist_checker()
            input("\nPress Enter to continue...")

        elif choice == "6":
            hmac_generator()
            input("\nPress Enter to continue...")

        else:
            print("Invalid option!")