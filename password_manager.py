import sys
import getpass
import json
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from termcolor import colored
import pyfiglet

class PasswordManager:
    def __init__(self):
        self.salt = os.urandom(16)
        self.passwords = {}
        self.root_password_hash = None
        
    def set_root_password(self, root_password):
        self.root_password_hash = hashlib.sha256(root_password.encode()).hexdigest()
        self.key = self.generate_key(root_password)
        self.fernet = Fernet(self.key)
        
    def verify_root_password(self, root_password):
        return hashlib.sha256(root_password.encode()).hexdigest() == self.root_password_hash
    
    def generate_key(self, root_password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(root_password.encode()))
        return key
        
    def add_password(self, service, password):
        encrypted_password = self.fernet.encrypt(password.encode())
        self.passwords[service] = encrypted_password.decode()
        
    def get_password(self, service):
        encrypted_password = self.passwords.get(service)
        if encrypted_password:
            return self.fernet.decrypt(encrypted_password.encode()).decode()
        return None
    
    def list_services(self):
        return list(self.passwords.keys())
    
    def save_data_to_file(self, filename):
        data = {
            'salt': base64.b64encode(self.salt).decode(),
            'root_password_hash': self.root_password_hash,
            'passwords': self.passwords
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
            
    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.salt = base64.b64decode(data['salt'])
        self.root_password_hash = data['root_password_hash']
        self.passwords = data['passwords']
        
def main():
    # Adding a cool ASCII title
    ascii_banner = pyfiglet.figlet_format("Password Manager")
    print(colored(ascii_banner, 'cyan'))

    pm = PasswordManager()
    
    if os.path.exists('passwords.json'):
        pm.load_from_file('passwords.json')
        while True:
            root_password = getpass.getpass(colored("Enter your root password: ", 'yellow'))
            if(pm.verify_root_password(root_password)):
                pm.set_root_password(root_password)
                print(colored("Access granted!", 'green'))
                break
            else:
                print(colored("Root password Incorrect. Try again.", 'red'))
                
    else:
        while True:
            root_password = getpass.getpass(colored("Set a new root password: ", 'yellow'))
            confirm_password = getpass.getpass(colored("Confirm root password: ", 'yellow'))
            if root_password == confirm_password:
                pm.set_root_password(root_password)
                pm.save_data_to_file('passwords.json')
                print(colored("Root password set and saved successfully!", 'green'))
                break
            else:
                print(colored("Passwords do not match. Try again.", 'red'))
                
    while True:
        print(colored("\n1. Add password", 'cyan'))
        print(colored("2. Get password", 'cyan'))
        print(colored("3. List services", 'cyan'))
        print(colored("4. Save passwords", 'cyan'))
        print(colored("5. Exit", 'cyan'))
        
        choice = input(colored("Enter your choice (1-5): ", 'yellow'))
        
        if choice == '1':
            service = input(colored("Enter the service name: ", 'yellow'))
            password = getpass.getpass(colored("Enter the password: ", 'yellow'))
            pm.add_password(service, password)
            print(colored("Password added successfully!", 'green'))
        
        elif choice == '2':
            service = input(colored("Enter the service name: ", 'yellow'))
            password = pm.get_password(service)
            if password:
                print(colored(f"Password for {service}: {password}", 'green'))
            else:
                print(colored("Service not found.", 'red'))
        
        elif choice == '3':
            services = pm.list_services()
            print(colored("Services:", 'cyan'))
            for service in services:
                print(colored(f"- {service}", 'yellow'))
        
        elif choice == '4':
            pm.save_data_to_file('passwords.json')
            print(colored("Passwords saved successfully!", 'green'))
        
        elif choice == '5':
            print(colored("Thank you for using the Password Manager. Goodbye!", 'magenta'))
            sys.exit(0)
        
        else:
            print(colored("Invalid choice. Please try again.", 'red'))

if __name__ == "__main__":
    main()
