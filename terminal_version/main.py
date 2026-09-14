'''
Algorithm:
1. Look at possible characters
- If 1 character remain: output the 1 character
- If 0 character remain: output "invalid character"
2. Score every unasked feature
3. Choose best feature to ask
4. Return question to user
5. Recieve yes/no
6. Remove incompatible characters
7. Repeat
'''

'''Import from character_base.json, '''

from terminal_version.helper_functions import load_character_base, find_best_question, user_response, remove_invalid_char, output_char
import numpy as np

X = load_character_base()

CHARACTERS = X.shape[0]
FEATURES = X.shape[1]

possible_char = np.ones(CHARACTERS)
unasked_q = np.ones(FEATURES)

while (np.sum(possible_char) > 1):
    best_q = find_best_question(possible_char, unasked_q)
    unasked_q[best_q] = 0
    user_ans = user_response(best_q)

    possible_char = remove_invalid_char(user_ans, best_q, possible_char)

output_char(possible_char)
