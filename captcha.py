import random
import string
import time
import sys
import threading
import os
import pyfiglet
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global timeout event
time_up_event = threading.Event()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def generate_random_character(difficulty):
    if difficulty == 'easy':
        characters = string.ascii_uppercase + string.digits
    elif difficulty == 'medium':
        characters = string.ascii_letters + string.digits
    else:
        characters = string.ascii_letters + string.digits + "@#$%&*?!"
    return random.choice(characters)

def generate_quantum_captcha(difficulty='medium'):
    captcha_length = {'easy': 6, 'medium': 8, 'hard': 10}[difficulty]
    captcha = "".join(generate_random_character(difficulty) for _ in range(captcha_length))

    # Optional: Skip quantum logic for now
    new_captcha = captcha

    # Use simpler fonts only
    fonts = ["small", "block"]
    selected_font = random.choice(fonts)

    try:
        ascii_captcha = pyfiglet.figlet_format(new_captcha, font=selected_font)
    except pyfiglet.FontNotFound:
        ascii_captcha = pyfiglet.figlet_format(new_captcha)

    clear_screen()
    print(Fore.CYAN + "\n--- Quantum CAPTCHA ---")
    print(Fore.YELLOW + "Generated CAPTCHA (Expires in 30 seconds!):\n")
    print(Fore.GREEN + ascii_captcha)
    print(Fore.LIGHTWHITE_EX + f"CAPTCHA (type this exactly): {new_captcha}")

    return new_captcha

def countdown_timer(timeout):
    for remaining in range(timeout, 0, -1):
        if time_up_event.is_set():
            return
        sys.stdout.write(Fore.BLUE + f"\r⏳ Time left: {remaining} seconds  ")
        sys.stdout.flush()
        time.sleep(1)
    time_up_event.set()
    sys.stdout.write("\r" + " " * 50 + "\r")

def input_with_timeout(prompt, timeout):
    # user_input = [None]
    return input(prompt).strip()

    # def get_input():
    #     try:
    #         user_input[0] = input(prompt).strip()
    #     except EOFError:
    #         pass
    #     time_up_event.set()

    # input_thread = threading.Thread(target=get_input)
    # input_thread.start()
    # input_thread.join(timeout)

    # if input_thread.is_alive():
    #     time_up_event.set()
    #     return None

    # return user_input[0]

def verify_user_response(expected_captcha, timeout=30, attempts_left=3):
    time_up_event.clear()

    print(Fore.MAGENTA + "⚡ Type the CAPTCHA exactly as shown. Case & special characters matter!")
    print(Fore.LIGHTWHITE_EX + f"You have {timeout} seconds to enter the CAPTCHA below:\n")

    timer_thread = threading.Thread(target=countdown_timer, args=(timeout,))
    timer_thread.start()

    user_input = input_with_timeout(Fore.LIGHTWHITE_EX + "✍ Enter CAPTCHA: ", timeout)
    time_up_event.set()
    timer_thread.join()

    if user_input is None:
        clear_screen()
        print(Fore.RED + f"\n❌ Time's up! You have {attempts_left - 1} attempt(s) left.\n")
        return False

    if user_input == expected_captcha:
        clear_screen()
        print(Fore.GREEN + "✅ CAPTCHA solved correctly! You are human. 🎉\n")
        return True

    print(Fore.RED + "❌ Incorrect CAPTCHA! Try again.\n")
    return False

def run_captcha_system(difficulty='medium'):
    attempts = 3
    while attempts > 0:
        expected_captcha = generate_quantum_captcha(difficulty)
        if verify_user_response(expected_captcha, timeout=30, attempts_left=attempts):
            return "CAPTCHA solved!"

        attempts -= 1
        if attempts == 0:
            clear_screen()
            print(Fore.RED + "\n🚨 Too many failed attempts! Access Locked. 🚨\n")
            return "Access locked due to failed CAPTCHA attempts."

        print(Fore.YELLOW + f"\n🔄 You have {attempts} attempt(s) left. New CAPTCHA incoming...\n")
        time.sleep(2)

# Entry point
if __name__ == "__main__":
    try:
        run_captcha_system('medium')
    except KeyboardInterrupt:
        clear_screen()
        print(Fore.RED + "\n\n✋ Interrupted by user. Exiting gracefully.\n")