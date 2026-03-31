import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv(override=True)

# Page config 
st.set_page_config(
    page_title="CryptoMind · AI Analyst",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg:       #080c10;
    --surface:  #0d1117;
    --border:   #1c2433;
    --accent:   #00e5ff;
    --accent2:  #7c3aed;
    --positive: #00e676;
    --text:     #e2e8f0;
    --muted:    #64748b;
}

html, body, .stApp { background-color: var(--bg) !important; font-family: 'Syne', sans-serif; color: var(--text); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1100px; }

/* Sidebar */
[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border); }
[data-testid="stSidebar"] * { color: var(--text) !important; }
/* Reduce Streamlit's default sidebar internal padding so everything fits */
[data-testid="stSidebar"] > div:first-child { padding: 0.75rem 0.85rem !important; }
/* Shrink gap between sidebar widgets */
[data-testid="stSidebar"] .stButton { margin-bottom: 0.2rem !important; }
[data-testid="stSidebar"] .stButton > button { padding: 0.25rem 0.6rem !important; font-size: 0.7rem !important; }

/*  Chat messages: override Streamlit's default bubbles  */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0 !important;
    margin-bottom: 0.75rem !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    background: transparent !important;
}

/* USER bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
[data-testid="stChatMessage"][data-user="true"] {
    flex-direction: row-reverse !important;
}

/* Style all message content blocks */
[data-testid="stChatMessage"] > div:last-child {
    max-width: 76%;
    padding: 0.85rem 1.15rem;
    border-radius: 16px;
    font-size: 0.9rem;
    line-height: 1.75;
    border: 1px solid var(--border);
    animation: fadeUp 0.22s ease;
}
@keyframes fadeUp { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

/* Avatar icons */
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarUser"] {
    width: 34px !important; height: 34px !important;
    border-radius: 8px !important;
    background: linear-gradient(135deg,#00e5ff22,#7c3aed33) !important;
    border: 1px solid var(--border) !important;
    font-size: 1rem !important;
}

/* Markdown inside bubbles */
[data-testid="stChatMessage"] p  { margin: 0.2rem 0; color: var(--text); }
[data-testid="stChatMessage"] strong { color: var(--accent); }
[data-testid="stChatMessage"] ul { padding-left: 1.2rem; margin: 0.4rem 0; }
[data-testid="stChatMessage"] li { margin: 0.15rem 0; }
[data-testid="stChatMessage"] code {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    background: #ffffff0d;
    padding: 1px 6px;
    border-radius: 4px;
    color: #a78bfa;
}
[data-testid="stChatMessage"] h3 { color: var(--accent); font-size: 0.95rem; margin: 0.6rem 0 0.2rem; }

/* Thinking dots */
.thinking { display:flex; gap:5px; padding:14px 18px;
    background:var(--surface); border:1px solid var(--border);
    border-radius:14px; width:fit-content; }
.thinking span { width:7px; height:7px; border-radius:50%; background:var(--accent);
    animation:bounce 1.2s ease infinite; }
.thinking span:nth-child(2){animation-delay:.2s}
.thinking span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-7px)}}

/* Status badge */
.status-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(0,230,118,0.08); border:1px solid rgba(0,230,118,0.25);
    border-radius:999px; padding:4px 12px; font-size:0.72rem;
    color:var(--positive); font-family:'Space Mono',monospace; margin-bottom:1.5rem;
}
.dot { width:7px; height:7px; border-radius:50%; background:var(--positive);
    animation:pulse 1.5s ease-in-out infinite; }
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}

