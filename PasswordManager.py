import json
import os

file_path = r"C:\Users\carlo\Desktop\password.json"

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
        if item["username"] == username and item["password"] == password:
            print("Login Successful!")
            break
    else:
        print("Invalid username or password")

elif choice == "2":
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")


    for item in passwords:
        if item["username"] == username:
            print("Username already exists!")
            break
    else:
        passwords.append({"username": username, "password": password})
        with open(file_path, "w") as file:
            json.dump(passwords, file, indent=4)
        print("Signup successful!")

else:
    print("Invalid choice.")
