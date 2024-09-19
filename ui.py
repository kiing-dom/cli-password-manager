
import time
import sys
import os
from termcolor import colored
import pyfiglet

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title():
    ascii_banner = pyfiglet.figlet_format("Auth the Grid")
    print(colored(ascii_banner, 'cyan'))
    print(colored("Created by kiing-dom", 'yellow'))

def display_menu():
    print(colored("\n1. Add password", 'cyan'))
    print(colored("2. Get password", 'cyan'))
    print(colored("3. List services", 'cyan'))
    print(colored("4. Edit a Password", 'cyan'))
    print(colored("5. Delete a Password", 'cyan'))
    print(colored("6. Generate Strong Password", 'blue'))
    print(colored("7. Star the GitHub repo", 'light_magenta'))
    print(colored("8. Exit", 'cyan'))

def get_user_choice():
    return input(colored("Enter your choice (1-8): ", 'yellow'))

def display_message(message, color='white'):
    print(colored(message, color))

def custom_loading_animation(duration=3):
    animation = "|/-\\"
    start_time = time.time()
    
    terminal_width = os.get_terminal_size().columns
    
    text = "Initializing Auth the Grid"
    padding = (terminal_width - len(text) - 2) // 2
    centered_text = " " * padding + text + " " * padding
    
    
    border = "+" + "-" * (len(centered_text) - 2) + "+"
    
    clear_screen()
    while time.time() - start_time < duration:
        for char in animation:
            # Print centered loading animation
            print("\n" * ((os.get_terminal_size().lines - 5) // 2)) 
            print(colored(border, 'cyan'))
            print(colored(f"|{centered_text}|", 'cyan'))
            print(colored(f"|{' ' * padding}{char}{' ' * padding}|", 'yellow'))
            print(colored(border, 'cyan'))
            
            sys.stdout.flush()
            time.sleep(0.1)
            clear_screen()
    
    print("\n" * ((os.get_terminal_size().lines - 3) // 2))  
    print(colored(border, 'green'))
    print(colored(f"|{centered_text}|", 'green'))
    print(colored(border, 'green'))
    time.sleep(0.5)
    clear_screen()