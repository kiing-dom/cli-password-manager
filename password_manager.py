import sys
import getpass
from cryptography.fernet import Fernet
import json

class PasswordManager:
    def _init_(self, master_password):
        self.key = self.generate_key(master_password)
        self.fernet = Fernet(self.key)
        self.passwords = {}