"""
GROWW RAG AI Chatbot — Main Application
Multi-section fintech AI platform with sidebar navigation.
"""
import streamlit as st
import os
import sys
import base64

# Stability shield
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["DEVICE"] = "cpu"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.phase1_ingestion.vector_store import VectorStoreManager
from src.phase2_rag.groq_client import GroqRAGClient
from src.phase3_app.pages import chat_page, faq_page, insights_page, about_page

# ── Page Config ──
st.set_page_config(
    page_title="GROWW RAG AI Chatbot",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Engine Init ──
@st.cache_resource(show_spinner=False)
def load_engine():
    vs = VectorStoreManager(persist_directory="chromadb_store")
    return vs, vs.get_retriever(top_k=5), GroqRAGClient()

if "engine_loaded" not in st.session_state:
    with st.spinner("Initializing GROWW RAG AI..."):
        vs, ret, groq = load_engine()
        st.session_state.vs_manager = vs
        st.session_state.retriever = ret
        st.session_state.groq_client = groq
        st.session_state.engine_loaded = True
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thinking" not in st.session_state:
    st.session_state.thinking = False
if "page" not in st.session_state:
    st.session_state.page = "chat"

# ── Avatar ──
def _load_avatar():
    p = os.path.join(os.path.dirname(__file__), "assets", "avatar.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

AVATAR_B64 = _load_avatar()

# ── CSS ──
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp {{ background:#0b0c10 !important; font-family:'Outfit',sans-serif; color:#e2e8f0; }}
[data-testid="stHeader"] {{ display:none !important; }}
[data-testid="stSidebar"] {{ background:#0d0e14 !important; border-right:1px solid rgba(139,92,246,0.12); }}
[data-testid="stSidebar"] > div:first-child {{ padding-top:0 !important; }}
.block-container {{ padding:0 !important; max-width:100% !important; }}

/* Sidebar */
.sb-brand {{ padding:28px 24px 12px; }}
.sb-brand-title {{ font-size:1.35rem;font-weight:800;background:linear-gradient(135deg,#8b5cf6,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }}
.sb-brand-sub {{ font-family:'JetBrains Mono';font-size:0.62rem;color:#475569;text-transform:uppercase;letter-spacing:2px;margin-top:4px; }}
.sb-divider {{ height:1px;background:rgba(255,255,255,0.05);margin:12px 24px; }}

/* AI Card */
.ai-card {{ margin:16px 12px;padding:18px;background:linear-gradient(135deg,rgba(139,92,246,0.07),rgba(6,182,212,0.05));border:1px solid rgba(139,92,246,0.2);border-radius:14px; }}
.ai-card-header {{ display:flex;align-items:center;gap:12px;margin-bottom:12px; }}
.ai-card-avatar {{ width:46px;height:46px;border-radius:12px;background:url('data:image/png;base64,{AVATAR_B64}') center/cover;border:2px solid rgba(139,92,246,0.4);flex-shrink:0; }}
.ai-card-name {{ font-size:0.92rem;font-weight:700;color:#e2e8f0; }}
.ai-card-role {{ font-size:0.72rem;color:#8b5cf6;font-family:'JetBrains Mono'; }}
.ai-badge {{ display:flex;align-items:center;gap:7px;padding:6px 10px;border-radius:8px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);font-size:0.72rem;color:#94a3b8;margin-bottom:6px; }}
.ai-badge-dot {{ width:7px;height:7px;border-radius:50%;flex-shrink:0; }}
.dot-green {{ background:#22c55e;box-shadow:0 0 6px rgba(34,197,94,0.5); }}
.dot-purple {{ background:#8b5cf6;box-shadow:0 0 6px rgba(139,92,246,0.5); }}
.dot-teal {{ background:#06b6d4;box-shadow:0 0 6px rgba(6,182,212,0.5); }}

/* Header */
.top-header {{ display:flex;justify-content:space-between;align-items:center;padding:16px 36px;border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(11,12,16,0.95);position:sticky;top:0;z-index:100;backdrop-filter:blur(8px); }}
.header-brand {{ font-size:1.15rem;font-weight:800;background:linear-gradient(135deg,#8b5cf6,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }}
.header-sep {{ color:rgba(255,255,255,0.1);font-size:1.1rem;margin:0 14px; }}
.header-sub {{ font-family:'JetBrains Mono';font-size:0.68rem;color:#475569;letter-spacing:2px; }}
.status-pill {{ background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.25);padding:5px 14px;border-radius:20px;font-size:0.72rem;font-family:'JetBrains Mono';color:#e2e8f0; }}
.status-dot {{ color:#22c55e;margin-right:5px; }}

/* Chat elements */
.user-row {{ display:flex;justify-content:flex-end;align-items:flex-end;gap:12px;margin-bottom:28px;max-width:900px;margin-left:auto;margin-right:auto;padding:0 24px; }}
.user-bubble {{ background:linear-gradient(135deg,rgba(139,92,246,0.15),rgba(6,182,212,0.08));border:1px solid rgba(139,92,246,0.25);border-radius:18px 18px 4px 18px;padding:14px 20px;font-size:0.97rem;line-height:1.6;color:#e2e8f0;max-width:75%; }}
.user-avatar-pill {{ width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#8b5cf6,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0; }}
.msg-time {{ font-family:'JetBrains Mono';font-size:0.6rem;color:#475569;margin-top:6px;text-align:right; }}

.ai-row {{ display:flex;align-items:flex-start;gap:14px;margin-bottom:28px;max-width:900px;margin-left:auto;margin-right:auto;padding:0 24px; }}
.ai-row-avatar {{ width:42px;height:42px;border-radius:12px;background-size:cover;background-position:center;border:1.5px solid rgba(139,92,246,0.35);flex-shrink:0;margin-top:2px; }}
.ai-row-avatar-fallback {{ width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#8b5cf6,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0;margin-top:2px; }}
.ai-bubble {{ background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:4px 18px 18px 18px;padding:16px 22px;font-size:0.97rem;line-height:1.7;color:#e2e8f0; }}
.ai-meta {{ display:flex;gap:8px;margin-top:8px;align-items:center; }}
.ai-pill {{ background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);padding:3px 9px;border-radius:5px;font-family:'JetBrains Mono';font-size:0.6rem;color:#475569;text-transform:uppercase; }}
.ai-time {{ font-family:'JetBrains Mono';font-size:0.6rem;color:#475569; }}

.src-grid {{ display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px; }}
.src-card {{ background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:14px 16px; }}
.src-label {{ font-family:'JetBrains Mono';font-size:0.58rem;color:#475569;margin-bottom:5px;text-transform:uppercase; }}
.src-name {{ font-size:0.88rem;font-weight:600;color:#c4b5fd; }}
.src-desc {{ font-size:0.78rem;color:#64748b;margin-top:4px;line-height:1.4; }}

.typing-row {{ display:flex;align-items:center;gap:14px;margin-bottom:20px;max-width:900px;margin-left:auto;margin-right:auto;padding:0 24px; }}
.typing-bubble {{ background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:4px 18px 18px 18px;padding:14px 20px; }}
.typing-dots {{ display:flex;gap:5px; }}
.typing-dot {{ width:7px;height:7px;border-radius:50%;background:#8b5cf6;opacity:0.4; }}

@keyframes pulse {{ 0%,100% {{ opacity:0.3; }} 50% {{ opacity:1; }} }}

/* Chat input */
[data-testid="stChatInput"] {{ border:none !important;background:transparent !important; }}
[data-testid="stChatInput"] > div {{ background:rgba(255,255,255,0.04) !important;border:1px solid rgba(139,92,246,0.25) !important;border-radius:16px !important;box-shadow:0 4px 24px rgba(0,0,0,0.3) !important; }}
[data-testid="stChatInput"] textarea {{ color:#e2e8f0 !important; }}
[data-testid="stChatInput"] textarea::placeholder {{ color:#475569 !important; }}

/* Expanders */
.streamlit-expanderHeader {{ background:rgba(255,255,255,0.025) !important;border:1px solid rgba(255,255,255,0.07) !important;border-radius:10px !important;color:#e2e8f0 !important; }}
</style>
""", unsafe_allow_html=True)


def set_page(p):
    st.session_state.page = p


def main():
    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown(
            '<div class="sb-brand">'
            '<div class="sb-brand-title">GROWW RAG AI</div>'
            '<div class="sb-brand-sub">Mutual Fund Assistant</div>'
            '</div>',
            unsafe_allow_html=True
        )

        # AI Card
        st.markdown(
            '<div class="ai-card">'
            '<div class="ai-card-header">'
            '<div class="ai-card-avatar"></div>'
            '<div>'
            '<div class="ai-card-name">GROWW AI</div>'
            '<div class="ai-card-role">Fund Intelligence</div>'
            '</div></div>'
            '<div class="ai-badge"><div class="ai-badge-dot dot-green"></div>Groq API Connected</div>'
            '<div class="ai-badge"><div class="ai-badge-dot dot-purple"></div>Vector DB Loaded</div>'
            '<div class="ai-badge"><div class="ai-badge-dot dot-teal"></div>Official AMC Sources</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        # Navigation buttons
        nav_items = [
            ("💬", "AI Conversation", "chat"),
            ("❓", "FAQ", "faq"),
            ("📈", "Fund Insights", "insights"),
            ("ℹ️", "About", "about"),
        ]
        for icon, label, key in nav_items:
            is_active = st.session_state.page == key
            btn_type = "primary" if is_active else "secondary"
            st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                on_click=set_page,
                args=(key,),
                use_container_width=True,
                type=btn_type
            )

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        if st.session_state.page == "chat":
            if st.button("🗑️  Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        st.markdown(
            '<div style="padding:16px 12px;margin-top:12px;">'
            '<div style="font-family:JetBrains Mono;font-size:0.6rem;color:#334155;'
            'text-transform:uppercase;letter-spacing:1px;text-align:center;">'
            'Powered by Groq · ChromaDB · LangChain</div></div>',
            unsafe_allow_html=True
        )

    # ── HEADER ──
    page_labels = {"chat": "AI Conversation", "faq": "FAQ", "insights": "Fund Insights", "about": "About"}
    cur_label = page_labels.get(st.session_state.page, "AI Conversation")
    st.markdown(
        f'<div class="top-header">'
        f'<div style="display:flex;align-items:center;">'
        f'<div class="header-brand">GROWW RAG AI Chatbot</div>'
        f'<span class="header-sep">|</span>'
        f'<div class="header-sub">{cur_label.upper()}</div>'
        f'</div>'
        f'<div class="status-pill"><span class="status-dot">●</span>Live · ICICI Prudential</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── PAGE ROUTER ──
    page = st.session_state.page
    if page == "chat":
        st.markdown('<div style="padding-top:24px;padding-bottom:100px;">', unsafe_allow_html=True)
        chat_page.render(AVATAR_B64)
        st.markdown('</div>', unsafe_allow_html=True)
    elif page == "faq":
        faq_page.render()
    elif page == "insights":
        insights_page.render()
    elif page == "about":
        about_page.render(AVATAR_B64)


if __name__ == "__main__":
    main()
