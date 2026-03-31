import os
import json
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

from tools import ALL_TOOLS

HF_API_KEY = st.secrets.get("HF_API_KEY") or os.getenv("HF_API_KEY")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

MAX_HISTORY = 6
TOOL_CONTENT_LIMIT = 1500

SYS_PROMPT = SystemMessage(
    content="""
        You are a professional Crypto Market Analyst Agent.
        You answer user questions about cryptocurrencies, market data, and recent news.

        AVAILABLE TOOLS:
        - crypto_list_tool(limit): get a condensed list of available crypto tickers.
        - crypto_data_tool(symbol): get real-time data for a symbol (e.g., BTC, ETH).
        - crypto_news_tool(query, max_items): get the latest news headlines + URLs.

        GUIDELINES:
        1) Think step-by-step and decide which tools to call.
        2) Use tools to retrieve data; never fabricate prices or metrics.
        3) Keep responses concise and scannable with bullet points.
        4) Provide helpful context when the user seems new to crypto.

        FORMAT (always use Markdown):
        - Bold section headers: **Summary**, **Data**, **What it means**, **Next steps**
        - Bullet points for data fields
        - Never reveal API keys or tokens.
        - If an endpoint errors, explain clearly and suggest alternatives.
    """
)


def _truncate_tool_messages(messages: list) -> list:
    """
    Truncate ToolMessage content to TOOL_CONTENT_LIMIT chars.
    """
    result = []
    for m in messages:
        if isinstance(m, ToolMessage) and len(str(m.content)) > TOOL_CONTENT_LIMIT:
            truncated = str(m.content)[:TOOL_CONTENT_LIMIT] + "... [truncated]"
            m = ToolMessage(content=truncated, tool_call_id=m.tool_call_id)
        result.append(m)
    return result


def _trim_and_clean(messages: list) -> list:
    """
    1. Keep only last MAX_HISTORY messages.
    2. Truncate tool response blobs.
    3. Ensure list never starts with a ToolMessage.
    """
    trimmed = messages[-MAX_HISTORY:] if len(messages) > MAX_HISTORY else messages
    trimmed = _truncate_tool_messages(trimmed)

    while trimmed and isinstance(trimmed[0], ToolMessage):
        trimmed = trimmed[1:]

    return trimmed


def _get_llm(provider: str):
    """Return the LLM for the chosen provider."""
    if provider == "HuggingFace (Qwen3-8B)":
        endpoint = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen3-8B",
            huggingfacehub_api_token=HF_API_KEY,
            task="text-generation",
            max_new_tokens=1024,
            temperature=0.1,
        )
        return ChatHuggingFace(llm=endpoint)

    elif provider == "HuggingFace (Zephyr-7B)":
        endpoint = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            huggingfacehub_api_token=HF_API_KEY,
            task="text-generation",
            max_new_tokens=1024,
            temperature=0.1,
        )
        return ChatHuggingFace(llm=endpoint)

    else:
        model_map = {
            "Groq - LLaMA 3.3 70B (default)": "llama-3.3-70b-versatile",
            "Groq - LLaMA 3.1 8B (faster)":   "llama-3.1-8b-instant",
        }
        model = model_map.get(provider, "llama-3.3-70b-versatile")
        return ChatGroq(
            model=model,
            groq_api_key=GROQ_API_KEY,
            temperature=0,
        )


def build_agent(thread_id: str = "default", provider: str = "Groq - LLaMA 3.3 70B (default)"):
    """Build and return a compiled LangGraph ReAct agent with memory + smart trimming."""
    llm = _get_llm(provider)
    llm_with_tools = llm.bind_tools(ALL_TOOLS)
    tool_node = ToolNode(tools=ALL_TOOLS)

    def assistant(state: MessagesState):
        cleaned = _trim_and_clean(state["messages"])
        return {"messages": [llm_with_tools.invoke([SYS_PROMPT] + cleaned)]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": thread_id}}

    return graph, config
