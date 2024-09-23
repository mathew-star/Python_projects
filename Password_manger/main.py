from termcolor import colored
import pyfiglet
from auth import User, Session
from password import PasswordManager
from storage import DataStore

def main():
    result = pyfiglet.figlet_format("PassWe", font="slant")
    print(colored(result, 'green'))
    data_store = DataStore('passwords.json')
    password_manager = PasswordManager(data_store)

    while True:
        print("\nPassword Manager")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = User(username, password)
            if data_store.get_password(user, 'login') == password:
                session = Session(user)
                logged_in_menu(session, password_manager)
            else:
                print("Invalid credentials")
        elif choice == '2':
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            user = User(username, password)
            data_store.save_password(user, 'login', password)
            print("User registered successfully")
        elif choice == '3':
            break
        else:
            print("Invalid choice")

def logged_in_menu(session, password_manager):
    while session.is_active:
        print("\nLogged In Menu")
        print("1. Add Password")
        print("2. Get Password")
        print("3. Generate Password")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            service = input("Enter service name: ")
            password = input("Enter password: ")
            success, message = password_manager.add_password(session.user, service, password)
            print(message)
        elif choice == '2':
            service = input("Enter service name: ")
            password = password_manager.get_password(session.user, service)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("Password not found")
        elif choice == '3':
            length = int(input("Enter password length: "))
            password = password_manager.generate_password(length)
            print(f"Generated password: {password}")
        elif choice == '4':
            session.end()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()