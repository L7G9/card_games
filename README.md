---
# Card Games

Card games written in Python using the Model-View-Controller pattern.

---

Created as example of Python project structure, testing, documentation and use of code quality tools.

Currently there is a single text based game called 21 Bust, in which a single user can play against application controlled players using a simple algorithm.

---

## Requirements
[Python3](https://www.python.org/downloads/)\
[Infelct package](https://pypi.org/project/inflect/)

---

## Getting Started - Ubuntu
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
Run game.
```bash
python3 run_21Bust.py
```

---

## Documentation
[code reference guide](https://l7g9.github.io/card_games/)

---

## Development Environment - Ubuntu
Development setup, includes pakages for testing, code quality and documentation.
```bash
git clone https://github.com/L7G9/card_games.git
cd card_games
python3 -m venv venv
source venv/bin/activate
pip install -r dev_requirements.txt
```
This will install the following tools.

### Commitizen
With pre-commit enforces use of Conventional Commits.
Then after a fix, feature or breaking feature is committed it...
  - Updates the project version number
  - Updates the changelog
  - Creates a new git tag
```bash
git add .
cz commit
cz bump
git push origin main
git push origin <tag_name>
```

### Black
Code sytle formatter.
```bash
black --line-length 79 .
```

### iSort
Import statement sorter.
```bash
isort .
```

### Flake8
Combines serveral tools to enhance code quality...
- Pycodestyle for PEP 8 style compilance
- PyFlakes for Defect analysis.
- McCabe for Complixity analysis.
```bash
flake8 .
```

### Pyright
Type checking for Python.
```bash
pyright .
```

### Pytest
Python unit testing.
```bash
pytest tests/
```

### Pytest-cov
Unit testing coverage.
```bash
pytest --cov=. tests/ --cov-fail-under=70 --cov-report=xml:reports/coverage.xml
```

### Bandit
Security vulnerability analysis.
```Bash
bandit -r model/ view/ controller/
```

### Sphinx
Build documentation source files from docstrings.
```Bash
sphinx-apidoc -o docs/source .
```
Build a static website from documentation source files.
```Bash
sphinx-apidoc -o docs/source .
```
Workflow to upload documentation to GitHub Pages.
[workflow](https://github.com/L7G9/card_games/blob/main/.github/workflows/sphinx.yml)
[documentation](https://l7g9.github.io/card_games/)

### Continuous integration pipeline
Using these tools to ensure code passes various quality tests before being pushed to main branch of the github repository.
[workflow](https://github.com/L7G9/card_games/blob/main/.github/workflows/main.yaml)

---

## Author
[@L7G9](https://www.github.com/L7G9)

---

## Acknowledgements
All these resources were used to create this project.  Thank you to all those who took the time and effort to share.
- [Essential Tools for Improving Code Quality in Python](https://itnext.io/essential-tools-for-improving-code-quality-in-python-d24ca3b963d4?gi=778eda09d9b7)
- [markdown syntax](https://towardsdatascience.com/the-ultimate-markdown-cheat-sheet-3d3976b31a0)
- [dillinger markdown editor](https://dillinger.io/)
- [python project structure](https://realpython.com/python-application-layouts/)
- [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [angular commit format](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [commitizen](https://commitizen-tools.github.io/commitizen/)
- [Pre-commit](https://pre-commit.com/)
- [Docstrings](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
- [black](https://pypi.org/project/black/)
- [isort](https://pycqa.github.io/isort/)
- [flake8](https://pypi.org/project/flake8/)
- [type-hinting](https://docs.python.org/3/library/typing.html)
- [pyright](https://microsoft.github.io/pyright/#/)
- [pytest](https://docs.pytest.org/en/7.3.x/)
- [pytest-cov](https://pypi.org/project/pytest-cov/)
- [bandit](https://pypi.org/project/bandit/)
- [sphinx](https://www.sphinx-doc.org/en/master/)
- [sphinx.ext.napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- [sphinx read the docs theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/)
- [github pages actions](https://github.com/peaceiris/actions-gh-pages)

---

