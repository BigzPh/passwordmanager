import json
import os
import hashlib
import secrets

file_path = r"C:\Users\carlo\PycharmProjects\ProgrammingLanguage\password.json"

def hash_password(password):
    salt = secrets.token_hex(16)  # 32 random characters
    iterations = 100_000

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        iterations
    ).hex()

    return {
        "salt": salt,
        "hash": hashed,
        "iterations": iterations
    }


def verify_password(password, stored_data):
    salt = stored_data["salt"]
    stored_hash = stored_data["hash"]
    iterations = stored_data["iterations"]

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        iterations
    ).hex()

    return new_hash == stored_hash


if os.path.exists(file_path):
    with open(file_path, "r") as file:
        try:
            passwords = json.load(file)
        except json.JSONDecodeError:
            passwords = []
else:
    passwords = []

choice = input("1. Login\n2. Sign Up\nEnter your choice: ")


if choice == "1":
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    for item in passwords:
        if item["username"] == username:
            if verify_password(password, item["password"]):
                print("Login Successful!")
            else:
                print("Invalid password!")
            break
    else:
        print("Username not found!")


elif choice == "2":
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")

    for item in passwords:
        if item["username"] == username:
            print("Username already exists")
            break
    else:
        hashed_data = hash_password(password)
        passwords.append({
            "username": username,
            "password": hashed_data
        })

        with open(file_path, "w") as file:
            json.dump(passwords, file, indent=4)

        print("Signup successful!")

else:
    print("Invalid choice!")
