# Auth The Grid (A CLI Password Manager)

Auth The Grid is a command-line interface (CLI) password manager that allows you to securely store and manage your passwords.

## Features

- **Secure Storage**: Passwords are encrypted using the Fernet symmetric encryption.
- **Root Password Protection**: Access to the password manager is protected by a root password.
- **Service Management**: Add, Edit, Delete, Retrieve, and List passwords for different services.
- **Password Generator**: Can Generate Strong Passwords for the user (minimum 12 characters)
- **Data Persistence**: Save and load passwords from a JSON file.

## Files

- `main.py` - The project entry point that ties everything together.
- `password_manager.py` - Contains the core password management logic.
- `file_operations.py` - Handles saving and loading passwords.
- `ui.py` - Manages the user interface and cli interactions
  

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/kiing-dom/cli-password-manager.git
    cd cli-password-manager
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the password manager:
```sh
python main.py
```

## Commands
1. Add password: Add a new password for a service.
2. Get password: Retrieve the password for a service.
3. List services: List all services with stored passwords.
4. Save passwords: Save the current passwords to a file.
5. Edit password
6. Delete Password
7. Star the GitHub repo: Open the GitHub repository in your browser.
8. Exit: Exit the password manager.

## Example
```sh
python password_manager.py
```
You will be prompted to set a root password if running for the first time, or to enter your root password if you have already set one.

## License
- This project is licensed under the MIT License.

## Author
- Created by [kiing-dom](github.com/kiing-dom)