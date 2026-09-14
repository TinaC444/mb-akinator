"""The terminal game's entropy and filtering logic, without terminal I/O."""

import json
from math import log2
from pathlib import Path


# Resolve the data relative to this file, regardless of the working directory.
DATA_PATH = Path(__file__).resolve().parent.parent / "character_base.json"
with DATA_PATH.open(encoding="utf-8") as character_file:
    data = json.load(character_file)

FEATURE_NAMES = tuple(data["features"])
CHARACTER_NAMES = tuple(data["characters"])
QUESTIONS = tuple(data["features"][feature] for feature in FEATURE_NAMES)
X = tuple(
    tuple(data["characters"][name][feature] for feature in FEATURE_NAMES)
    for name in CHARACTER_NAMES
)


def new_game():
    """Create independent masks sized from the character database."""
    return {
        "possible_char": [1] * len(CHARACTER_NAMES),
        "unasked_q": [1] * len(FEATURE_NAMES),
    }


def find_best_question(possible_char, unasked_q):
    """Choose the unasked question closest to a 50/50 split of survivors."""
    remaining = [index for index, possible in enumerate(possible_char) if possible]
    if not remaining:
        return None

    best_q = None
    best_entropy = -1.0
    for question_index, unasked in enumerate(unasked_q):
        if not unasked:
            continue

        yes_probability = sum(X[index][question_index] for index in remaining) / len(remaining)
        entropy = 0.0
        for probability in (yes_probability, 1.0 - yes_probability):
            if probability > 0:
                entropy -= probability * log2(probability)

        # Keep the first question in JSON order when scores tie.
        if entropy > best_entropy:
            best_entropy = entropy
            best_q = question_index

    return best_q


def remove_invalid_char(user_ans, best_q, possible_char):
    """Return a new mask; an eliminated character can never come back."""
    return [
        int(bool(possible) and X[index][best_q] == user_ans)
        for index, possible in enumerate(possible_char)
    ]


def output_char(possible_char):
    """Return the final message for display on the webpage."""
    remaining = [name for name, possible in zip(CHARACTER_NAMES, possible_char) if possible]
    if len(remaining) == 1:
        return f"Your character is {remaining[0]}."
    if not remaining:
        return "Invalid sequence: no character matches those answers."
    return "No questions left. I couldn't narrow it down to one character."


def game_view(game):
    """Expose only the current question/result and count to the page."""
    remaining = sum(game["possible_char"])
    best_q = None
    if remaining > 1:
        best_q = find_best_question(game["possible_char"], game["unasked_q"])

    done = best_q is None
    return {
        "question_index": best_q,
        "message": output_char(game["possible_char"]) if done else QUESTIONS[best_q],
        "remaining": remaining,
        "done": done,
    }
