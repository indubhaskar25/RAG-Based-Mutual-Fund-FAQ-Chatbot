"""
Chat Page — AI Conversation with RAG pipeline.
"""
import streamlit as st
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%I:%M %p")


def render_user(content, ts):
    st.markdown(
        f'<div class="chat-wrap" style="padding:0;">'
        f'<div class="user-row">'
        f'<div>'
        f'<div class="user-bubble">{content}</div>'
        f'<div class="user-time">{ts}</div>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_assistant(content, sources=None, ts=None):
    ts = ts or ""
    src_html = ""
    if sources:
        cards = ""
        for i, s in enumerate(sources):
            if isinstance(s, dict):
                name = str(s.get("name", "Unknown")).replace("_", " ").replace(".txt", "").title()
                url = s.get("url") or f"https://groww.in/search?q={name.replace(' ', '+')}"
            else:
                name = str(s).replace("_", " ").replace(".txt", "").title()
                url = f"https://groww.in/search?q={name.replace(' ', '+')}"
                
            cards += (
                f'<a href="{url}" target="_blank" class="src-card">'
                f'<div class="src-label">Source {i+1}</div>'
                f'<div class="src-name">{name}</div>'
                f'<div class="src-link">Open Source ↗</div>'
                f'</a>'
            )
        src_html = f'<div class="src-grid">{cards}</div>'

    st.markdown(
        f'<div class="chat-wrap" style="padding:0;">'
        f'<div class="ai-row">'
        f'<div class="ai-avatar">🤖</div>'
        f'<div style="flex:1;">'
        f'<div class="ai-bubble">{content}</div>'
        f'<div class="ai-meta">'
        f'<div class="ai-pill">Retrieved</div>'
        f'<div class="ai-pill">Official Source</div>'
        f'<span class="ai-time">{ts}</span>'
        f'</div>'
        f'{src_html}'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_loading():
    st.markdown(
        '<div class="chat-wrap" style="padding:0;">'
        '<div class="loading-row">'
        '<div class="ai-avatar">🤖</div>'
        '<div class="loading-bubble">'
        '<div class="loading-text">Retrieving AMC documents...</div>'
        '<div class="loading-dots">'
        '<div class="loading-dot"></div>'
        '<div class="loading-dot"></div>'
        '<div class="loading-dot"></div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


def render(avatar_b64):
    from src.phase2_rag.guardrail import QueryGuardrail

    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

    # Welcome message
    if not st.session_state.messages:
        render_assistant(
            "Hello! I'm your GROWW AI mutual fund assistant. "
            "I can answer factual questions about ICICI Prudential fund schemes — "
            "expense ratios, exit loads, NAVs, and more. How can I help?",
            ts=get_timestamp()
        )

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user(msg["content"], msg.get("ts", ""))
        else:
            render_assistant(msg["content"], msg.get("sources"), msg.get("ts", ""))

    if st.session_state.thinking:
        render_loading()

    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    prompt = st.chat_input("Ask about mutual funds, expense ratios, exit loads...")
    if prompt:
        ts = get_timestamp()
        st.session_state.messages.append({"role": "user", "content": prompt, "ts": ts})
        st.session_state.thinking = True
        st.rerun()

    # RAG engine
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
                    ans = "I couldn't find relevant information. Please try rephrasing your question."
                    sources = []
                else:
                    raw = st.session_state.groq_client.generate_answer(last_q, docs)
                    ans = raw.split("Source:")[0].strip()
                    
                    src_map = {}
                    for d in docs:
                        s_url = d.metadata.get("source_url")
                        s_name = d.metadata.get("scheme_name") or d.metadata.get("source", "doc").split("/")[-1]
                        if s_name not in src_map:
                            src_map[s_name] = s_url
                            
                    sources = [{"name": n, "url": u} for n, u in src_map.items()][:2]
            st.session_state.messages.append({
                "role": "assistant", "content": ans,
                "sources": sources, "ts": ts
            })
        except Exception:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Temporary issue. Please try again in a moment.",
                "sources": [], "ts": ts
            })
        st.session_state.thinking = False
        st.rerun()
