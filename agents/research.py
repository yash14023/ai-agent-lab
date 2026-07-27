from core import Tool, run
from tools import web_search, read_page
from prompts import RESEARCH as prompt

tools = [
    Tool("web_search", "Search the web for information", {"query": "string"}, web_search),
    Tool("read_page", "Read and extract text from a URL", {"url": "string"}, read_page),
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
