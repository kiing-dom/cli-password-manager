import os
import getpass
import webbrowser
import sys
from password_manager import PasswordManager
from file_operations import save_data_to_file, load_from_file
from ui import display_title, display_menu, get_user_choice, display_message, custom_loading_animation
from termcolor import colored

GITHUB_REPO_URL = 'https://github.com/kiing-dom/cli-password-manager'
PASSWORDS_FILE_PATH = 'passwords.json'

def load_or_set_root_password(pm):
    """Loads or sets the root password based on whether the password file exists"""
    if os.path.exists(PASSWORDS_FILE_PATH):
        load_from_file(pm, PASSWORDS_FILE_PATH)
        return prompt_root_password(pm)
    else:
        return set_new_root_password(pm)
    
def prompt_root_password(pm):
    """Promp user to enter root password until it is correct"""
    while True:
        root_password = getpass.getpass(colored("Enter your root password: ", 'yellow'))
        if pm.verify_root_password(root_password):
            pm.set_root_password(root_password)
            display_message("Access granted!", 'green')
            return True
        else:
            display_message("Root password Incorrect. Try again.", 'red')

def set_new_root_password(pm):
    """Set a new root password and save it to file."""
    while True:
        root_password = getpass.getpass(colored("Set a new root password: ", 'yellow'))
        confirm_password = getpass.getpass(colored("Confirm root password: ", 'yellow'))
        if root_password == confirm_password:
            pm.set_root_password(root_password)
            save_data_to_file(pm, PASSWORDS_FILE_PATH)
            display_message("Root password set and saved successfully!", 'green')
            return True
        else:
            display_message("Passwords do not match, Try again.", 'red')

def handle_add_password(pm):
    """Handle the flow for adding a password."""
    service = input(colored("Enter the service name: ", 'yellow'))
    if service in pm.list_services():
        overwrite_choice = input(colored(f"A password for '{service}' exists already. Overwrite? (Y/n): ", 'red')).lower()
        if overwrite_choice != 'y':
            display_message("Operation cancelled.", 'yellow')
            return
    
    password = getpass.getpass(colored("Enter the password: ", 'yellow'))
    pm.add_password(service, password)
    save_data_to_file(pm, PASSWORDS_FILE_PATH)
    display_message("Password added successfully!", 'green')

def handle_get_password(pm):
    """Handle the flow foor retrieving a password"""
    service = input(colored("Enter the service name: ", 'yellow'))
    password = pm.get_password(service)
    if password:
        display_message(f"Password for {service}: {password}", 'green')
    else:
        display_message("Service not found.", 'red')

def handle_edit_password(pm):
    """Handle the flow for editing a password"""
    service = input(colored("Enter name of service with password to be edited: ", 'yellow'))
    if service in pm.list_services():
        new_password = getpass.getpass(colored("Enter the new password: ", 'yellow'))
        if pm.edit_password(service, new_password):
            display_message(f"Password for {service} updated successfully!", 'green')
        else:
            display_message("Password could not be updated!", 'red')
    else:
        display_message("Service could not be found", 'red')

def handle_delete_password(pm):
    """Handle the flow for deleting a password."""
    service = input(colored("Enter the name of the service to be deleted: ", 'yellow'))
    if service in pm.list_services():
        confirm = input(colored(f"Are you sure you want to delete the password for {service}? (Y/n): ", 'yellow')).lower()
        if confirm == 'y' and pm.delete_password(service):
            display_message(f"Password for {service} deleted successfully!", 'green')
            save_data_to_file(pm, PASSWORDS_FILE_PATH)
        else:
            display_message(f"Password for {service} could not be deleted", 'red')
    else:
        display_message(f"Service {service} does not exist.", 'red')

def handle_generate_password(pm):
    """Handle generating a strong password."""
    length = int(input(colored("Enter a password length: ", 'yellow')))
    if length < 12:
        display_message("Invalid length. Password length should be at least 12", 'red')
    else:
        password = pm.generate_strong_password(length)
        display_message(f"Password: {password}", 'green')

def main():
    custom_loading_animation()
    display_title()

    pm = PasswordManager()
    
    load_or_set_root_password(pm)
    
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            handle_add_password(pm)
        elif choice == '2':
            handle_get_password(pm)
        elif choice == '3':
            services = pm.list_services()
            display_message("Services:", 'cyan')
            for service in services:
                display_message(f"- {service}", 'yellow')
        elif choice == '4':
            handle_edit_password(pm)
        elif choice == '5':
            handle_delete_password(pm)
        elif choice == '6':
            handle_generate_password(pm)
        elif choice == '7':
            display_message("Opening GitHub repo in browser...", 'cyan')
            webbrowser.open(GITHUB_REPO_URL)
        elif choice == '8':
            display_message("Thank you for staying Auth the Grid. Goodbye!", 'red')
            sys.exit(0)
        else:
            display_message("Invalid choice. Please try again.", 'red')

if __name__ == "__main__":
    main()