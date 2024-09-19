import os
import getpass
import webbrowser
import sys
from password_manager import PasswordManager
from file_operations import save_data_to_file, load_from_file
from ui import display_title, display_menu, get_user_choice, display_message, custom_loading_animation
from termcolor import colored

GITHUB_REPO_URL = 'https://github.com/kiing-dom/cli-password-manager'

def main():
    custom_loading_animation()
    display_title()

    pm = PasswordManager()
    
    if os.path.exists('passwords.json'):
        load_from_file(pm, 'passwords.json')
        while True:
            root_password = getpass.getpass(colored("Enter your root password: ", 'yellow'))
            if pm.verify_root_password(root_password):
                pm.set_root_password(root_password)
                display_message("Access granted!", 'green')
                break
            else:
                display_message("Root password Incorrect. Try again.", 'red')
    else:
        while True:
            root_password = getpass.getpass(colored("Set a new root password: ", 'yellow'))
            confirm_password = getpass.getpass(colored("Confirm root password: ", 'yellow'))
            if root_password == confirm_password:
                pm.set_root_password(root_password)
                save_data_to_file(pm, 'passwords.json')
                display_message("Root password set and saved successfully!", 'green')
                break
            else:
                display_message("Passwords do not match. Try again.", 'red')
                
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == '1':
            service = input(colored("Enter the service name: ", 'yellow'))
            password = getpass.getpass(colored("Enter the password: ", 'yellow'))
            pm.add_password(service, password)
            display_message("Password added successfully!", 'green')
        
        elif choice == '2':
            service = input(colored("Enter the service name: ", 'yellow'))
            password = pm.get_password(service)
            if password:
                display_message(f"Password for {service}: {password}", 'green')
            else:
                display_message("Service not found.", 'red')
        
        elif choice == '3':
            services = pm.list_services()
            display_message("Services:", 'cyan')
            for service in services:
                display_message(f"- {service}", 'yellow')
        
        elif choice == '4':
            save_data_to_file(pm, 'passwords.json')
            display_message("Passwords saved successfully!", 'green')
            
        elif choice == '5':
            service = input(colored("Enter name of service with password to be edited: ", 'yellow'))
            if service in pm.list_services():
                new_password = getpass.getpass(colored("Enter the new password: ", 'yellow'))
                if pm.edit_password(service, new_password):
                    display_message(f"Password for {service} updated successfully!", 'green')
                else:
                    display_message(f"Password could not be updated!", 'red')
            else:
                display_message(f"Service could not be found", 'red')
                
        elif choice == '6':
            service = input(colored("Enter name of service to be deleted: ", 'yellow'))
            if service in pm.list_services():
                confirm = input(colored(f"Are you sure you want to delete the password for {service}? (y/n): ", 'yellow')).lower()
                if confirm == 'y':
                    if(pm.delete_password(service)):
                        display_message(f"Password for {service} deleted successfully!", 'green')
                        save_data_to_file(pm, 'passwords.json')
                    else:
                        display_message(f"Password for {service} could not be deleted", 'red')
                else: display_message("Deletion cancelled.", 'yellow')
            else: display_message(f"Service {service} does not exist.", 'red')

        elif choice == '7':
            length = int(input(colored("Enter a password length: ", 'yellow')))
            if length < 12:
                display_message("Invalid length. Password length should be at least 12")
            else:
                password = pm.generate_strong_password(length)
                display_message(f"Password: {password}")
            
        elif choice == '8':
            display_message("Opening GitHub repo in browser...", 'cyan')
            webbrowser.open(GITHUB_REPO_URL)
        
        elif choice == '9':
            display_message("Thank you for staying Auth the Grid. Goodbye!", 'red')
            sys.exit(0)
        
        else:
            display_message("Invalid choice. Please try again.", 'red')

if __name__ == "__main__":
    main()