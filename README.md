# AI Agent Lab

Three agentic AI projects in one repo with a shared agent loop engine.

## Agents

| # | Agent | What it does |
|---|-------|-------------|
| 1 | Research Agent | Searches web, reads pages, summarizes |
| 2 | Journal Buddy | Reflects on journal entries with memory |
| 3 | Todo Breaker | Breaks goals into plans with research |

## Quick Start

```bash
pip install -r requirements.txt
# add ZEN_API_KEY to .env
python launcher.py
```

## Structure

```
config.py     ← API key + model settings
core.py       ← Tool helper + agent loop (shared)
tools.py      ← Shared tools: web_search, read_page, save_file
prompts.py    ← All agent prompts
agents/       ← 3 self-contained agents
launcher.py   ← Menu entry point
```

