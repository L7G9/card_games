# Deck of cards
Simple project to test out development tools in Python

## Mark Down
[Cheat Sheet](https://towardsdatascience.com/the-ultimate-markdown-cheat-sheet-3d3976b31a0#fd13)

## Virtual environment
```
python -m venv venv
source venv/bin/activate
deactivate
```

## Project Structure
[RealPython.com](https://realpython.com/python-application-layouts/)

## Documentation
[RealPython.com](https://realpython.com/documenting-python-code/)

### Type Hinting
[RealPython.com](https://realpython.com/lessons/type-hinting/)
'''
def happy_birthday(name: str, age: int) -> str:
    return ("%s is %d years old today.  HAPPY BIRTHDAY!" % (name, age))
'''

### Doctstrings
Add doctrings to...



[Google docstrings standard](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
'''
def happy_birthday(name: str, age: int) -> str:
    """Creates birthday greeting.

    Uses the name and age aguments to create a birthday greeting as a string.

    Args:
        name: The name of the person who's birthday it is.
        age : The age of the person in years.

    Returns:
        A string containing the birthday greeting.  For example:

        'Bob is 12 years old today.  HAPPY BIRTHDAY!'
    """

    return ("%s is %d years old today.  HAPPY BIRTHDAY!" % (name, age))
'''

### Sphinx


## Python Tools
[Code Quality](https://itnext.io/essential-tools-for-improving-code-quality-in-python-d24ca3b963d4?gi=97defc488bb3)

### Flake8


#### Pycodestyle
Compliance with PEP 8 style guidelines

#### PyFlakes
Systax Checker

#### McCabe
Complexity analysis

### isort

### Black

### Pyright

### Bandit


