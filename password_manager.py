import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
    
    # edit password
    def edit_password(self, service, new_password):
        if service in self.passwords:
            encrypted_password = self.fernet.encrypt(new_password.encode())
            self.passwords[service] = encrypted_password.decode();
            return True
        return False
    
    # delete function
    def delete_password(self, service):
        if service in self.passwords:
            del self.passwords[service]
            return True
        return False
    
    def list_services(self):
        return list(self.passwords.keys())