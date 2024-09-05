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
        self.salt = os.random(16)
        self.passwords = {}
        self.master_password_hash = None
        
    def set_master_password(self, master_password):
        self.master_password_hash = hashlib.sha256(master_password.encode()).hexdigest()
        self.key = self.generate_key(master_password)
        self.fernet = Fernet(self.key)
        
    def verify_master_password(self, master_password):
        return hashlib.sha256(master_password.encode()).hexdigest() == self.master_password_hash
    
    def generate_key(self, master_password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64decode(kdf.derive(master_password.encode()))
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
            'master_password_hash': self.master_password_hash,
            'passwords': self.passowrds
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
            
    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.salt = base64.b64decode(data['salt'])
        self.master_password_hash = data['master_password_hash']
        self.passwords = data['passwords']
        
def main():
    print("Welcome to the password Manager!!")
    
    pm = PasswordManager()
    
    if os.path.exists('passwords.json'):
        pm.load_from_file('passwords.json')
        while True:
            master_password = getpass.getpass("Enter your root password: ")
            if(pm.verify_master_password(master_password)):
                pm.set_master_password(master_password)
                break
            else:
                print("Root password Incorrect. Try again.")
                
    else:
        while True:
            master_password = getpass.getpass("Set a new root password: ")
            confirm_password = getpass.getpass("Confirm root password: ")
            if master_password == confirm_password:
                pm.set_master_password(master_password)
                break
            else:
                print("Passwords do not match. Try again")
                
    