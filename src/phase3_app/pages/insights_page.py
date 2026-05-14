"""
Fund Insights Page — Dashboard-style analytics section.
"""
import streamlit as st
import os


FUND_DATA = [
    {"name": "Silver ETF FoF", "category": "Commodity", "risk": "High", "type": "Open-Ended"},
    {"name": "Large Cap Fund", "category": "Large Cap", "risk": "Moderate", "type": "Open-Ended"},
    {"name": "Dynamic Plan", "category": "Dynamic Asset", "risk": "Moderate", "type": "Open-Ended"},
    {"name": "Top 100 Fund", "category": "Large Cap", "risk": "Moderate", "type": "Open-Ended"},
    {"name": "Infrastructure Fund", "category": "Sectoral", "risk": "High", "type": "Open-Ended"},
    {"name": "Commodities Fund", "category": "Commodity", "risk": "High", "type": "Open-Ended"},
    {"name": "Balanced Fund", "category": "Hybrid", "risk": "Moderate", "type": "Open-Ended"},
    {"name": "FlexiCap Fund", "category": "FlexiCap", "risk": "High", "type": "Open-Ended"},
    {"name": "Retirement Pure Equity", "category": "Retirement", "risk": "High", "type": "Open-Ended"},
    {"name": "Short Term Plan", "category": "Debt", "risk": "Low", "type": "Open-Ended"},
    {"name": "Liquid Fund", "category": "Liquid", "risk": "Low", "type": "Open-Ended"},
    {"name": "Indo Asia Equity Fund", "category": "International", "risk": "Very High", "type": "Open-Ended"},
    {"name": "Nifty Index Fund", "category": "Index", "risk": "Moderate", "type": "Open-Ended"},
    {"name": "MultiCap Fund", "category": "MultiCap", "risk": "High", "type": "Open-Ended"},
    {"name": "Corporate Bond Fund", "category": "Debt", "risk": "Low", "type": "Open-Ended"},
    {"name": "Nifty Midcap 150 Index", "category": "Index", "risk": "High", "type": "Open-Ended"},
    {"name": "Dividend Yield Equity", "category": "Dividend Yield", "risk": "High", "type": "Open-Ended"},
    {"name": "Aggressive Hybrid FoF", "category": "Hybrid", "risk": "High", "type": "Open-Ended"},
    {"name": "Business Cycle Fund", "category": "Thematic", "risk": "Very High", "type": "Open-Ended"},
]

RISK_COLORS = {
    "Low": "#22c55e",
    "Moderate": "#eab308",
    "High": "#f97316",
    "Very High": "#ef4444",
}


def render():
    st.markdown(
        '<div style="max-width:950px;margin:0 auto;padding:32px 24px;">'
        '<h2 style="font-size:1.6rem;font-weight:800;'
        'background:linear-gradient(135deg,#8b5cf6,#06b6d4);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'margin-bottom:4px;">Fund Insights</h2>'
        '<p style="color:#64748b;font-size:0.9rem;margin-bottom:28px;">'
        'Overview of indexed ICICI Prudential schemes and knowledge base statistics.</p>',
        unsafe_allow_html=True
    )

    # Count scraped docs
    doc_count = 0
    data_path = "data/raw_scraped"
    if os.path.exists(data_path):
        doc_count = len([f for f in os.listdir(data_path) if f.endswith(".txt")])

    # Metric cards
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "Indexed Schemes", str(len(FUND_DATA)), "📊"),
        (c2, "Data Sources", str(doc_count), "📄"),
        (c3, "Fund Categories", str(len(set(f["category"] for f in FUND_DATA))), "🏷️"),
        (c4, "AMC", "ICICI Prudential", "🏦"),
    ]
    for col, label, val, icon in metrics:
        with col:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);'
                f'border-radius:14px;padding:20px;text-align:center;">'
                f'<div style="font-size:1.5rem;margin-bottom:6px;">{icon}</div>'
                f'<div style="font-size:1.4rem;font-weight:800;color:#e2e8f0;">{val}</div>'
                f'<div style="font-size:0.72rem;color:#64748b;margin-top:4px;'
                f'font-family:JetBrains Mono;text-transform:uppercase;letter-spacing:1px;">{label}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)

    # Risk distribution chart
    st.markdown(
        '<div style="font-size:0.75rem;font-family:JetBrains Mono;color:#8b5cf6;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">Risk Distribution</div>',
        unsafe_allow_html=True
    )
    risk_counts = {}
    for f in FUND_DATA:
        risk_counts[f["risk"]] = risk_counts.get(f["risk"], 0) + 1

    chart_cols = st.columns(len(risk_counts))
    for idx, (risk, count) in enumerate(sorted(risk_counts.items(), key=lambda x: ["Low", "Moderate", "High", "Very High"].index(x[0]))):
        with chart_cols[idx]:
            color = RISK_COLORS.get(risk, "#8b5cf6")
            pct = int(count / len(FUND_DATA) * 100)
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);'
                f'border-radius:12px;padding:16px;text-align:center;">'
                f'<div style="font-size:1.3rem;font-weight:800;color:{color};">{count}</div>'
                f'<div style="font-size:0.78rem;color:#94a3b8;margin-top:2px;">{risk} Risk</div>'
                f'<div style="height:4px;background:rgba(255,255,255,0.05);border-radius:2px;margin-top:10px;">'
                f'<div style="height:4px;width:{pct}%;background:{color};border-radius:2px;"></div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)

    # Category pie chart
    st.markdown(
        '<div style="font-size:0.75rem;font-family:JetBrains Mono;color:#8b5cf6;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">Category Breakdown</div>',
        unsafe_allow_html=True
    )
    import pandas as pd
    cat_counts = {}
    for f in FUND_DATA:
        cat_counts[f["category"]] = cat_counts.get(f["category"], 0) + 1
    df = pd.DataFrame(list(cat_counts.items()), columns=["Category", "Count"])
    st.bar_chart(df.set_index("Category"), color="#8b5cf6")

    st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)

    # Scheme cards grid
    st.markdown(
        '<div style="font-size:0.75rem;font-family:JetBrains Mono;color:#8b5cf6;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">Indexed Schemes</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(3)
    for i, fund in enumerate(FUND_DATA):
        color = RISK_COLORS.get(fund["risk"], "#8b5cf6")
        with cols[i % 3]:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);'
                f'border-radius:12px;padding:16px;margin-bottom:12px;">'
                f'<div style="font-size:0.92rem;font-weight:700;color:#e2e8f0;margin-bottom:6px;">'
                f'ICICI Pru {fund["name"]}</div>'
                f'<div style="display:flex;gap:6px;flex-wrap:wrap;">'
                f'<span style="background:rgba(139,92,246,0.12);color:#c4b5fd;padding:3px 8px;'
                f'border-radius:6px;font-size:0.68rem;">{fund["category"]}</span>'
                f'<span style="background:rgba({",".join(str(int(color.lstrip("#")[j:j+2],16)) for j in (0,2,4))},0.15);'
                f'color:{color};padding:3px 8px;border-radius:6px;font-size:0.68rem;">'
                f'{fund["risk"]} Risk</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
