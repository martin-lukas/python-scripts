from colorama import Fore, Style


def print_choices(choices):
    for i, choice in enumerate(choices, start=1):
        print(Fore.BLUE + f"{i})\t{choice}" + Style.RESET_ALL)


def print_success(string):
    print(Fore.GREEN + string + Style.RESET_ALL)


def print_error(string):
    print(Fore.RED + string + Style.RESET_ALL)


def read_number(
    prompt, matches=lambda x: True, error_message="Invalid number. Try again."
):
    return read(
        prompt,
        lambda x: x.isdigit() and matches(int(x)),
        error_message
    )


def read(
    prompt, matches=lambda x: True, error_message="Invalid input. Try again."
):
    while True:
        value = input(Style.RESET_ALL + prompt)
        if matches(value):
            return value
        else:
            print_error(error_message)


def choose(choices, prompt, error_message):
    while True:
        print_choices(choices)
        choice = read(prompt)
        if choice.isdigit() and 0 < int(choice) <= len(choices):
            return int(choice) - 1
        else:
            print_error(error_message)


def choose_with_default(choices, prompt, error_message):
    while True:
        print_choices(choices)
        choice = read(prompt)
        if choice.isdigit() and 0 < int(choice) <= len(choices):
            return int(choice) - 1
        elif choice == "":
            return -1
        else:
            print_error(error_message)
