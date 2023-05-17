import os


def get_option(prompt: str, options: list[str]) -> str:
    result = None
    valid_input = False
    while not valid_input:
        result = input(prompt)
        if result in options:
            valid_input = True
    return result


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
