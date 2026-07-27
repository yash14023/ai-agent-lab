from core import Tool, run
from tools import web_search, save_file
from prompts import PLANNER as prompt

tools = [
    Tool("web_search", "Search the web for information", {"query": "string"}, web_search),
    Tool("save_file", "Save content to a file", {"filename": "string", "content": "string"}, save_file),
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
        answer, messages = run(query, tools, prompt, messages)
        print(answer)
