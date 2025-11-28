import json
import os
from hashlib import pbkdf2_hmac
import base64

file_path = r"C:\Users\carlo\Desktop\password.json"

passwords = {}
if os.path.exists(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            passwords = {item["username"]: item for item in data}
    except (json.JSONDecodeError, KeyError):
        passwords = {}

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    key = pbkdf2_hmac(
        "sha512",
        password.encode("utf-8"),
        salt,
        200_000
    )
    return salt, key

def encrypt(username, password):
    salt, key = hash_password(password)
    return {
        "username": username,
        "salt": base64.b64encode(salt).decode("utf-8"),
        "hash": base64.b64encode(key).decode("utf-8")
    }


def verify_password(password, stored):
    try:
        salt = base64.b64decode(stored["salt"])
        original_hash = base64.b64decode(stored["hash"])
        _, new_hash = hash_password(password, salt)
        return new_hash == original_hash
    except (ValueError, KeyError):
        return False

def is_strong_password(password):
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(
        c.isdigit() for c in password)


choice = input("1. Login\n2. Sign Up\nEnter your choice: ").strip()

if choice == "1":
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")

    if username in passwords and verify_password(password, passwords[username]):
        print("Login Successful!")
    else:
        print("Invalid username or password")

elif choice == "2":
    username = input("Enter a new username: ").strip()
    password = input("Enter a new password: ")

    if not username or not password:
        print("Username and password cannot be empty.")
    elif username in passwords:
        print("Username already exists!")
    elif not is_strong_password(password):
        print("Password must be at least 8 characters with uppercase, lowercase, and a digit.")
    else:
        passwords[username] = encrypt(username, password)
        with open(file_path, "w") as file:
            json.dump(list(passwords.values()), file, indent=4)
        print("Signup successful!")

else:
    print("Invalid choice.")
