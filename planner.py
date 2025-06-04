import json
from datetime import datetime

entries = []
DATA_FILE = "data.json"

def load_entries():
    global entries
    try:
        with open(DATA_FILE, "r") as f:
            entries = json.load(f)
    except FileNotFoundError:
        entries = []

def save_entries():
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f)

def add_entry(entry_type, description, amount):
    entry = {
        "type": entry_type,
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    entries.append(entry)
    save_entries()

def list_entries():
    return entries
