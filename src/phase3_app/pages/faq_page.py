"""
FAQ Page — Expandable categorized mutual fund FAQs.
"""
import streamlit as st


FAQ_DATA = {
    "Investment Basics": [
        {
            "q": "What is SIP (Systematic Investment Plan)?",
            "a": "SIP is a method of investing a fixed amount regularly in a mutual fund scheme. It allows investors to buy units on a given date each month, helping to average the purchase cost over time through rupee cost averaging."
        },
        {
            "q": "What is NAV (Net Asset Value)?",
            "a": "NAV is the per-unit market value of a mutual fund. It is calculated by dividing the total value of all assets in the fund (minus liabilities) by the total number of outstanding units."
        },
        {
            "q": "What is a lock-in period?",
            "a": "A lock-in period is the minimum duration for which an investment must be held before it can be redeemed. For example, ELSS funds have a mandatory 3-year lock-in period."
        },
    ],
    "Costs & Charges": [
        {
            "q": "What is expense ratio?",
            "a": "The expense ratio is the annual fee charged by a mutual fund to manage your investment. It covers fund management, administration, and distribution costs. A lower expense ratio means more of your returns are retained."
        },
        {
            "q": "What is exit load?",
            "a": "Exit load is a fee charged when an investor redeems mutual fund units before a specified period. It is designed to discourage early withdrawal and is typically 1% if redeemed within 1 year."
        },
    ],
    "Fund Categories": [
        {
            "q": "What is ELSS (Equity Linked Savings Scheme)?",
            "a": "ELSS is a type of equity mutual fund that offers tax deductions under Section 80C of the Income Tax Act, up to ₹1.5 lakh per year. It has a mandatory 3-year lock-in period, the shortest among all Section 80C instruments."
        },
        {
            "q": "What is a FlexiCap Fund?",
            "a": "A FlexiCap Fund is an open-ended equity scheme that can invest across large-cap, mid-cap, and small-cap stocks without any restriction on allocation. This gives the fund manager flexibility to shift between market capitalizations."
        },
        {
            "q": "What is a Liquid Fund?",
            "a": "A Liquid Fund invests in very short-term debt instruments with maturities up to 91 days. These are considered low-risk and are suitable for parking surplus funds or as an alternative to savings accounts."
        },
        {
            "q": "What is a Hybrid/Balanced Fund?",
            "a": "A Hybrid Fund invests in a mix of equity and debt instruments to balance risk and return. The allocation ratio depends on the fund type — aggressive hybrid funds invest 65-80% in equity, while conservative ones lean towards debt."
        },
    ],
    "ICICI Prudential Specific": [
        {
            "q": "How many ICICI Prudential schemes are indexed?",
            "a": "This chatbot currently indexes 19 ICICI Prudential Mutual Fund schemes plus the fund house overview page and 4 educational/category pages from Groww — totalling 24 data sources."
        },
        {
            "q": "Where does this chatbot get its data?",
            "a": "All data is scraped from official Groww.in pages for ICICI Prudential Mutual Fund schemes. This includes scheme-specific details like NAV, expense ratio, exit load, minimum investment, and fund manager information."
        },
    ],
}


def render():
    st.markdown(
        '<div style="max-width:850px;margin:0 auto;padding:32px 24px;">'
        '<h2 style="font-size:1.6rem;font-weight:800;'
        'background:linear-gradient(135deg,#8b5cf6,#06b6d4);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'margin-bottom:4px;">Frequently Asked Questions</h2>'
        '<p style="color:#64748b;font-size:0.9rem;margin-bottom:28px;">'
        'Quick answers to common mutual fund questions.</p>',
        unsafe_allow_html=True
    )

    # Search filter
    search = st.text_input(
        "🔍 Search FAQs",
        placeholder="Type to filter questions...",
        label_visibility="collapsed"
    )

    for category, items in FAQ_DATA.items():
        filtered = [
            item for item in items
            if not search or search.lower() in item["q"].lower() or search.lower() in item["a"].lower()
        ]
        if not filtered:
            continue

        st.markdown(
            f'<div style="margin-top:24px;margin-bottom:10px;font-size:0.75rem;'
            f'font-family:JetBrains Mono;color:#8b5cf6;text-transform:uppercase;'
            f'letter-spacing:2px;">{category}</div>',
            unsafe_allow_html=True
        )

        for item in filtered:
            with st.expander(item["q"]):
                st.markdown(
                    f'<div style="color:#94a3b8;line-height:1.7;font-size:0.92rem;">'
                    f'{item["a"]}</div>',
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)
