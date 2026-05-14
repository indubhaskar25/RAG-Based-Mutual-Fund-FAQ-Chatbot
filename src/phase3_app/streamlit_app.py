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
from src.phase3_app.views import chat_page, faq_page, insights_page, about_page

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

# ── Global CSS ──
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
.stApp {{ background:#0a0b0f !important; font-family:'Inter',sans-serif; color:#e2e8f0; }}
[data-testid="stHeader"] {{ display:none !important; }}
[data-testid="stSidebarNav"] {{ display:none !important; }}
[data-testid="stSidebarNavItems"] {{ display:none !important; }}
ul[data-testid="stSidebarNavItems"] {{ display:none !important; }}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{ display:none !important; max-height:0 !important; overflow:hidden !important; }}
[data-testid="stSidebar"] {{ background:#0c0d12 !important; border-right:1px solid rgba(139,92,246,0.08); }}
[data-testid="stSidebar"] > div:first-child {{ padding-top:0 !important; }}
.block-container {{ padding:0 !important; max-width:100% !important; }}

/* ── Sidebar Branding ── */
.sb-brand {{ padding:28px 20px 14px; }}
.sb-brand-title {{ font-size:1.2rem; font-weight:800; background:linear-gradient(135deg,#8b5cf6,#06b6d4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:0.3px; }}
.sb-brand-sub {{ font-family:'JetBrains Mono'; font-size:0.58rem; color:#475569; text-transform:uppercase; letter-spacing:1.5px; margin-top:3px; }}
.sb-divider {{ height:1px; background:rgba(255,255,255,0.04); margin:10px 16px; }}

/* ── AI Status Card ── */
.ai-card {{ margin:12px 10px; padding:14px 16px; background:linear-gradient(135deg,rgba(139,92,246,0.05),rgba(6,182,212,0.03)); border:1px solid rgba(139,92,246,0.12); border-radius:12px; }}
.ai-card-row {{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }}
.ai-card-icon {{ width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,#8b5cf6,#06b6d4); display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0; }}
.ai-card-name {{ font-size:0.85rem; font-weight:700; color:#e2e8f0; }}
.ai-card-role {{ font-size:0.65rem; color:#64748b; font-family:'JetBrains Mono'; }}
.ai-badge {{ display:flex; align-items:center; gap:6px; padding:5px 10px; border-radius:6px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04); font-size:0.68rem; color:#64748b; margin-bottom:4px; }}
.ai-badge-dot {{ width:6px; height:6px; border-radius:50%; flex-shrink:0; }}
.dot-green {{ background:#22c55e; box-shadow:0 0 4px rgba(34,197,94,0.4); }}
.dot-purple {{ background:#8b5cf6; box-shadow:0 0 4px rgba(139,92,246,0.4); }}
.dot-teal {{ background:#06b6d4; box-shadow:0 0 4px rgba(6,182,212,0.4); }}

/* ── Top Header ── */
.top-header {{ display:flex; justify-content:space-between; align-items:center; padding:14px 32px; border-bottom:1px solid rgba(255,255,255,0.04); background:rgba(10,11,15,0.96); position:sticky; top:0; z-index:100; backdrop-filter:blur(12px); }}
.header-brand {{ font-size:1.05rem; font-weight:700; background:linear-gradient(135deg,#8b5cf6,#06b6d4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.header-sep {{ color:rgba(255,255,255,0.08); font-size:1rem; margin:0 12px; }}
.header-sub {{ font-family:'JetBrains Mono'; font-size:0.62rem; color:#475569; letter-spacing:1.5px; }}
.status-pill {{ background:rgba(34,197,94,0.06); border:1px solid rgba(34,197,94,0.15); padding:4px 12px; border-radius:16px; font-size:0.65rem; font-family:'JetBrains Mono'; color:#94a3b8; }}
.status-dot {{ color:#22c55e; margin-right:4px; }}

/* ── Chat Layout ── */
.chat-wrap {{ max-width:720px; margin:0 auto; padding:28px 16px 120px; }}

/* ── User Bubble ── */
.user-row {{ display:flex; justify-content:flex-end; gap:10px; margin-bottom:22px; }}
.user-bubble {{ background:linear-gradient(135deg,rgba(139,92,246,0.18),rgba(99,102,241,0.12)); border:1px solid rgba(139,92,246,0.2); border-radius:16px 16px 4px 16px; padding:12px 18px; font-size:0.92rem; line-height:1.65; color:#e2e8f0; max-width:45%; box-shadow:0 2px 12px rgba(139,92,246,0.08); }}
.user-time {{ font-family:'JetBrains Mono'; font-size:0.55rem; color:#475569; margin-top:4px; text-align:right; }}

/* ── AI Bubble ── */
.ai-row {{ display:flex; align-items:flex-start; gap:10px; margin-bottom:22px; }}
.ai-avatar {{ width:32px; height:32px; border-radius:8px; background:linear-gradient(135deg,#8b5cf6,#06b6d4); display:flex; align-items:center; justify-content:center; font-size:0.85rem; flex-shrink:0; margin-top:2px; }}
.ai-bubble {{ background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:4px 16px 16px 16px; padding:14px 18px; font-size:0.92rem; line-height:1.75; color:#cbd5e1; max-width:70%; backdrop-filter:blur(4px); }}
.ai-meta {{ display:flex; gap:6px; margin-top:6px; align-items:center; flex-wrap:wrap; }}
.ai-pill {{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:2px 8px; border-radius:4px; font-family:'JetBrains Mono'; font-size:0.55rem; color:#475569; text-transform:uppercase; }}
.ai-time {{ font-family:'JetBrains Mono'; font-size:0.55rem; color:#475569; }}

/* ── Source Cards ── */
.src-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:10px; max-width:70%; }}
.src-card {{ background:rgba(255,255,255,0.015); border:1px solid rgba(255,255,255,0.04); border-radius:8px; padding:10px 12px; cursor:pointer; transition:all 0.2s ease; text-decoration:none; display:block; }}
.src-card:hover {{ border-color:rgba(139,92,246,0.25); background:rgba(139,92,246,0.04); transform:translateY(-1px); }}
.src-label {{ font-family:'JetBrains Mono'; font-size:0.52rem; color:#475569; margin-bottom:3px; text-transform:uppercase; }}
.src-name {{ font-size:0.78rem; font-weight:600; color:#a78bfa; }}
.src-link {{ font-size:0.6rem; color:#475569; margin-top:4px; font-family:'JetBrains Mono'; }}

/* ── Loading Animation ── */
.loading-row {{ display:flex; align-items:flex-start; gap:10px; margin-bottom:22px; }}
.loading-bubble {{ background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:4px 16px 16px 16px; padding:12px 18px; max-width:70%; }}
.loading-text {{ font-size:0.78rem; color:#64748b; font-family:'JetBrains Mono'; margin-bottom:6px; }}
.loading-dots {{ display:flex; gap:4px; }}
.loading-dot {{ width:6px; height:6px; border-radius:50%; background:#8b5cf6; animation:ldpulse 1.2s infinite; }}
.loading-dot:nth-child(2) {{ animation-delay:0.2s; }}
.loading-dot:nth-child(3) {{ animation-delay:0.4s; }}
@keyframes ldpulse {{ 0%,80%,100% {{ opacity:0.2; transform:scale(0.8); }} 40% {{ opacity:1; transform:scale(1); }} }}

/* ── Chat Input ── */
[data-testid="stChatInput"] {{ border:none !important; background:transparent !important; }}
[data-testid="stChatInput"] > div {{ background:rgba(255,255,255,0.03) !important; border:1px solid rgba(139,92,246,0.15) !important; border-radius:14px !important; box-shadow:0 4px 20px rgba(0,0,0,0.25) !important; }}
[data-testid="stChatInput"] textarea {{ color:#e2e8f0 !important; font-size:0.9rem !important; }}
[data-testid="stChatInput"] textarea::placeholder {{ color:#475569 !important; }}
[data-testid="stChatInput"] button {{ border-radius:10px !important; }}

/* ── Expanders ── */
.streamlit-expanderHeader {{ background:rgba(255,255,255,0.02) !important; border:1px solid rgba(255,255,255,0.05) !important; border-radius:10px !important; color:#e2e8f0 !important; font-size:0.88rem !important; }}

/* ── Responsive ── */
@media (max-width:768px) {{
    .chat-wrap {{ padding:16px 10px 100px; }}
    .user-bubble {{ max-width:75%; }}
    .ai-bubble {{ max-width:90%; }}
    .src-grid {{ grid-template-columns:1fr; max-width:90%; }}
    .top-header {{ padding:12px 16px; }}
    .header-brand {{ font-size:0.9rem; }}
}}
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

        # AI Status Card
        st.markdown(
            '<div class="ai-card">'
            '<div class="ai-card-row">'
            '<div class="ai-card-icon">🤖</div>'
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
        nav = [("💬", "AI Conversation", "chat"), ("❓", "FAQ", "faq"),
               ("📊", "Fund Insights", "insights"), ("ℹ️", "About", "about")]
        for icon, label, key in nav:
            active = st.session_state.page == key
            st.button(
                f"{icon}  {label}", key=f"nav_{key}",
                on_click=set_page, args=(key,),
                use_container_width=True,
                type="primary" if active else "secondary"
            )

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        if st.session_state.page == "chat":
            if st.button("🗑️  Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        st.markdown(
            '<div style="padding:14px 10px;margin-top:8px;">'
            '<div style="font-family:JetBrains Mono;font-size:0.55rem;color:#334155;'
            'text-transform:uppercase;letter-spacing:1px;text-align:center;">'
            'Groq · ChromaDB · LangChain</div></div>',
            unsafe_allow_html=True
        )

    # ── HEADER ──
    labels = {"chat": "AI Conversation", "faq": "FAQ", "insights": "Fund Insights", "about": "About"}
    st.markdown(
        f'<div class="top-header">'
        f'<div style="display:flex;align-items:center;">'
        f'<div class="header-brand">GROWW RAG AI Chatbot</div>'
        f'<span class="header-sep">|</span>'
        f'<div class="header-sub">{labels.get(st.session_state.page, "").upper()}</div>'
        f'</div>'
        f'<div class="status-pill"><span class="status-dot">●</span> Live · ICICI Prudential</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── PAGE ROUTER ──
    page = st.session_state.page
    if page == "chat":
        chat_page.render(AVATAR_B64)
    elif page == "faq":
        faq_page.render()
    elif page == "insights":
        insights_page.render()
    elif page == "about":
        about_page.render(AVATAR_B64)


if __name__ == "__main__":
    main()
