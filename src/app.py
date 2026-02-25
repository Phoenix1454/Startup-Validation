import os
import streamlit as st
from langchain_core.messages import ToolMessage, AIMessageChunk, HumanMessage

# Load Streamlit Cloud secrets into environment variables (for deployed app)
for key in ["OPENAI_API_KEY", "FIRECRAWL_API_KEY", "GITHUB_TOKEN"]:
    if key in st.secrets:
        os.environ[key] = st.secrets[key]

from validator import create_startup_validator_agent

# Cache agent in session_state so memory persists across Streamlit reruns
if "agent" not in st.session_state:
    st.session_state.agent = create_startup_validator_agent()
agent = st.session_state.agent

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []
    welcome_msg = "👋 **Welcome!** I'm your startup validation assistant."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
user_input = st.chat_input("Ask me about your startup idea...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream agent response
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        response_placeholder = st.empty()
        thinking_placeholder.info("🤔 **Thinking...**")

        config = {"configurable": {"thread_id": "startup_session"}}
        full_response = ""

        try:
            for stream_mode, chunk in agent.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode=["messages", "custom"],
            ):
                if stream_mode == "custom":
                    if chunk:
                        chunk_str = str(chunk).lower()
                        if "market" in chunk_str or "research" in chunk_str:
                            thinking_placeholder.info("🔍 **Researching market data...**")
                        elif "community" in chunk_str or "hacker news" in chunk_str:
                            thinking_placeholder.info("📊 **Analyzing community sentiment...**")
                        elif "github" in chunk_str or "technical" in chunk_str:
                            thinking_placeholder.info("⚙️ **Assessing technical feasibility...**")
                elif stream_mode == "messages":
                    if isinstance(chunk[0], AIMessageChunk):
                        if chunk[0].content:
                            full_response += chunk[0].content
                            response_placeholder.markdown(full_response + "▌")
        except Exception as e:
            full_response = f"❌ **Error:** {str(e)}\nPlease try asking your question again."

        thinking_placeholder.empty()
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})