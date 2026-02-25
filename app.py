"""Streamlit frontend for the Startup Domain Name Validator agent."""

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Startup Domain Validator",
    page_icon="🚀",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar – API key configuration
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("Provide your API keys below or set them in a `.env` file.")

    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        placeholder="sk-...",
    )
    firecrawl_key = st.text_input(
        "Firecrawl API Key",
        type="password",
        value=os.getenv("FIRECRAWL_API_KEY", ""),
        placeholder="fc-...",
    )

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if firecrawl_key:
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_key

    st.markdown("---")
    st.markdown(
        "**About**\n\n"
        "This app uses a [LangGraph](https://langchain-ai.github.io/langgraph/) "
        "agent and [Firecrawl](https://www.firecrawl.dev/) to check whether "
        "common domain variants for your startup are already live."
    )

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
st.title("🚀 Startup Domain Name Validator")
st.markdown(
    "Enter your startup name and the agent will check the most common domain "
    "extensions for availability using **Firecrawl**, then summarise the "
    "results with **GPT-4o-mini**."
)

startup_name = st.text_input(
    "Startup name:",
    placeholder="e.g. TechVision, DataFlow, CloudSync",
    max_chars=60,
)

run_button = st.button("🔍 Validate Domains", type="primary", use_container_width=False)

if run_button:
    # --- Validate inputs ---
    if not startup_name.strip():
        st.warning("Please enter a startup name.")
        st.stop()
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI API Key is missing. Add it in the sidebar or in your `.env` file.")
        st.stop()
    if not os.getenv("FIRECRAWL_API_KEY"):
        st.error("Firecrawl API Key is missing. Add it in the sidebar or in your `.env` file.")
        st.stop()

    # --- Run the agent ---
    with st.spinner("Running LangGraph agent… this may take a moment."):
        # Import here so the module is not loaded at startup (avoids import errors
        # before packages are installed in a fresh environment).
        from agent.graph import build_graph  # noqa: PLC0415

        graph = build_graph()
        result = graph.invoke(
            {
                "startup_name": startup_name.strip(),
                "domains": [],
                "validation_results": [],
                "summary": "",
            }
        )

    validation_results: list = result.get("validation_results", [])
    summary: str = result.get("summary", "")

    # --- Display domain results ---
    st.markdown("---")
    st.header("📋 Domain Availability Results")

    available = [r for r in validation_results if not r["exists"]]
    taken = [r for r in validation_results if r["exists"]]

    col_avail, col_taken = st.columns(2)

    with col_avail:
        st.subheader("✅ Available")
        if available:
            for r in available:
                st.success(f"**{r['domain']}**")
        else:
            st.info("None of the checked domains appear to be available.")

    with col_taken:
        st.subheader("❌ Already taken")
        if taken:
            for r in taken:
                st.error(f"**{r['domain']}**")
                if r.get("content_preview"):
                    with st.expander(f"Site preview – {r['domain']}"):
                        st.markdown(r["content_preview"])
        else:
            st.info("All checked domains appear to be available.")

    # --- Display AI summary ---
    if summary:
        st.markdown("---")
        st.header("🤖 AI Analysis")
        st.markdown(summary)
