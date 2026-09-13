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

from helper_functions import load_character_base

X = load_character_base()
print(X)
print(X.shape)