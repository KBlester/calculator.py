import json
import os
from typing import List


class HistoryManager:
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            storage_path = os.path.join(os.path.expanduser("~"), ".calculadora_history.json")
        self.storage_path = storage_path
        self.history: List[str] = []
        self.load()

    def add(self, entry: str):
        self.history.append(entry)
        self.save()

    def get_all(self) -> List[str]:
        return list(self.history)

    def clear(self):
        self.history.clear()
        self.save()

    def remove(self, index: int):
        if 0 <= index < len(self.history):
            self.history.pop(index)
            self.save()

    def load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []

    def save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError:
            pass
