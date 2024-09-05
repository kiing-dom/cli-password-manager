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
    def _init_(self, master_password):
        self.salt = os.random(16)
        self.passwords = {}
        self.master_password_hash = None
        
    def set_master_password(self, master_password):
        self.master_password_hash = hashlib.sha256(master_password.encode()).hexdigest()
        self.key = self.generate_key(master_password)
        self.fernet = Fernet(self.key)
        
    def generate_key(self, master_password):
        return Fernet.generate_key()
    
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
    
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.passwords, f)
            
    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.passowrds = json.load(f)