/* Chat input */
[data-testid="stChatInput"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea { color: var(--text) !important; font-family:'Syne',sans-serif !important; font-size:0.9rem !important; }
[data-testid="stChatInput"] button { background: linear-gradient(135deg,var(--accent),var(--accent2)) !important; border-radius:8px !important; border:none !important; }

/* Buttons */
.stButton > button {
    background:transparent !important; border:1px solid var(--border) !important;
    color:var(--text) !important; font-family:'Space Mono',monospace !important;
    font-size:0.72rem !important; border-radius:8px !important;
    padding:0.3rem 0.7rem !important; transition:all 0.18s !important;
}
.stButton > button:hover { border-color:var(--accent) !important; color:var(--accent) !important; }

/* Selectbox */
[data-baseweb="select"] > div { background:var(--surface) !important; border-color:var(--border) !important; border-radius:8px !important; }
[data-baseweb="select"] span { color:var(--text) !important; }
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# Import agent
from agent import build_agent

# Session state 
DEFAULT_MODEL = "Groq - LLaMA 3.3 70B (default)"
MODEL_OPTIONS = [
    "Groq - LLaMA 3.3 70B (default)",
    "Groq - LLaMA 3.1 8B (faster)",
    "HuggingFace (Qwen3-8B)",
    "HuggingFace (Zephyr-7B)",
]

if "agent" not in st.session_state:
    st.session_state._last_model = DEFAULT_MODEL
    st.session_state.agent, st.session_state.config = build_agent("web-1", provider=DEFAULT_MODEL)
if "messages" not in st.session_state:
    st.session_state.messages = []

#  Sidebar 
with st.sidebar:
    st.markdown("""
    <div style='padding:0.6rem 0 0.7rem;border-bottom:1px solid #1c2433;margin-bottom:0.7rem;'>
        <div style='display:flex;align-items:center;justify-content:space-between;'>
            <div style='display:flex;align-items:center;gap:8px;'>
                <span style='font-size:1.5rem;background:linear-gradient(135deg,#00e5ff,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>₿</span>
                <div>
                    <div style='font-size:1.1rem;font-weight:800;line-height:1.1;background:linear-gradient(90deg,#00e5ff,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>CryptoMind</div>
                    <div style='font-size:0.55rem;color:#64748b;font-family:Space Mono,monospace;letter-spacing:1.5px;text-transform:uppercase;'>AI Market Analyst</div>
                </div>
            </div>
            <div style='display:inline-flex;align-items:center;gap:5px;background:rgba(0,230,118,0.08);border:1px solid rgba(0,230,118,0.25);border-radius:999px;padding:3px 9px;font-size:0.62rem;color:#00e676;font-family:Space Mono,monospace;'>
                <div style='width:6px;height:6px;border-radius:50%;background:#00e676;animation:pulse 1.5s ease-in-out infinite;'></div>Live
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<p style='font-size:0.72rem;font-weight:700;letter-spacing:1px;color:#94a3b8;margin:0 0 0.35rem;text-transform:uppercase;'>⚡ Quick Prompts</p>", unsafe_allow_html=True)
    quick_prompts = [
        ("📈", "BTC price & sentiment"),
        ("🔄", "XRP vs DOGE — which to buy?"),
        ("📰", "Latest crypto news"),
        ("🏆", "Top 10 coins by market cap"),
        ("🔍", "Analyze ETH right now"),
    ]
    for icon, label in quick_prompts:
        if st.button(f"{icon} {label}", use_container_width=True, key=f"qp_{label}"):
            st.session_state._pending = label

    st.markdown("<hr style='margin:0.6rem 0;border-color:#1c2433;'>", unsafe_allow_html=True)

    # Model selector
    st.markdown("<p style='font-size:0.72rem;font-weight:700;letter-spacing:1px;color:#94a3b8;margin:0 0 0.35rem;text-transform:uppercase;'>🤖 Model</p>", unsafe_allow_html=True)
    selected_model = st.selectbox("", MODEL_OPTIONS, key="model_choice", label_visibility="collapsed")
    if st.session_state.get("_last_model") != selected_model:
        st.session_state._last_model = selected_model
        st.session_state.agent, st.session_state.config = build_agent("web-model-change", provider=selected_model)
        st.session_state.messages = []
        st.rerun()

    st.markdown("<hr style='margin:0.6rem 0;border-color:#1c2433;'>", unsafe_allow_html=True)

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent, st.session_state.config = build_agent(
            "web-reset", provider=st.session_state.get("model_choice", DEFAULT_MODEL)
        )
        st.rerun()

    st.markdown("""
    <div style='margin-top:0.7rem;font-size:0.62rem;color:#334155;font-family:Space Mono,monospace;line-height:1.8;text-align:center;'>
    LangGraph · Groq · HuggingFace · FreeCrypto · NewsAPI
    </div>
    """, unsafe_allow_html=True)

#  Main header 
st.markdown("""
<div style='padding-bottom:0.75rem;border-bottom:1px solid #1c2433;margin-bottom:1.5rem;'>
    <h2 style='margin:0;font-size:1.5rem;font-weight:800;
               background:linear-gradient(90deg,#00e5ff,#7c3aed);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        Crypto Intelligence Chat
    </h2>
    <p style='margin:4px 0 0;font-size:0.8rem;color:#64748b;font-family:Space Mono,monospace;'>
        Real-time data · News · AI analysis · Multi-turn memory
    </p>
</div>
""", unsafe_allow_html=True)

#  Empty state 
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;padding:3.5rem 0;color:#334155;'>
        <div style='font-size:3rem;margin-bottom:1rem;'>₿</div>
        <div style='font-size:1.1rem;font-weight:600;color:#475569;'>Ask me anything about crypto</div>
        <div style='font-size:0.8rem;color:#334155;margin-top:6px;font-family:Space Mono,monospace;'>
            prices · news · analysis · comparisons
        </div>
    </div>
    """, unsafe_allow_html=True)

#  Render history 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

#  Quick-prompt injection 
user_input = st.chat_input("Ask about any coin, price, or news…")
pending = st.session_state.pop("_pending", None)
if pending:
    user_input = pending

#  Handle input 
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
        <div class="thinking">
            <span></span><span></span><span></span>
        </div>
        """, unsafe_allow_html=True)

        try:
            result = st.session_state.agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                st.session_state.config,
            )
            last_ai = next((m for m in reversed(result["messages"]) if m.type == "ai"), None)
            reply = last_ai.content if last_ai else "Sorry, I couldn't get a response."
        except Exception as e:
            reply = f"**Error:** {e}"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
