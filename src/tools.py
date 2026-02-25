from dotenv import load_dotenv
import os
import requests
from firecrawl import FirecrawlApp, V1ScrapeOptions as ScrapeOptions
from langgraph.config import get_stream_writer
 
load_dotenv()

def research_market_landscape(startup_idea: str) -> str:
    """Research the market landscape for a startup idea, including market size, competitors, and industry analysis."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        return "❌ Error: FIRECRAWL_API_KEY environment variable is required"
 
    app = FirecrawlApp(api_key=api_key)
    writer = get_stream_writer()
    writer(f"TOOL USE: Researching market data for {startup_idea}...")

    search_result = app.search(
    f"{startup_idea} market size competitors industry analysis",
    limit=5,
    scrape_options=ScrapeOptions(formats=["markdown"])
)
    
def analyze_community_sentiment(startup_idea: str) -> str:
    """Analyze community sentiment about a startup idea using Hacker News discussions."""
    writer = get_stream_writer()
    writer(f"TOOL USE: Analyzing community sentiment using Hacker News...")
 
    search_url = "https://hn.algolia.com/api/v1/search"
    params = {"query": startup_idea, "tags": "story", "hitsPerPage": 10}
    response = requests.get(search_url, params=params)

def assess_technical_feasibility(startup_idea: str) -> str:
    """Assess the technical feasibility of a startup idea by searching GitHub for related open-source projects."""
    github_token = os.getenv("GITHUB_TOKEN")
    search_url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {github_token}"}
    params = {
        "q": startup_idea.replace(" ", "+"),
        "sort": "stars", "order": "desc", "per_page": 10
    }

