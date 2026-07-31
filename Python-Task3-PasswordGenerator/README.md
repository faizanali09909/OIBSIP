# Task 3 – Random Password Generator (Advanced Tier)

## Objective
A GUI-based password generator that creates strong, cryptographically secure
passwords based on user-defined criteria (length, character types, ambiguous
character exclusion).

## Tech Stack
- Python 3
- `secrets` module (cryptographically secure random generation)
- `tkinter` (GUI)
- `pyperclip` (clipboard integration)

## Features
- Length control via slider + spinbox (8–64 characters)
- Checkboxes for uppercase, lowercase, numbers, and symbols (min. 2 required)
- Guaranteed inclusion of at least one character from each selected type
- Password strength indicator (Weak / Medium / Strong) with a visual bar
- Copy to Clipboard button, with auto-copy on generation
- Option to exclude ambiguous characters (0, O, l, 1, I)
- Session-only history of the last 5 generated passwords (not saved to disk)

## How to Run
```bash
pip install pyperclip
python password_generator.py
```

## Notes
Uses `secrets.choice()` and a manual Fisher-Yates shuffle (via
`secrets.randbelow()`) instead of the `random` module, since `random` is not
cryptographically secure and shouldn't be used for anything security-sensitive
like password generation.
