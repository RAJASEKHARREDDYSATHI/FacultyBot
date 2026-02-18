import json

def load_data():
    with open("faculty_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
