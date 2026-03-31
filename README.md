# ₿ CryptoMind — AI Crypto Market Analyst

A production-ready **LangGraph ReAct agent** that autonomously calls real-time crypto price and news APIs, reasons over live data and serves a multi-turn conversational UI via Streamlit.
Powered by **Groq (LLaMA 3.3 & LLaMA 3.1)** & **HuggingFace (Qwen3 & Zephyr)** models, **FreeCryptoAPI**, and **NewsAPI**. 

Ask about any cryptocurrency — the agent fetches **live data**, reads **latest news**, and delivers **structured investment insights**.  

This isn't just a chatbot — it's a *reasoning agent* that:  

➡️ decides which tools to use\
➡️ gathers real-time information\
➡️ compares assets intelligently\
➡️ explains results clearly
<br><br>
  
## 🏗️ Architecture

```
User Input
    │
    ▼
Streamlit UI (app.py)
    │
    ▼
LangGraph ReAct Agent (agent.py)
    │  ┌─────────────────────────────────────┐
    ├──▶  crypto_list_tool  → FreeCryptoAPI  │
    ├──▶  crypto_data_tool  → FreeCryptoAPI  │  tools.py
    └──▶  crypto_news_tool  → NewsAPI        │
       └─────────────────────────────────────┘
    │
    ▼
Models (reasoning + response)
    ├──▶ Groq LLaMA 3.3 70B
    ├──▶ Groq LLaMA 3.1 8B
    ├──▶ HuggingFace (Qwen3-8B)
    └──▶ HuggingFace (Zephyr-7B)
    │
    ▼
MemorySaver (multi-turn conversation memory)
```

<br>

## ⚡ Local Setup

```bash
# 1. Clone / enter the project folder
cd crypto_agent

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys
# Edit .env and fill in your keys

# 5. Run
streamlit run app.py
```
<br> 

API Keys needed (all free tiers available):
| Key | Get it at |
|-----|-----------|
| `GROQ_API_KEY` | https://console.groq.com |
| `FREECRYPTO_TOKEN` | https://freecryptoapi.com |
| `NEWSAPI_KEY` | https://newsapi.org |
| `HF_API_KEY` | https://huggingface.co/ |

<br>

## 🗂 Project Structure

```plaintext
crypto_agent/
├── app.py            # Streamlit web UI
├── agent.py          # LangGraph ReAct agent + memory
├── tools.py          # Crypto data + news tools
├── requirements.txt
├── .env
└── README.md
```
