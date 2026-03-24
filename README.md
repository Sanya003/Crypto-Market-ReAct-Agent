# Crypto-Market-ReAct-Agent
LLM-powered Crypto Market Analyst Agent built using LangGraph, tool calling, and real-time APIs. The agent can fetch cryptocurrency prices, compare assets, and analyze latest news before providing structured investment insights.

## Features
- 🔎 Real-time cryptocurrency data retrieval
- 📰 Latest crypto news analysis
- 🧠 Multi-step reasoning using ReAct pattern
- 🛠 Tool calling with LangChain + LangGraph
- 💾 Conversational memory support
- 📊 Structured investment insights
- ⚡ CLI interactive chat interface
- 🔐 Environment variable based API management

## Architecture
```
User Query
    ↓
LangGraph ReAct Agent
    ↓
Tool Selection (LLM reasoning)
    ↓
Crypto APIs + News API
    ↓
Structured Analysis Response

```

## Usage
Run the agent:

```python
python main.py
```

Example interaction:
```
👤 You: Compare XRP and DOGE and tell me which is better?
🤖 Agent:
Summary
...
Market Data
...
News Highlights
...
Recommendation
...
```

## Project Structure
```plaintext
crypto-react-agent/
│
├── main.py
├── test.py
├── .env
├── requirements.txt
└── README.md
```

## Tools Implemented
- **crypto_list_tool** → Fetch available cryptocurrencies
- **crypto_data_tool** → Get crypto price data
- **crypto_news_tool** → Fetch latest news
