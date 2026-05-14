"""
Chat Page — AI Conversation with RAG pipeline.
"""
import streamlit as st
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%I:%M %p")


def render_user(content, ts, avatar_b64):
    st.markdown(
        f'<div class="user-row">'
        f'<div style="text-align:right;">'
        f'<div class="user-bubble">{content}</div>'
        f'<div class="msg-time">{ts}</div>'
        f'</div>'
        f'<div class="user-avatar-pill">👤</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_assistant(content, avatar_b64, sources=None, ts=None):
    ts = ts or ""
    if avatar_b64:
        av = f'<div class="ai-row-avatar" style="background-image:url(data:image/png;base64,{avatar_b64})"></div>'
    else:
        av = '<div class="ai-row-avatar-fallback">🤖</div>'

    src_html = ""
    if sources:
        cards = ""
        for i, s in enumerate(sources):
            name = s.replace("_", " ").replace(".txt", "").title()
            cards += (
                f'<div class="src-card">'
                f'<div class="src-label">Source {i+1}</div>'
                f'<div class="src-name">{name}</div>'
                f'<div class="src-desc">Official ICICI Prudential AMC data.</div>'
                f'</div>'
            )
        src_html = f'<div class="src-grid">{cards}</div>'

    st.markdown(
        f'<div class="ai-row">'
        f'{av}'
        f'<div style="flex:1;">'
        f'<div class="ai-bubble">{content}</div>'
        f'<div class="ai-meta">'
        f'<div class="ai-pill">RAG Retrieved</div>'
        f'<div class="ai-pill">Official Source</div>'
        f'<span class="ai-time">{ts}</span>'
        f'</div>'
        f'{src_html}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render(avatar_b64):
    from src.phase2_rag.guardrail import QueryGuardrail

    # Welcome message
    if not st.session_state.messages:
        render_assistant(
            "Hello! I'm GROWW AI, your personal mutual fund intelligence assistant. "
            "I'm connected to official ICICI Prudential fund data and ready to answer "
            "factual questions about expense ratios, exit loads, NAVs, and more. "
            "How can I help you today?",
            avatar_b64,
            ts=get_timestamp()
        )

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user(msg["content"], msg.get("ts", ""), avatar_b64)
        else:
            render_assistant(
                msg["content"], avatar_b64,
                sources=msg.get("sources"), ts=msg.get("ts", "")
            )

    # Typing indicator
    if st.session_state.thinking:
        if avatar_b64:
            av = f'<div class="ai-row-avatar" style="background-image:url(data:image/png;base64,{avatar_b64})"></div>'
        else:
            av = '<div class="ai-row-avatar-fallback">🤖</div>'
        st.markdown(
            f'<div class="typing-row">'
            f'{av}'
            f'<div class="typing-bubble">'
            f'<div class="typing-dots">'
            f'<div class="typing-dot" style="animation:pulse 1s infinite"></div>'
            f'<div class="typing-dot" style="animation:pulse 1s infinite 0.15s"></div>'
            f'<div class="typing-dot" style="animation:pulse 1s infinite 0.3s"></div>'
            f'</div></div></div>',
            unsafe_allow_html=True
        )

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
                    ans = "I couldn't find relevant information. Please try rephrasing."
                    sources = []
                else:
                    raw = st.session_state.groq_client.generate_answer(last_q, docs)
                    ans = raw.split("Source:")[0].strip()
                    sources = list(set(
                        [d.metadata.get("source", "doc").split("/")[-1] for d in docs]
                    ))[:2]
            st.session_state.messages.append({
                "role": "assistant", "content": ans,
                "sources": sources, "ts": ts
            })
        except Exception:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Temporary issue. Please try again.",
                "sources": [], "ts": ts
            })
        st.session_state.thinking = False
        st.rerun()
