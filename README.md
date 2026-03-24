# Crypto-Market-ReAct-Agent

> Your AI-powered crypto analyst that **thinks, researches, and compares** before giving insights.

An intelligent **LLM-driven Crypto Market Analyst** built with **LangGraph + Tool Calling + Real-time APIs**.  
Ask about any cryptocurrency — the agent fetches **live data**, reads **latest news**, and delivers **structured investment insights**.  

This isn't just a chatbot — it's a *reasoning agent* that:  

➡️ decides which tools to use\
➡️ gathers real-time information\
➡️ compares assets intelligently\
➡️ explains results clearly
<br><br>

## 🚀 What it can do

- 🔎 Fetch **real-time cryptocurrency prices**
- 📰 Analyze **latest crypto news**
- ⚖️ Compare **multiple coins intelligently**
- 🧠 Multi-step reasoning using **ReAct pattern**
- 🛠 Smart **tool calling** with LangGraph
- 💾 **Conversational memory** support
- 📊 Clean, structured investment insights
- ⚡ Interactive **CLI chat agent**
<br>
  
## 🏗️ Architecture

```
❓ User Question
↓
🧠 LLM decides what to do
↓
🛠 Calls tools (price + news)
↓
📡 Fetches real-time data
↓
📊 Returns structured analysis

```
<br>

## ▶️ Run the Agent

```python
python main.py
```

### Example interaction:
```
👤 You: Compare XRP and DOGE — which is better?

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
<br>

## 🗂 Project Structure

```plaintext
crypto-react-agent/
│
├── main.py
├── test.py
├── .env
├── requirements.txt
├── README.md
└── README.md
```
<br>

## 🛠 Tools Used by the Agent
- **crypto_list_tool** → Fetch available cryptocurrencies
- **crypto_data_tool** → Get crypto price data
- **crypto_news_tool** → Fetch latest news
