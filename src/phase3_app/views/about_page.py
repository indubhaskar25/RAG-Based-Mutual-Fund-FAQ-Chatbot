"""
About Page — Architecture overview and compliance.
"""
import streamlit as st


def render(avatar_b64):
    st.markdown(
        '<div style="max-width:780px;margin:0 auto;padding:28px 20px;">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:1.4rem;font-weight:700;color:#e2e8f0;margin-bottom:2px;">'
        'ℹ️ About GROWW RAG AI</div>'
        '<div style="color:#64748b;font-size:0.82rem;margin-bottom:24px;">'
        'A Retrieval-Augmented Generation chatbot for factual mutual fund information.</div>',
        unsafe_allow_html=True
    )

    sections = [
        ("🧠", "RAG Architecture",
         "Your query is embedded into a vector, matched against a knowledge base of official "
         "mutual fund documents, and the most relevant chunks are sent to an LLM with a strict "
         "system prompt to generate a factual, sourced response."),
        ("⚡", "Groq LLM Inference",
         "We use Groq's ultra-fast inference API with Llama 3.1 8B Instant. Temperature is set "
         "to 0.0 for deterministic output with a max of 200 tokens. Responses are limited to "
         "3 sentences with exactly one official source citation."),
        ("🗄️", "ChromaDB Vector Store",
         "Documents are stored as vector embeddings in a persistent ChromaDB instance. Embeddings "
         "are generated using FastEmbed (BAAI/bge-small-en-v1.5) on ONNX Runtime — no GPU required. "
         "Top-5 most similar chunks are retrieved per query."),
        ("📡", "Official Data Pipeline",
         "Data is scraped from official Groww.in pages for 19 ICICI Prudential schemes, plus the "
         "fund house overview, 3 educational pages, and 1 category page — totalling 24 sources. "
         "A GitHub Actions workflow refreshes this data daily."),
        ("🛡️", "Facts-Only Compliance",
         "A query safety guardrail intercepts advisory questions before they reach the retrieval "
         "or LLM pipeline. These are blocked with a polite refusal and a link to SEBI's investor "
         "education portal. The LLM system prompt enforces facts-only constraints."),
    ]

    for icon, title, desc in sections:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
            f'border-radius:12px;padding:16px 18px;margin-bottom:10px;">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
            f'<span style="font-size:1rem;">{icon}</span>'
            f'<span style="font-size:0.92rem;font-weight:700;color:#e2e8f0;">{title}</span>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.82rem;line-height:1.7;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Tech stack
    st.markdown(
        '<div style="margin-top:20px;font-size:0.68rem;font-family:JetBrains Mono;color:#8b5cf6;'
        'text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Tech Stack</div>',
        unsafe_allow_html=True
    )

    techs = [
        ("Streamlit", "UI & Deploy"), ("Groq API", "LLM"), ("ChromaDB", "Vector DB"),
        ("FastEmbed", "Embeddings"), ("LangChain", "RAG"), ("GitHub Actions", "CI/CD"),
    ]
    cols = st.columns(3)
    for i, (name, role) in enumerate(techs):
        with cols[i % 3]:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                f'border-radius:8px;padding:12px;text-align:center;margin-bottom:8px;">'
                f'<div style="font-size:0.85rem;font-weight:600;color:#a78bfa;">{name}</div>'
                f'<div style="font-size:0.65rem;color:#64748b;margin-top:2px;">{role}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
