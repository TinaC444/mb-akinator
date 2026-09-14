import json
import numpy as np

with open("character_base.json", "r") as f:
    data = json.load(f)

feature_names = list(data["features"].keys())
character_names = list(data["characters"].keys())


def load_character_base():
    """Build the character-by-feature matrix in the JSON file's key order."""
    
    return np.array([
        [data["characters"][char][feature] for feature in feature_names]
        for char in character_names
    ], dtype=int)


def find_best_question(possible_char, unasked_q):
    """Return the unasked question with the highest binary split entropy."""
    
    X = load_character_base()
    possible_char = np.asarray(possible_char, dtype=bool)
    unasked_q = np.asarray(unasked_q, dtype=bool)

    #error checking
    if possible_char.size != X.shape[0]:
        raise ValueError("possible_char must have one entry per character")
    if unasked_q.size != X.shape[1]:
        raise ValueError("unasked_q must have one entry per feature")
    possible_count = np.count_nonzero(possible_char)
    if possible_count == 0:
        raise ValueError("There are no possible characters left")

    #use entropy to find the best question!!!
    best_q = None
    best_entropy = -1.0

    for question_index in np.flatnonzero(unasked_q):
        yes_count = np.count_nonzero(X[possible_char, question_index])
        yes_probability = yes_count / possible_count
        no_probability = 1.0 - yes_probability

        entropy = 0.0
        for probability in (yes_probability, no_probability):
            if probability > 0:
                entropy -= probability * np.log2(probability)

        if entropy > best_entropy:
            best_entropy = entropy
            best_q = int(question_index)

    if best_q is None:
        raise ValueError("There are no unasked questions left")

    return best_q


def user_response(best_q):
    """Ask a question in the terminal and return the answer as 0 or 1."""
    if not 0 <= best_q < len(feature_names):
        raise IndexError("best_q is not a valid question index")

    question = data["features"][feature_names[best_q]]

    while True:
        answer = input(f"{question} (yes/no or 1/0): ").strip().lower()
        if answer in {"1", "yes", "y"}:
            return 1
        if answer in {"0", "no", "n"}:
            return 0
        print("Please answer yes/no or 1/0.")


def remove_invalid_char(user_ans, best_q, possible_char=None):
    """Remove possible characters that disagree with the user's answer."""
    X = load_character_base()

    if user_ans not in (0, 1, False, True):
        raise ValueError("user_ans must be 0 or 1")
    if not 0 <= best_q < X.shape[1]:
        raise IndexError("best_q is not a valid question index")

    if possible_char is None:
        possible_char = np.ones(X.shape[0], dtype=int)
    else:
        possible_char = np.asarray(possible_char).copy()

    if possible_char.size != X.shape[0]:
        raise ValueError("possible_char must have one entry per character")

    possible_char[X[:, best_q] != int(user_ans)] = 0
    return possible_char


def output_char(possible_char):
    """Print the result when zero or one possible character remains."""
    possible_char = np.asarray(possible_char, dtype=bool)
    if possible_char.size != len(character_names):
        raise ValueError("possible_char must have one entry per character")

    remaining = np.flatnonzero(possible_char)

    if remaining.size == 1:
        character = character_names[remaining[0]]
        print(f"Your character is {character}.")
        return character

    if remaining.size == 0:
        print("Invalid sequence: no character matches those answers.")
        return None

    print(f"Unable to determine one character; {remaining.size} remain.")
    return None
