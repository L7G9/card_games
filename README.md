# Card Games
> Card games written in Python using the Model-View-Controller pattern.

Created as example of Python project structure, testing, documentation and use of code quality tools.  

Currently there is a single text based game called 21 Bust, in which a single user can play against application controlled players using a simple algorithm.  

## Requirements
[Python3](https://www.python.org/downloads/)\
[Infelct package](https://pypi.org/project/inflect/)

## Getting Started
Ubuntu setup.  

Clone GitHub repository.  
```bash
git clone https://github.com/L7G9/card_games.git
cd card_games
```
Create a virtual environment (optional).  
```bash
python3 -m venv venv
source venv/bin/activate
```
Install packages.
```bash
pip install -r requirements.txt
```
Run game
```bash
python3 run_21Bust.py
```

## Project Structure
- controller
	- twenty_one_bust : Controller class for 21 Bust model and Text View
- model
	- card_game : Generic classes for any card game
	- twenty_one_bust : Classes specific to the game of 21 Bust
- tests
	- model : Pytest units tests
- view
	- text_view : Functions to supplement print, input and sleep while using the console as a text based view
- run_21Bust.py : Python script to run the 21 Bust game


## Development Environment
Ubuntu development setup, includes pakages for testing and code quality.  
```bash
git clone https://github.com/L7G9/card_games.git
cd card_games
python3 -m venv venv
source venv/bin/activate
pip install -r dev_requirements.txt
```

### Pytest
Python unit testing.  
```bash
pytest test/
```

### Flake8
Combines serveral tools to enhance code quality including...
- Pycodestyle : PEP 8 style compilance.
- PyFlakes : Defect analysis.
- McCabe : Complixity analysis.
```bash
flake8 .
```

### iSort
Import statement sorter.
```bash
isort .
```

### Black
Code sytle formatter.  
```bash
black --line-length 79 .
```

## Authors
- [@L7G9](https://www.github.com/L7G9)

## Acknowledgements
- [Online Markdown Editor](https://markdownlivepreview.com/)
- [Markdown Guide]()
- [Python Project Structure]()
- [Docstrings](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
- [Sphinx]()
- [Type Hinting](https://realpython.com/lessons/type-hinting/)
- [Unit Testing]()
- [Code Quality Tools](https://itnext.io/essential-tools-for-improving-code-quality-in-python-d24ca3b963d4?gi=778eda09d9b7)
