from termcolor import colored
import pyfiglet

def print_ascii_banner():
    ascii_banner = pyfiglet.figlet_format("Password Manager")
    print(colored(ascii_banner, 'cyan'))

def print_menu():
    print(colored("\n1. Add password", 'cyan'))
    print(colored("2. Get password", 'cyan'))
    print(colored("3. List services", 'cyan'))
    print(colored("4. Save passwords", 'cyan'))
    print(colored("5. Exit", 'cyan'))

def print_colored(text, color):
    print(colored(text, color))
