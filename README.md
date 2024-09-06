# Auth The Grid (A CLI Password Manager)

Auth The Grid is a command-line interface (CLI) password manager that allows you to securely store and manage your passwords.

## Features

- **Secure Storage**: Passwords are encrypted using the Fernet symmetric encryption.
- **Root Password Protection**: Access to the password manager is protected by a root password.
- **Service Management**: Add, retrieve, and list passwords for different services.
- **Data Persistence**: Save and load passwords from a JSON file.
- **GitHub Integration**: Easily star the GitHub repository from the CLI.

## Files

- `password_manager.py` - Main file with the CLI interface.

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
python password_manager.py
```

## Commands
1. Add password: Add a new password for a service.
2. Get password: Retrieve the password for a service.
3. List services: List all services with stored passwords.
4. Save passwords: Save the current passwords to a file.
5. Star the GitHub repo: Open the GitHub repository in your browser.
6. Exit: Exit the password manager.

## Example
```sh
python password_manager.py
```
You will be prompted to set a root password if running for the first time, or to enter your root password if you have already set one.

## License
- This project is licensed under the MIT License.

## Author
- Created by [kiing-dom](github.com/kiing-dom)