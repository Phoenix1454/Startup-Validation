"""LangGraph state-machine for startup domain validation.

Graph flow:
    generate_domains → validate_domains → summarize_results → END
"""

import re
from typing import List, TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from agent.tools import validate_domain


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class ValidationState(TypedDict):
    """Shared state passed between graph nodes."""

    startup_name: str
    domains: List[str]
    validation_results: List[dict]
    summary: str


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

def generate_domains(state: ValidationState) -> ValidationState:
    """Generate common domain-name variations from the startup name."""
    raw = state["startup_name"]
    clean = re.sub(r"[^a-z0-9]", "", raw.lower())

    domains: List[str] = [
        f"{clean}.com",
        f"{clean}.io",
        f"{clean}.co",
        f"{clean}.ai",
        f"{clean}.app",
        f"get{clean}.com",
        f"try{clean}.com",
    ]

    return {**state, "domains": domains}


def validate_domains(state: ValidationState) -> ValidationState:
    """Run Firecrawl validation for every domain in the list."""
    results = [validate_domain(domain) for domain in state["domains"]]
    return {**state, "validation_results": results}


def summarize_results(state: ValidationState) -> ValidationState:
    """Use an LLM to produce a human-friendly summary of the results."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    lines = []
    for r in state["validation_results"]:
        label = "TAKEN" if r["exists"] else "AVAILABLE"
        lines.append(f"- {r['domain']}: {label} ({r['status']})")
    results_text = "\n".join(lines)

    prompt = (
        f"I am validating domain names for a startup called \"{state['startup_name']}\".\n\n"
        "Here are the findings:\n"
        f"{results_text}\n\n"
        "Please provide a concise summary that:\n"
        "1. Lists the available domains.\n"
        "2. Lists the taken domains.\n"
        "3. Recommends the best domain choice with a short explanation."
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "summary": response.content}


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def build_graph():
    """Compile and return the LangGraph agent."""
    graph = StateGraph(ValidationState)

    graph.add_node("generate_domains", generate_domains)
    graph.add_node("validate_domains", validate_domains)
    graph.add_node("summarize_results", summarize_results)

    graph.set_entry_point("generate_domains")
    graph.add_edge("generate_domains", "validate_domains")
    graph.add_edge("validate_domains", "summarize_results")
    graph.add_edge("summarize_results", END)

    return graph.compile()
