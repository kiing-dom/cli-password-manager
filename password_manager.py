import sys
import getpass
import json
import os
import base64
import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordManager:
    def _init_(self):
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
    print("Welcome to the password Manager!!")
    
    pm = PasswordManager()
    
    if os.path.exists('passwords.json'):
        pm.load_from_file('passwords.json')
        while True:
            root_password = getpass.getpass("Enter your root password: ")
            if(pm.verify_root_password(root_password)):
                pm.set_root_password(root_password)
                break
            else:
                print("Root password Incorrect. Try again.")
                
    else:
        while True:
            root_password = getpass.getpass("Set a new root password: ")
            confirm_password = getpass.getpass("Confirm root password: ")
            if root_password == confirm_password:
                pm.set_root_password(root_password)
                break
            else:
                print("Passwords do not match. Try again")
                
    while True:
        print("\n1. Add password")
        print("2. Get password")
        print("3. List services")
        print("4. Save passwords")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            service = input("Enter the service name: ")
            password = getpass.getpass("Enter the password: ")
            pm.add_password(service, password)
            print("Password added successfully!")
        
        elif choice == '2':
            service = input("Enter the service name: ")
            password = pm.get_password(service)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("Service not found.")
        
        elif choice == '3':
            services = pm.list_services()
            print("Services:")
            for service in services:
                print(f"- {service}")
        
        elif choice == '4':
            pm.save_data_to_file('passwords.json')
            print("Passwords saved successfully!")
        
        elif choice == '5':
            print("Thank you for using the Password Manager. Goodbye!")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()