import json
import os
from datetime import datetime

DATA_FILE = "data.json"

class Entry:
    def __init__(self, entry_type, description, amount, date=None):
        self.type = entry_type
        self.description = description
        self.amount = amount
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "type": self.type,
            "description": self.description,
            "amount": self.amount,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Entry(data["type"], data["description"], data["amount"], data["date"])

class BudgetPlanner:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.entries = self.load_entries()

    def load_entries(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r") as f:
            data = json.load(f)
            return [Entry.from_dict(e) for e in data]

    def save_entries(self):
        with open(self.filename, "w") as f:
            json.dump([e.to_dict() for e in self.entries], f, indent=2)

    def add_entry(self, entry):
        self.entries.append(entry)
        self.save_entries()

    def list_entries(self):
        return self.entries

    def get_summary(self):
        income = sum(e.amount for e in self.entries if e.type == "income")
        expense = sum(e.amount for e in self.entries if e.type == "expense")
        return income, expense, income - expense
