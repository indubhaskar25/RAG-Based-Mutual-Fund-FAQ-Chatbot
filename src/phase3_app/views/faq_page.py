"""
FAQ Page — Polished help-center with category chips and search.
"""
import streamlit as st

FAQ_DATA = {
    "💰 Investment Basics": [
        ("What is SIP (Systematic Investment Plan)?",
         "SIP is a method of investing a fixed amount regularly in a mutual fund scheme. It allows investors to buy units on a given date each month, helping to average the purchase cost over time through rupee cost averaging."),
        ("What is NAV (Net Asset Value)?",
         "NAV is the per-unit market value of a mutual fund. It is calculated by dividing the total value of all assets in the fund (minus liabilities) by the total number of outstanding units."),
        ("What is a lock-in period?",
         "A lock-in period is the minimum duration for which an investment must be held before it can be redeemed. For example, ELSS funds have a mandatory 3-year lock-in period."),
    ],
    "💳 Costs & Charges": [
        ("What is expense ratio?",
         "The expense ratio is the annual fee charged by a mutual fund to manage your investment. It covers fund management, administration, and distribution costs. A lower expense ratio means more of your returns are retained."),
        ("What is exit load?",
         "Exit load is a fee charged when an investor redeems mutual fund units before a specified period. It is designed to discourage early withdrawal and is typically 1% if redeemed within 1 year."),
    ],
    "📊 Fund Categories": [
        ("What is ELSS (Equity Linked Savings Scheme)?",
         "ELSS is a type of equity mutual fund that offers tax deductions under Section 80C of the Income Tax Act, up to ₹1.5 lakh per year. It has a mandatory 3-year lock-in period."),
        ("What is a FlexiCap Fund?",
         "A FlexiCap Fund is an open-ended equity scheme that can invest across large-cap, mid-cap, and small-cap stocks without any restriction on allocation."),
        ("What is a Liquid Fund?",
         "A Liquid Fund invests in very short-term debt instruments with maturities up to 91 days. These are considered low-risk and suitable for parking surplus funds."),
        ("What is a Hybrid/Balanced Fund?",
         "A Hybrid Fund invests in a mix of equity and debt instruments. Aggressive hybrid funds invest 65-80% in equity, while conservative ones lean towards debt."),
    ],
    "🏦 ICICI Prudential": [
        ("How many schemes are indexed?",
         "This chatbot currently indexes 19 ICICI Prudential Mutual Fund schemes plus the fund house overview page and 4 educational/category pages — totalling 24 data sources."),
        ("Where does this chatbot get its data?",
         "All data is scraped from official Groww.in pages for ICICI Prudential Mutual Fund schemes, including NAV, expense ratio, exit load, minimum investment, and fund manager information."),
    ],
}


def render():
    st.markdown(
        '<div style="max-width:780px;margin:0 auto;padding:28px 20px;">'
        '<div style="font-size:1.4rem;font-weight:700;color:#e2e8f0;margin-bottom:2px;">'
        '❓ Frequently Asked Questions</div>'
        '<div style="color:#64748b;font-size:0.82rem;margin-bottom:24px;">'
        'Quick answers to common mutual fund questions.</div>',
        unsafe_allow_html=True
    )

    # Search
    search = st.text_input(
        "Search", placeholder="Search FAQs...",
        label_visibility="collapsed"
    )

    # Category chips
    categories = list(FAQ_DATA.keys())
    selected = st.radio(
        "Category", ["All"] + categories,
        horizontal=True, label_visibility="collapsed"
    )

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    for cat, items in FAQ_DATA.items():
        if selected != "All" and selected != cat:
            continue

        filtered = [
            (q, a) for q, a in items
            if not search or search.lower() in q.lower() or search.lower() in a.lower()
        ]
        if not filtered:
            continue

        st.markdown(
            f'<div style="font-size:0.68rem;font-family:JetBrains Mono;color:#8b5cf6;'
            f'text-transform:uppercase;letter-spacing:1.5px;margin:18px 0 8px;">{cat}</div>',
            unsafe_allow_html=True
        )

        for q, a in filtered:
            with st.expander(q):
                st.markdown(
                    f'<div style="color:#94a3b8;line-height:1.7;font-size:0.88rem;">{a}</div>',
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)
