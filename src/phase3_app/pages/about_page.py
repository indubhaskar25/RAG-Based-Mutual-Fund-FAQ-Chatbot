"""
About Page — Architecture overview and compliance information.
"""
import streamlit as st


def render(avatar_b64):
    st.markdown(
        '<div style="max-width:850px;margin:0 auto;padding:32px 24px;">',
        unsafe_allow_html=True
    )

    # Title
    st.markdown(
        '<h2 style="font-size:1.6rem;font-weight:800;'
        'background:linear-gradient(135deg,#8b5cf6,#06b6d4);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'margin-bottom:4px;">About GROWW RAG AI</h2>'
        '<p style="color:#64748b;font-size:0.9rem;margin-bottom:28px;">'
        'A Retrieval-Augmented Generation chatbot built for factual mutual fund information.</p>',
        unsafe_allow_html=True
    )

    # Avatar card
    if avatar_b64:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:18px;padding:24px;'
            f'background:linear-gradient(135deg,rgba(139,92,246,0.07),rgba(6,182,212,0.05));'
            f'border:1px solid rgba(139,92,246,0.2);border-radius:16px;margin-bottom:28px;">'
            f'<div style="width:64px;height:64px;border-radius:14px;'
            f'background:url(data:image/png;base64,{avatar_b64}) center/cover;'
            f'border:2px solid rgba(139,92,246,0.4);flex-shrink:0;"></div>'
            f'<div>'
            f'<div style="font-size:1.1rem;font-weight:700;color:#e2e8f0;">GROWW AI Assistant</div>'
            f'<div style="font-size:0.82rem;color:#94a3b8;line-height:1.6;margin-top:4px;">'
            f'I provide factual, sourced answers about ICICI Prudential Mutual Fund schemes. '
            f'I do not give investment advice or recommendations.</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    # Architecture section
    sections = [
        (
            "🧠", "RAG Architecture",
            "This chatbot uses Retrieval-Augmented Generation (RAG) to answer questions. "
            "Your query is first embedded into a vector, matched against a knowledge base of "
            "official mutual fund documents, and the most relevant chunks are sent to an LLM "
            "along with a strict system prompt to generate a factual, sourced response."
        ),
        (
            "⚡", "Groq LLM Inference",
            "We use Groq's ultra-fast inference API with the Llama 3.1 8B Instant model. "
            "Temperature is set to 0.0 for deterministic, facts-only output with a max of "
            "200 tokens to enforce conciseness. Responses are limited to 3 sentences with "
            "exactly one official source citation."
        ),
        (
            "🗄️", "ChromaDB Vector Store",
            "All documents are stored as vector embeddings in a persistent ChromaDB instance. "
            "Embeddings are generated using FastEmbed (BAAI/bge-small-en-v1.5) which runs on "
            "ONNX Runtime — no GPU or PyTorch required. The top-5 most similar chunks are "
            "retrieved for each query."
        ),
        (
            "📡", "Official Data Pipeline",
            "Data is scraped from official Groww.in pages for 19 ICICI Prudential schemes, "
            "plus the fund house overview, 3 educational pages, and 1 category page — "
            "totalling 24 authoritative sources. A GitHub Actions workflow refreshes this "
            "data daily at 00:00 UTC."
        ),
        (
            "🛡️", "Facts-Only Compliance",
            "A query safety guardrail intercepts advisory questions (e.g., 'Should I invest?', "
            "'Best fund?') BEFORE they reach the retrieval or LLM pipeline. These are blocked "
            "with a polite refusal and a link to SEBI's investor education portal. The LLM "
            "system prompt provides defense-in-depth by enforcing facts-only constraints."
        ),
    ]

    for icon, title, desc in sections:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);'
            f'border-radius:14px;padding:20px 22px;margin-bottom:14px;">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">'
            f'<span style="font-size:1.2rem;">{icon}</span>'
            f'<span style="font-size:1rem;font-weight:700;color:#e2e8f0;">{title}</span>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.88rem;line-height:1.7;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Tech stack
    st.markdown(
        '<div style="margin-top:24px;font-size:0.75rem;font-family:JetBrains Mono;'
        'color:#8b5cf6;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">'
        'Tech Stack</div>',
        unsafe_allow_html=True
    )

    techs = [
        ("Streamlit", "Frontend & Deployment"),
        ("Groq API", "LLM Inference"),
        ("ChromaDB", "Vector Database"),
        ("FastEmbed", "Embeddings (ONNX)"),
        ("LangChain", "RAG Orchestration"),
        ("GitHub Actions", "Automated Data Refresh"),
    ]

    cols = st.columns(3)
    for i, (name, role) in enumerate(techs):
        with cols[i % 3]:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);'
                f'border-radius:10px;padding:14px;text-align:center;margin-bottom:10px;">'
                f'<div style="font-size:0.9rem;font-weight:700;color:#c4b5fd;">{name}</div>'
                f'<div style="font-size:0.72rem;color:#64748b;margin-top:3px;">{role}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
