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
    result = None
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
