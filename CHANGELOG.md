## 1.1.0 (2023-06-14)

### Feat

- **ConsoleController**: changed range to opponent players to 0-7

### Fix

- **ConsoleController**: replaced assert with TypeError to ensure player.action_selector has been set

### Refactor

- **ConsoleController**: rename names attribute

## 1.0.1 (2023-06-08)

### Fix

- **console_controller**: add assert to ensure action_selector is not None

## 1.0.0 (2023-06-07)

### BREAKING CHANGE

- just a test

### Feat

- **test.py**: add goodbye_message method
- **test.py**: add hello_message function
- **test.py**: add file to test use of commitizen
- add workflow to bump version number

### Fix

- **test.py**: remove ! from message methods
- add version bump job to main CI workflow
- **run_21bust.py**: update docstring
