import json
from openai import OpenAI
from config import API_KEY, MODEL, BASE_URL

class Tool:
    def __init__(self, name, description, params, fn):
        self.name = name
        self.description = description
        self.params = params
        self.fn = fn

    def to_schema(self):
        props = {}
        for p, t in self.params.items():
            props[p] = {"type": t, "description": f"The {p} parameter"}
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": list(self.params.keys())
                }
            }
        }

    def execute(self, **kwargs):
        try:
            return self.fn(**kwargs)
        except Exception as e:
            return f"Error: {e}"

def run(query, tools, system_prompt, messages=None, verbose=True):
    if not API_KEY:
        return "Error: ZEN_API_KEY not found in .env", messages

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    if messages is None:
        messages = [{"role": "system", "content": system_prompt}]

    messages.append({"role": "user", "content": query})

    schemas = [t.to_schema() for t in tools]
    tool_map = {t.name: t for t in tools}

    for turn in range(15):
        if verbose:
            print(f"\nTurn {turn + 1}")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=schemas,
            tool_choice="auto"
        )

        msg = response.choices[0].message
        messages.append(msg)

        if msg.tool_calls:
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)

                if verbose:
                    print(f"  -> {name}({args})")

                tool = tool_map.get(name)
                if tool:
                    result = tool.execute(**args)
                else:
                    result = f"Unknown tool: {name}"

                if verbose:
                    print(f"  <- {result[:80]}...")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })

            if len(messages) > 20:
                overflow = len(messages) - 10
                messages = [messages[0]] + messages[overflow:]
        else:
            return msg.content, messages

    return "Reached maximum turns.", messages
