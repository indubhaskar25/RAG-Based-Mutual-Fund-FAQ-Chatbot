"""
Fund Insights Page — Dashboard-style analytics.
"""
import streamlit as st
import os
import pandas as pd
from datetime import datetime

FUNDS = [
    {"name": "Silver ETF FoF", "cat": "Commodity", "risk": "High"},
    {"name": "Large Cap Fund", "cat": "Large Cap", "risk": "Moderate"},
    {"name": "Dynamic Plan", "cat": "Dynamic Asset", "risk": "Moderate"},
    {"name": "Top 100 Fund", "cat": "Large Cap", "risk": "Moderate"},
    {"name": "Infrastructure Fund", "cat": "Sectoral", "risk": "High"},
    {"name": "Commodities Fund", "cat": "Commodity", "risk": "High"},
    {"name": "Balanced Fund", "cat": "Hybrid", "risk": "Moderate"},
    {"name": "FlexiCap Fund", "cat": "FlexiCap", "risk": "High"},
    {"name": "Retirement Pure Equity", "cat": "Retirement", "risk": "High"},
    {"name": "Short Term Plan", "cat": "Debt", "risk": "Low"},
    {"name": "Liquid Fund", "cat": "Liquid", "risk": "Low"},
    {"name": "Indo Asia Equity Fund", "cat": "International", "risk": "Very High"},
    {"name": "Nifty Index Fund", "cat": "Index", "risk": "Moderate"},
    {"name": "MultiCap Fund", "cat": "MultiCap", "risk": "High"},
    {"name": "Corporate Bond Fund", "cat": "Debt", "risk": "Low"},
    {"name": "Nifty Midcap 150 Index", "cat": "Index", "risk": "High"},
    {"name": "Dividend Yield Equity", "cat": "Dividend Yield", "risk": "High"},
    {"name": "Aggressive Hybrid FoF", "cat": "Hybrid", "risk": "High"},
    {"name": "Business Cycle Fund", "cat": "Thematic", "risk": "Very High"},
]

RISK_CLR = {"Low": "#22c55e", "Moderate": "#eab308", "High": "#f97316", "Very High": "#ef4444"}


def _card(icon, value, label):
    return (
        f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
        f'border-radius:12px;padding:18px;text-align:center;">'
        f'<div style="font-size:1.3rem;margin-bottom:4px;">{icon}</div>'
        f'<div style="font-size:1.3rem;font-weight:800;color:#e2e8f0;">{value}</div>'
        f'<div style="font-size:0.62rem;color:#64748b;margin-top:3px;font-family:JetBrains Mono;'
        f'text-transform:uppercase;letter-spacing:1px;">{label}</div></div>'
    )


def render():
    st.markdown(
        '<div style="max-width:900px;margin:0 auto;padding:28px 20px;">'
        '<div style="font-size:1.4rem;font-weight:700;color:#e2e8f0;margin-bottom:2px;">'
        '📊 Fund Insights</div>'
        '<div style="color:#64748b;font-size:0.82rem;margin-bottom:24px;">'
        'Knowledge base statistics and indexed scheme overview.</div>',
        unsafe_allow_html=True
    )

    doc_count = 0
    if os.path.exists("data/raw_scraped"):
        doc_count = len([f for f in os.listdir("data/raw_scraped") if f.endswith(".txt")])

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_card("📊", str(len(FUNDS)), "Schemes"), unsafe_allow_html=True)
    with c2:
        st.markdown(_card("📄", str(doc_count), "Documents"), unsafe_allow_html=True)
    with c3:
        st.markdown(_card("🏷️", str(len(set(f["cat"] for f in FUNDS))), "Categories"), unsafe_allow_html=True)
    with c4:
        st.markdown(_card("🕐", datetime.now().strftime("%b %d"), "Last Sync"), unsafe_allow_html=True)

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # Risk distribution
    st.markdown(
        '<div style="font-size:0.68rem;font-family:JetBrains Mono;color:#8b5cf6;'
        'text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Risk Distribution</div>',
        unsafe_allow_html=True
    )
    risk_counts = {}
    for f in FUNDS:
        risk_counts[f["risk"]] = risk_counts.get(f["risk"], 0) + 1

    order = ["Low", "Moderate", "High", "Very High"]
    cols = st.columns(len(risk_counts))
    for idx, risk in enumerate(order):
        if risk not in risk_counts:
            continue
        count = risk_counts[risk]
        color = RISK_CLR.get(risk, "#8b5cf6")
        pct = int(count / len(FUNDS) * 100)
        with cols[idx]:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                f'border-radius:10px;padding:14px;text-align:center;">'
                f'<div style="font-size:1.2rem;font-weight:800;color:{color};">{count}</div>'
                f'<div style="font-size:0.72rem;color:#94a3b8;margin-top:2px;">{risk}</div>'
                f'<div style="height:3px;background:rgba(255,255,255,0.04);border-radius:2px;margin-top:8px;">'
                f'<div style="height:3px;width:{pct}%;background:{color};border-radius:2px;"></div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # Category chart
    st.markdown(
        '<div style="font-size:0.68rem;font-family:JetBrains Mono;color:#8b5cf6;'
        'text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Category Breakdown</div>',
        unsafe_allow_html=True
    )
    cat_counts = {}
    for f in FUNDS:
        cat_counts[f["cat"]] = cat_counts.get(f["cat"], 0) + 1
    df = pd.DataFrame(list(cat_counts.items()), columns=["Category", "Count"])
    st.bar_chart(df.set_index("Category"), color="#8b5cf6")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # Scheme cards
    st.markdown(
        '<div style="font-size:0.68rem;font-family:JetBrains Mono;color:#8b5cf6;'
        'text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Indexed Schemes</div>',
        unsafe_allow_html=True
    )
    cols = st.columns(3)
    for i, fund in enumerate(FUNDS):
        color = RISK_CLR.get(fund["risk"], "#8b5cf6")
        with cols[i % 3]:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);'
                f'border-radius:10px;padding:12px 14px;margin-bottom:8px;">'
                f'<div style="font-size:0.85rem;font-weight:600;color:#e2e8f0;margin-bottom:5px;">'
                f'ICICI Pru {fund["name"]}</div>'
                f'<div style="display:flex;gap:5px;flex-wrap:wrap;">'
                f'<span style="background:rgba(139,92,246,0.1);color:#a78bfa;padding:2px 7px;'
                f'border-radius:4px;font-size:0.62rem;">{fund["cat"]}</span>'
                f'<span style="color:{color};font-size:0.62rem;padding:2px 7px;'
                f'border-radius:4px;background:rgba(255,255,255,0.03);">'
                f'{fund["risk"]}</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
