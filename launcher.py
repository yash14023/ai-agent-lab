import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

def main():
    agents = {
        "1": ("agents.research", "Research Agent"),
        "2": ("agents.journal", "Journal Buddy"),
        "3": ("agents.planner", "Todo Breaker"),
    }

    while True:
        print("\n=== AI Agent Lab ===")
        for k, (_, name) in agents.items():
            print(f"{k}. {name}")
        print("0. Exit\n")

        choice = input("Pick an agent (1-3): ").strip()

        if choice == "0":
            break

        if choice not in agents:
            print("Invalid choice.")
            continue

        module_path, label = agents[choice]
        import importlib
        module = importlib.import_module(module_path)
        print(f"\n--- {label} ---")
        getattr(module, "run_agent")()

if __name__ == "__main__":
    main()
