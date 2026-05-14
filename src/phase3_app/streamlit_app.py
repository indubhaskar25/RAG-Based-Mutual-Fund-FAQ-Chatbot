import streamlit as st
import os
import sys
import base64
import time
from datetime import datetime

# 1. ABSOLUTE STABILITY SHIELD
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["DEVICE"] = "cpu"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Add root directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.phase1_ingestion.vector_store import VectorStoreManager
from src.phase2_rag.groq_client import GroqRAGClient
from src.phase2_rag.guardrail import QueryGuardrail

# 2. PAGE CONFIG
st.set_page_config(
    page_title="GROWW RAG AI Chatbot",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. ENGINE INIT (cached for deployment stability)
@st.cache_resource(show_spinner=False)
def load_engine():
    vs = VectorStoreManager(persist_directory="chromadb_store")
    retriever = vs.get_retriever(top_k=5)
    groq = GroqRAGClient()
    return vs, retriever, groq

if "engine_loaded" not in st.session_state:
    with st.spinner("Initializing GROWW RAG AI..."):
        vs, retriever, groq_client = load_engine()
        st.session_state.vs_manager = vs
        st.session_state.retriever = retriever
        st.session_state.groq_client = groq_client
        st.session_state.engine_loaded = True

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# 4. AVATAR LOADER
def get_avatar_b64():
    avatar_path = os.path.join(os.path.dirname(__file__), "assets", "avatar.png")
    if os.path.exists(avatar_path):
        with open(avatar_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

AVATAR_B64 = get_avatar_b64()

def get_timestamp():
    return datetime.now().strftime("%I:%M %p")

# 5. GLOBAL CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
.stApp {{ background-color: #0b0c10 !important; font-family: 'Outfit', sans-serif; color: #e2e8f0; }}
[data-testid="stHeader"] {{ display: none !important; }}
[data-testid="stSidebar"] {{ background-color: #0d0e14 !important; border-right: 1px solid rgba(139,92,246,0.12); }}
[data-testid="stSidebar"] > div:first-child {{ padding-top: 0 !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}

/* ── Sidebar brand ── */
.sb-brand {{ padding: 28px 24px 12px; }}
.sb-brand-title {{ font-size: 1.35rem; font-weight: 800; background: linear-gradient(135deg, #8b5cf6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 0.5px; }}
.sb-brand-sub {{ font-family: 'JetBrains Mono'; font-size: 0.62rem; color: #475569; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; }}

/* ── Sidebar nav ── */
.sb-nav-item {{
    display: flex; align-items: center; gap: 12px;
    padding: 11px 24px; color: #94a3b8; font-size: 0.9rem;
    cursor: pointer; border-radius: 8px; margin: 2px 12px;
    transition: all 0.2s ease; border: 1px solid transparent;
}}
.sb-nav-item:hover {{ background: rgba(139,92,246,0.08); border-color: rgba(139,92,246,0.2); color: #c4b5fd; }}
.sb-nav-active {{ background: rgba(139,92,246,0.12); border-color: rgba(139,92,246,0.3); color: #c4b5fd; }}
.sb-nav-icon {{ font-size: 1rem; width: 20px; text-align: center; }}
.sb-divider {{ height: 1px; background: rgba(255,255,255,0.05); margin: 12px 24px; }}

/* ── AI Assistant Card ── */
.ai-card {{
    margin: 16px 12px; padding: 18px;
    background: linear-gradient(135deg, rgba(139,92,246,0.07), rgba(6,182,212,0.05));
    border: 1px solid rgba(139,92,246,0.2); border-radius: 14px;
}}
.ai-card-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }}
.ai-card-avatar {{
    width: 46px; height: 46px; border-radius: 12px;
    background: url('data:image/png;base64,{AVATAR_B64}') center/cover;
    border: 2px solid rgba(139,92,246,0.4); flex-shrink: 0;
}}
.ai-card-name {{ font-size: 0.92rem; font-weight: 700; color: #e2e8f0; }}
.ai-card-role {{ font-size: 0.72rem; color: #8b5cf6; font-family: 'JetBrains Mono'; }}
.ai-badge {{
    display: flex; align-items: center; gap: 7px;
    padding: 6px 10px; border-radius: 8px;
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
    font-size: 0.72rem; color: #94a3b8; margin-bottom: 6px;
}}
.ai-badge-dot {{ width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }}
.dot-green {{ background: #22c55e; box-shadow: 0 0 6px rgba(34,197,94,0.5); }}
.dot-purple {{ background: #8b5cf6; box-shadow: 0 0 6px rgba(139,92,246,0.5); }}
.dot-teal {{ background: #06b6d4; box-shadow: 0 0 6px rgba(6,182,212,0.5); }}

/* ── Header bar ── */
.top-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 36px; border-bottom: 1px solid rgba(255,255,255,0.05);
    background: rgba(11,12,16,0.95); position: sticky; top: 0; z-index: 100;
    backdrop-filter: blur(8px);
}}
.header-brand {{ font-size: 1.15rem; font-weight: 800; background: linear-gradient(135deg, #8b5cf6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.header-sep {{ color: rgba(255,255,255,0.1); font-size: 1.1rem; margin: 0 14px; }}
.header-sub {{ font-family: 'JetBrains Mono'; font-size: 0.68rem; color: #475569; letter-spacing: 2px; }}
.status-pill {{
    background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.25);
    padding: 5px 14px; border-radius: 20px; font-size: 0.72rem;
    font-family: 'JetBrains Mono'; color: #e2e8f0;
}}
.status-dot {{ color: #22c55e; margin-right: 5px; }}

/* ── Chat area ── */
.chat-area {{ max-width: 900px; margin: 0 auto; padding: 32px 24px 140px; }}

/* ── User bubble ── */
.user-row {{ display: flex; justify-content: flex-end; align-items: flex-end; gap: 12px; margin-bottom: 28px; }}
.user-bubble {{
    background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(6,182,212,0.08));
    border: 1px solid rgba(139,92,246,0.25); border-radius: 18px 18px 4px 18px;
    padding: 14px 20px; font-size: 0.97rem; line-height: 1.6; color: #e2e8f0;
    max-width: 75%;
}}
.user-avatar-pill {{
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}}
.msg-time {{ font-family: 'JetBrains Mono'; font-size: 0.6rem; color: #475569; margin-top: 6px; text-align: right; }}

/* ── Assistant bubble ── */
.ai-row {{ display: flex; align-items: flex-start; gap: 14px; margin-bottom: 28px; }}
.ai-row-avatar {{
    width: 42px; height: 42px; border-radius: 12px;
    background: url('data:image/png;base64,{AVATAR_B64}') center/cover;
    border: 1.5px solid rgba(139,92,246,0.35); flex-shrink: 0; margin-top: 2px;
}}
.ai-row-avatar-fallback {{
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; flex-shrink: 0; margin-top: 2px;
}}
.ai-bubble {{
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 4px 18px 18px 18px; padding: 16px 22px;
    font-size: 0.97rem; line-height: 1.7; color: #e2e8f0; flex: 1;
}}
.ai-meta {{ display: flex; gap: 8px; margin-top: 8px; align-items: center; }}
.ai-pill {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06); padding: 3px 9px; border-radius: 5px; font-family: 'JetBrains Mono'; font-size: 0.6rem; color: #475569; text-transform: uppercase; }}
.ai-time {{ font-family: 'JetBrains Mono'; font-size: 0.6rem; color: #475569; }}

/* ── Source cards ── */
.src-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }}
.src-card {{
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px; padding: 14px 16px;
}}
.src-label {{ font-family: 'JetBrains Mono'; font-size: 0.58rem; color: #475569; margin-bottom: 5px; text-transform: uppercase; }}
.src-name {{ font-size: 0.88rem; font-weight: 600; color: #c4b5fd; }}
.src-desc {{ font-size: 0.78rem; color: #64748b; margin-top: 4px; line-height: 1.4; }}

/* ── Typing indicator ── */
.typing-row {{ display: flex; align-items: center; gap: 14px; margin-bottom: 20px; }}
.typing-bubble {{ background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07); border-radius: 4px 18px 18px 18px; padding: 14px 20px; }}
.typing-dots {{ display: flex; gap: 5px; }}
.typing-dot {{ width: 7px; height: 7px; border-radius: 50%; background: #8b5cf6; opacity: 0.4; }}

/* ── Chat input override ── */
[data-testid="stChatInput"] {{ border: none !important; background: transparent !important; }}
[data-testid="stChatInput"] > div {{ background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(139,92,246,0.25) !important; border-radius: 16px !important; backdrop-filter: blur(10px); box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important; }}
[data-testid="stChatInput"] textarea {{ color: #e2e8f0 !important; }}
[data-testid="stChatInput"] textarea::placeholder {{ color: #475569 !important; }}
</style>
""", unsafe_allow_html=True)


def render_user(content, ts):
    st.markdown(
        f'<div class="chat-area" style="padding:0;">'
        f'<div class="user-row">'
        f'<div style="text-align:right;">'
        f'<div class="user-bubble">{content}</div>'
        f'<div class="msg-time">{ts}</div>'
        f'</div>'
        f'<div class="user-avatar-pill">👤</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_assistant(content, sources=None, ts=None):
    ts = ts or ""
    avatar_html = (
        f'<div class="ai-row-avatar"></div>'
        if AVATAR_B64
        else '<div class="ai-row-avatar-fallback">🤖</div>'
    )

    src_html = ""
    if sources:
        cards = "".join(
            f'<div class="src-card">'
            f'<div class="src-label">Source {i+1}</div>'
            f'<div class="src-name">{s.replace("_", " ").replace(".txt", "").title()}</div>'
            f'<div class="src-desc">Extracted from official ICICI Prudential AMC knowledge base.</div>'
            f'</div>'
            for i, s in enumerate(sources)
        )
        src_html = f'<div class="src-grid">{cards}</div>'

    st.markdown(
        f'<div class="chat-area" style="padding:0;">'
        f'<div class="ai-row">'
        f'{avatar_html}'
        f'<div style="flex:1;">'
        f'<div class="ai-bubble">{content}</div>'
        f'<div class="ai-meta">'
        f'<div class="ai-pill">RAG Retrieved</div>'
        f'<div class="ai-pill">Official Source</div>'
        f'<span class="ai-time">{ts}</span>'
        f'</div>'
        f'{src_html}'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def main():
    # ── SIDEBAR ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
            '<div class="sb-brand">'
            '<div class="sb-brand-title">GROWW RAG AI</div>'
            '<div class="sb-brand-sub">Mutual Fund Assistant</div>'
            '</div>',
            unsafe_allow_html=True
        )

        # AI Assistant Card
        st.markdown(
            '<div class="ai-card">'
            '<div class="ai-card-header">'
            f'<div class="ai-card-avatar"></div>'
            '<div>'
            '<div class="ai-card-name">GROWW AI</div>'
            '<div class="ai-card-role">Fund Intelligence Assistant</div>'
            '</div>'
            '</div>'
            '<div class="ai-badge"><div class="ai-badge-dot dot-green"></div>Groq API Connected</div>'
            '<div class="ai-badge"><div class="ai-badge-dot dot-purple"></div>Vector DB Loaded</div>'
            '<div class="ai-badge"><div class="ai-badge-dot dot-teal"></div>Official AMC Sources</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="sb-nav-item sb-nav-active"><span class="sb-nav-icon">💬</span>AI Conversation</div>'
            '<div class="sb-nav-item"><span class="sb-nav-icon">📚</span>Knowledge Base</div>'
            '<div class="sb-nav-item"><span class="sb-nav-icon">📈</span>Fund Insights</div>'
            '<div class="sb-nav-item"><span class="sb-nav-icon">ℹ️</span>About</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        if st.button("🗑️  Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown(
            '<div style="padding: 16px 12px; margin-top: 12px;">'
            '<div style="font-family: JetBrains Mono; font-size: 0.6rem; color: #334155; text-transform: uppercase; letter-spacing: 1px; text-align: center;">'
            'Powered by Groq · ChromaDB · LangChain'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # ── TOP HEADER ────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="top-header">'
        '<div style="display:flex;align-items:center;">'
        '<div class="header-brand">GROWW RAG AI Chatbot</div>'
        '<span class="header-sep">|</span>'
        '<div class="header-sub">Mutual Fund Intelligence</div>'
        '</div>'
        '<div class="status-pill"><span class="status-dot">●</span>Live · ICICI Prudential</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── CHAT BODY ─────────────────────────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-area">', unsafe_allow_html=True)

        if not st.session_state.messages:
            render_assistant(
                "Hello! I'm GROWW AI, your personal mutual fund intelligence assistant. "
                "I'm connected to official ICICI Prudential fund data and ready to answer "
                "factual questions about expense ratios, exit loads, NAVs, and more. "
                "How can I help you today?",
                ts=get_timestamp()
            )

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                render_user(msg["content"], ts=msg.get("ts", ""))
            else:
                render_assistant(msg["content"], sources=msg.get("sources"), ts=msg.get("ts", ""))

        if st.session_state.thinking:
            st.markdown(
                '<div class="chat-area" style="padding:0;">'
                '<div class="typing-row">'
                f'{"<div class=ai-row-avatar></div>" if AVATAR_B64 else "<div class=ai-row-avatar-fallback>🤖</div>"}'
                '<div class="typing-bubble">'
                '<div class="typing-dots">'
                '<div class="typing-dot"></div>'
                '<div class="typing-dot" style="opacity:0.65;animation-delay:0.15s"></div>'
                '<div class="typing-dot" style="opacity:0.9;animation-delay:0.3s"></div>'
                '</div>'
                '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── CHAT INPUT ────────────────────────────────────────────────────────────
    prompt = st.chat_input("Ask about mutual funds, expense ratios, exit loads...")

    if prompt:
        ts = get_timestamp()
        st.session_state.messages.append({"role": "user", "content": prompt, "ts": ts})
        st.session_state.thinking = True
        st.rerun()

    # ── RAG ENGINE ────────────────────────────────────────────────────────────
    if st.session_state.thinking:
        last_q = st.session_state.messages[-1]["content"]
        ts = get_timestamp()
        try:
            if QueryGuardrail.is_advisory(last_q):
                ans = QueryGuardrail.get_refusal_response()["answer"]
                sources = []
            else:
                docs = st.session_state.retriever.invoke(last_q)
                if not docs:
                    ans = "I couldn't find relevant information in the knowledge base. Please try rephrasing your question."
                    sources = []
                else:
                    raw = st.session_state.groq_client.generate_answer(last_q, docs)
                    ans = raw.split("Source:")[0].strip()
                    sources = list(set(
                        [doc.metadata.get("source", "Official Doc").split("/")[-1] for doc in docs]
                    ))[:2]

            st.session_state.messages.append({
                "role": "assistant",
                "content": ans,
                "sources": sources,
                "ts": ts
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ I encountered a temporary issue. Please try again in a moment.",
                "sources": [],
                "ts": ts
            })
        st.session_state.thinking = False
        st.rerun()


if __name__ == "__main__":
    main()
