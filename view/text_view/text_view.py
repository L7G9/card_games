"""Functions to enable the use of the console as a text based view in MVC.

Use these to supplement print, read and sleep.

Functions:

    get_option(prompt, options) -> string

    clear_screen()

Typical usage examples:

    number = get_option("Pick a number fro 1 to 4", ["1", "2", "3", "4"])

    clear_screen()
"""

import os


def get_option(prompt: str, options: list[str]) -> str:
    """Get user to select an option.

    Prompts user to enter an option into console until a valid one is entered.

    Args:
        prompt: A string describing to user what their options are.
        options: A list of string containing the valid options.

    Returns:
        A string containing the option chosen.
    """
    result = ""
    valid_input = False
    while not valid_input:
        result = input(prompt)
        if result in options:
            valid_input = True
    return result


def clear_screen():
    """Clear screen depending on operating system."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
