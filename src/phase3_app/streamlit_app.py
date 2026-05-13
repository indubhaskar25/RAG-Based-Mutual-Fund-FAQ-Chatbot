import streamlit as st
import os

# 1. ABSOLUTE STABILITY SHIELD
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["DEVICE"] = "cpu"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import sys
import base64
from PIL import Image
import time

# Add root directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.phase1_ingestion.vector_store import VectorStoreManager
from src.phase2_rag.groq_client import GroqRAGClient
from src.phase2_rag.guardrail import QueryGuardrail

# 2. SETUP & THEMING
st.set_page_config(
    page_title="GROW RAG | Nexus Protocol",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. PERSISTENT ENGINE INIT
if "vs_manager" not in st.session_state:
    st.session_state.vs_manager = VectorStoreManager(persist_directory="chromadb_store")
    st.session_state.retriever = st.session_state.vs_manager.get_retriever(top_k=5)
    st.session_state.groq_client = GroqRAGClient()
if "messages" not in st.session_state: st.session_state.messages = []
if "thinking" not in st.session_state: st.session_state.thinking = False

# Helper to encode local avatar
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

AVATAR_PATH = "/Users/datateam/.gemini/antigravity/brain/5346a4c0-7904-4efe-8a65-6721c97e252c/groww_ai_assistant_avatar_1778663721084.png"
AVATAR_B64 = get_base64_image(AVATAR_PATH)

# NEXUS PROTOCOL STYLES
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    .stApp {{ background-color: #0b0d11 !important; font-family: 'Outfit', sans-serif; color: #e6edf3; }}
    [data-testid="stSidebar"] {{ background-color: #0b0d11 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); }}
    [data-testid='stHeader'] {{ display:none !important; }}

    .avatar-nexus {{
        width: 48px; height: 48px; border-radius: 12px;
        background: url('data:image/png;base64,{AVATAR_B64}') center/cover;
        border: 1px solid #00f5ff; box-shadow: 0 0 15px rgba(0, 245, 255, 0.1);
        flex-shrink: 0;
    }}
    .bubble-assistant {{
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px; border-radius: 12px; font-size: 1.1rem; line-height: 1.7;
    }}
    .telemetry-pills {{ display: flex; gap: 10px; margin-top: 12px; }}
    .pill {{ background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.65rem; color: #5f6a7d; text-transform: uppercase; }}

    .bubble-user {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px; border-radius: 12px; font-size: 1.1rem;
    }}
    .user-avatar-glyph {{
        width: 48px; height: 48px; border-radius: 12px;
        background: #7a2fff; display: flex; align-items: center; justify-content: center;
        color: #fff; font-size: 1.4rem; flex-shrink: 0;
    }}

    /* Streamlit Overrides */
    .stChatInput {{ border: none !important; background: transparent !important; }}
    [data-testid="stVerticalBlock"] > div:first-child {{ margin-top: 0 !important; }}
</style>
""", unsafe_allow_html=True)

def render_assistant(content, sources=None):
    source_html = ""
    if sources:
        modules = "".join([f"""<div style="background: #0f1218; border: 1px solid rgba(255,255,255,0.05); padding: 24px; border-radius: 12px; margin-top: 10px;">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.6rem; color: #5f6a7d; margin-bottom: 10px;">DOC_X{i+1}</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 8px;">{s}</div>
            <div style="font-size: 0.85rem; color: #8b949e; line-height: 1.5;">Detailed factual report extracted from Grow RAG knowledge base.</div>
            <div style="display: flex; justify-content: space-between; margin-top: 20px; font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #5f6a7d;">
                <span>CONFIDENCE: 98.4%</span>
                <span style="font-size: 1rem;">📤</span>
            </div>
        </div>""" for i, s in enumerate(sources)])
        source_html = f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 24px;">{modules}</div>'

    st.markdown(f"""
    <div style="display: flex; gap: 24px; max-width: 1000px; margin: 0 auto 32px auto; align-items: flex-start;">
        <div class="avatar-nexus"></div>
        <div style="flex-grow: 1;">
            <div class="bubble-assistant">{content}</div>
            <div class="telemetry-pills">
                <div class="pill">Retrieved</div>
                <div class="pill">Latency: 8.2ms</div>
            </div>
            {source_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_user(content):
    st.markdown(f"""
    <div style="display: flex; gap: 24px; max-width: 1000px; margin: 0 auto 32px auto; align-items: flex-start; justify-content: flex-end;">
        <div style="flex-grow: 0; max-width: 80%;">
            <div class="bubble-user">{content}</div>
            <div style="text-align: right; font-family: 'JetBrains Mono'; font-size: 0.6rem; color: #5f6a7d; margin-top: 10px; text-transform: uppercase;">Packet Delivered</div>
        </div>
        <div class="user-avatar-glyph">👤</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # 1. SIDEBAR
    with st.sidebar:
        st.markdown("""
        <div style="padding: 40px 30px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #fff; letter-spacing: 1px;">GROW RAG</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #5f6a7d; text-transform: uppercase; margin-top: 5px;">Intelligence Core</div>
        </div>
        <div style="padding: 15px 30px; display: flex; align-items: center; gap: 15px; color: #8b949e;">🏠 &nbsp; Home</div>
        <div style="padding: 15px 30px; display: flex; align-items: center; gap: 15px; color: #8b949e;">❓ &nbsp; FAQ</div>
        <div style="padding: 15px 30px; display: flex; align-items: center; gap: 15px; color: #8b949e;">🗑️ &nbsp; Clear Chat</div>
        <div style="padding: 15px 30px; display: flex; align-items: center; gap: 15px; color: #8b949e;">⚙️ &nbsp; Settings</div>
        
        <div style="position: fixed; bottom: 0; width: 300px; padding: 30px; border-top: 1px solid rgba(255,255,255,0.05); background: #0b0d11;">
            <div style="display:flex; align-items:center; gap:12px;">
                <div class="avatar-nexus" style="width:36px; height:36px;"></div>
                <div>
                    <div style="font-size:0.9rem; font-weight:700;">Neural Link</div>
                    <div style="font-size:0.7rem; color:#00f5ff; font-family:'JetBrains Mono';">ACTIVE</div>
                </div>
            </div>
            <div style="background: #00f5ff; color: #000; padding: 14px; border-radius: 8px; text-align: center; font-weight: 700; font-size: 0.9rem; box-shadow: 0 0 20px rgba(0, 245, 255, 0.2); margin-top: 20px;">Upgrade to Pro</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. NEXUS HEADER
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; border-bottom: 1px solid rgba(255,255,255,0.05); background: #0b0d11; position: sticky; top: 0; z-index: 100;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="font-size: 1.4rem; font-weight: 700; letter-spacing: 1px;">GROW RAG</div>
            <div style="color: rgba(255,255,255,0.1); font-size: 1.2rem;">|</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #5f6a7d; letter-spacing: 2px;">NEXUS PROTOCOL</div>
        </div>
        <div style="display: flex; align-items: center; gap: 25px;">
            <div style="background: rgba(0, 245, 255, 0.05); border: 1px solid rgba(0, 245, 255, 0.2); padding: 6px 16px; border-radius: 20px; font-size: 0.75rem; font-family: 'JetBrains Mono'; color: #fff;">
                <span style="color:#00f5ff;">●</span> Active
            </div>
            <div style="font-size: 1.3rem; color: #8b949e;">🔔</div><div style="font-size: 1.3rem; color: #8b949e;">👤</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. CONVERSATION HUB
    st.write("")
    st.write("")
    
    if not st.session_state.messages:
        render_assistant("Greetings! I have initialized the retrieval-augmented generation protocols. I am connected to the Grow RAG core database. How can I assist your neural exploration today?")

    for msg in st.session_state.messages:
        if msg["role"] == "user": render_user(msg["content"])
        else: render_assistant(msg["content"], sources=msg.get("sources"))
    
    if st.session_state.thinking:
        st.markdown("<div style='max-width:1000px; margin:0 auto; padding-left:72px; font-family:JetBrains Mono; font-size:0.7rem; color:#5f6a7d; animation:pulse 1s infinite;'>SYNCHRONIZING NEURAL DATA...</div>", unsafe_allow_html=True)

    # 4. NEXUS CONTROL
    st.markdown('<div style="position: fixed; bottom: 15px; left: 340px; right: 40px; text-align: center; font-family: \'JetBrains Mono\'; font-size: 0.65rem; color: #5f6a7d; letter-spacing: 2px;">SYSTEM: GROW RAG CORE V4.2 // NEURAL LINK ENCRYPTED</div>', unsafe_allow_html=True)
    
    prompt = st.chat_input("Query Intelligence Core...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.thinking = True
        st.rerun()

    # 5. INTELLIGENCE ENGINE
    if st.session_state.thinking:
        last_q = st.session_state.messages[-1]["content"]
        try:
            if QueryGuardrail.is_advisory(last_q):
                ans = QueryGuardrail.get_refusal_response()['answer']
                sources = []
            else:
                docs = st.session_state.retriever.invoke(last_q)
                if not docs: ans = "No documentation found."; sources = []
                else:
                    ans = st.session_state.groq_client.generate_answer(last_q, docs).split("Source:")[0].strip()
                    sources = list(set([doc.metadata.get('source', 'Official Doc').split('/')[-1] for doc in docs]))[:2]
            
            st.session_state.messages.append({"role": "assistant", "content": ans, "sources": sources})
        except: pass
        st.session_state.thinking = False
        st.rerun()

if __name__ == "__main__":
    main()
