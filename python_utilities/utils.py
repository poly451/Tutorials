import json

def save_data(cls, filepath: str, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def open_data(cls, filepath):
    with open(filepath, "r") as f:
        mylines = json.load(f)
    return mylines