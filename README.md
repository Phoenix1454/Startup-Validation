# Startup Domain Name Validator 🚀

A **LangGraph** agent with a **Streamlit** frontend that validates domain-name availability for your startup using **Firecrawl** and summarises the results with an OpenAI LLM.

---

## How it works

```
User enters startup name
        │
        ▼
[generate_domains]  – produces 7 common domain variants (.com, .io, .co, .ai, .app, get*.com, try*.com)
        │
        ▼
[validate_domains]  – calls Firecrawl for each domain to check whether it is live
        │
        ▼
[summarize_results] – asks GPT-4o-mini to summarise findings and recommend the best option
        │
        ▼
Streamlit UI displays available / taken domains + AI summary
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Phoenix1454/Startup-Validation.git
cd Startup-Validation
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=fc-...
```

> You can also paste the keys directly in the Streamlit sidebar at runtime.

---

## Running the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project structure

```
Startup-Validation/
├── app.py              # Streamlit frontend
├── agent/
│   ├── __init__.py
│   ├── graph.py        # LangGraph state-machine
│   └── tools.py        # Firecrawl domain-validation tool
├── requirements.txt
├── .env.example
└── README.md
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `langgraph` | Agent orchestration |
| `langchain-openai` | OpenAI LLM integration |
| `streamlit` | Web UI |
| `firecrawl-py` | Domain validation via web scraping |
| `python-dotenv` | Environment variable loading |
