import json
import os
import re
from datetime import datetime
from core import Tool, run
from prompts import JOURNAL as prompt

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "journal_entries.json")

class MemoryStore:
    def __init__(self, filepath=MEMORY_FILE):
        self.filepath = filepath
        self._ensure()

    def _ensure(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def save(self, text, reflection=""):
        with open(self.filepath, "r") as f:
            entries = json.load(f)
        entries.append({
            "text": text,
            "reflection": reflection,
            "timestamp": datetime.now().isoformat()
        })
        with open(self.filepath, "w") as f:
            json.dump(entries, f, indent=2)

    def find_similar(self, text, top_k=3):
        with open(self.filepath, "r") as f:
            entries = json.load(f)
        words = set(re.findall(r'\w+', text.lower()))
        scored = []
        for e in entries:
            e_words = set(re.findall(r'\w+', e["text"].lower()))
            overlap = len(words & e_words)
            total = len(words | e_words)
            score = overlap / max(total, 1)
            scored.append((score, e))
        scored.sort(reverse=True)
        return [e for s, e in scored[:top_k] if s > 0.05]

def get_related(text):
    store = MemoryStore()
    similar = store.find_similar(text)
    if not similar:
        return "No strongly related past entries found."
    result = "Related past entries:\n"
    for i, e in enumerate(similar, 1):
        result += f"{i}. [{e['timestamp'][:10]}] {e['text'][:200]}\n"
    return result

tools = [
    Tool("get_related", "Find past journal entries similar to the given text", {"text": "string"}, get_related),
]

def run_agent():
    messages = None
    print("Commands: 'exit' = menu, 'new' = fresh chat\n")
    while True:
        query = input("> ").strip()
        if query.lower() in ("exit", "quit"):
            break
        if query.lower() == "new":
            messages = None
            print("--- New chat ---")
            continue
        if not query:
            continue
        store = MemoryStore()
        answer, messages = run(query, tools, prompt, messages)
        store.save(query, answer)
        print(answer)
