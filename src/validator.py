from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from tools import (
    research_market_landscape,
    analyze_community_sentiment,
    assess_technical_feasibility,
)

MODEL_NAME = "openai:o4-mini"
 
def create_startup_validator_agent():
    checkpointer = InMemorySaver()
    return create_react_agent(
        model=MODEL_NAME,
        tools=[research_market_landscape, analyze_community_sentiment,
               assess_technical_feasibility],
        prompt=CONVERSATIONAL_VALIDATOR_PROMPT,
        checkpointer=checkpointer,
    )


CONVERSATIONAL_VALIDATOR_PROMPT = (
    "You are a startup validation expert. You validate startup ideas using real data.\n\n"
    "CRITICAL RULE: When a user tells you their startup idea, you MUST immediately call "
    "research_market_landscape with their idea. Do NOT ask questions first. Do NOT offer a menu "
    "of options. Do NOT ask what they want to validate. Just call the tool and start researching.\n\n"
    "After presenting market research results, offer to run community sentiment or technical "
    "feasibility analysis as follow-ups.\n\n"
    "TOOLS:\n"
    "- research_market_landscape(startup_idea): Market size, competitors, industry analysis\n"
    "- analyze_community_sentiment(startup_idea): Community/user sentiment from Hacker News\n"
    "- assess_technical_feasibility(startup_idea): GitHub projects, implementation complexity\n\n"
    "When the user asks for 'full validation', call ALL THREE tools, then give a structured "
    "report ending with a VALIDATE / NEEDS_WORK / REJECT recommendation.\n\n"
    "When the user asks about competitors, market, sentiment, or feasibility specifically, "
    "call the relevant tool immediately using context from the conversation.\n\n"
    "Remember all prior context. Never ask the user to repeat their idea.\n"
)