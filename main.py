import os
import sys
import getpass
from password_manager import PasswordManager
from utils import print_ascii_banner, print_menu, print_colored

def main():
    print_ascii_banner()

    pm = PasswordManager()
    
    if os.path.exists('passwords.json'):
        pm.load_from_file('passwords.json')
        while True:
            root_password = getpass.getpass(print_colored("Enter your root password: ", 'yellow'))
            if(pm.verify_root_password(root_password)):
                pm.set_root_password(root_password)
                print_colored("Access granted!", 'green')
                break
            else:
                print_colored("Root password Incorrect. Try again.", 'red')
                
    else:
        while True:
            root_password = getpass.getpass(print_colored("Set a new root password: ", 'yellow'))
            confirm_password = getpass.getpass(print_colored("Confirm root password: ", 'yellow'))
            if root_password == confirm_password:
                pm.set_root_password(root_password)
                pm.save_data_to_file('passwords.json')
                print_colored("Root password set and saved successfully!", 'green')
                break
            else:
                print_colored("Passwords do not match. Try again.", 'red')
                
    while True:
        print_menu()
        choice = input(print_colored("Enter your choice (1-5): ", 'yellow'))
        
        if choice == '1':
            service = input(print_colored("Enter the service name: ", 'yellow'))
            password = getpass.getpass(print_colored("Enter the password: ", 'yellow'))
            pm.add_password(service, password)
            print_colored("Password added successfully!", 'green')
        
        elif choice == '2':
            service = input(print_colored("Enter the service name: ", 'yellow'))
            password = pm.get_password(service)
            if password:
                print_colored(f"Password for {service}: {password}", 'green')
            else:
                print_colored("Service not found.", 'red')
        
        elif choice == '3':
            services = pm.list_services()
            print_colored("Services:", 'cyan')
            for service in services:
                print_colored(f"- {service}", 'yellow')
        
        elif choice == '4':
            pm.save_data_to_file('passwords.json')
            print_colored("Passwords saved successfully!", 'green')
        
        elif choice == '5':
            print_colored("Thank you for using the Password Manager. Goodbye!", 'magenta')
            sys.exit(0)
        
        else:
            print_colored("Invalid choice. Please try again.", 'red')

if __name__ == "__main__":
    main()
