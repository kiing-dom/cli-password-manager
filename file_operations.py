import json
import base64

def save_data_to_file(pm, filename):
    data = {
        'salt': base64.b64encode(pm.salt).decode(),
        'root_password_hash': pm.root_password_hash,
        'passwords': pm.passwords
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_from_file(pm, filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    pm.salt = base64.b64decode(data['salt'])
    pm.root_password_hash = data['root_password_hash']
    pm.passwords = data['passwords']