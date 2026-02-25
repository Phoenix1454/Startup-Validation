# 🚀 Startup Idea Validator

An AI-powered startup validation agent built with **LangGraph** and **Streamlit**. Describe your startup idea and get instant, data-driven feedback on market landscape, community sentiment, and technical feasibility.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Chat%20UI-red)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-green)

Active link: https://phoenix1454-startup-validation-srcapp-wjnche.streamlit.app

---

## Features

- **Market Landscape Research** — Searches the web via [Firecrawl](https://firecrawl.dev) for market size, competitors, and industry analysis.
- **Community Sentiment Analysis** — Queries Hacker News for relevant discussions, upvotes, and comment activity.
- **Technical Feasibility Assessment** — Searches GitHub for related open-source projects, star counts, and languages used.
- **Conversational Memory** — Remembers your idea across follow-up questions in the same session.
- **Streaming UI** — Real-time thinking indicators and token-by-token response streaming in a Streamlit chat interface.

## Architecture

```
User ── Streamlit Chat UI ── LangGraph ReAct Agent (o4-mini)
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
             Firecrawl      Hacker News      GitHub
           (market data)   (sentiment)    (feasibility)
```

| File | Purpose |
|------|---------|
| `src/app.py` | Streamlit chat interface with streaming |
| `src/validator.py` | LangGraph agent setup and system prompt |
| `src/tools.py` | Tool functions (Firecrawl, HN, GitHub) |

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### API Keys

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=fc-...
GITHUB_TOKEN=ghp_...        # optional, increases GitHub rate limit
```

### Installation

```bash
# Clone the repo
git clone https://github.com/Phoenix1454/Startup-Validation.git
cd Startup-Validation

# Install dependencies (using uv)
uv sync

# Or with pip
pip install -r pyproject.toml
```

### Run

```bash
python -m streamlit run src/app.py
```

The app will open at `http://localhost:8501`.

## Usage

1. **Describe your idea** — e.g. *"I want to build an AI-powered resume screening tool for small businesses"*
2. The agent will immediately research the market landscape and present findings.
3. **Ask follow-ups** — *"What about competitors?"*, *"Check community sentiment"*, *"Assess technical feasibility"*
4. **Full validation** — type *"Do a full validation"* to run all three tools and get a structured VALIDATE / NEEDS_WORK / REJECT recommendation.

## Tech Stack

| Technology | Role |
|------------|------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | ReAct agent orchestration with memory |
| [OpenAI o4-mini](https://platform.openai.com/) | LLM reasoning |
| [Firecrawl](https://firecrawl.dev) | Web search & scraping for market data |
| [Streamlit](https://streamlit.io) | Chat UI with streaming support |
| Hacker News API | Community sentiment via Algolia search |
| GitHub API | Open-source project discovery |

## License

MIT
