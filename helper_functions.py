import json
import numpy as np

with open("character_base.json", "r") as f:
    data = json.load(f)
    

def load_character_base():
    # Feature names, in consistent order
    feature_names = list(data["features"].keys())

    # Character names
    character_names = list(data["characters"].keys())

    # Build N x d matrix
    X = np.array([
        [data["characters"][char][feature] for feature in feature_names]
        for char in character_names
    ], dtype=int)
    
    return X