"""
Data source configuration for the Mutual Fund FAQ Chatbot.
Contains the exact, fixed set of 24 Groww URLs used for this project.
AMC: ICICI Prudential Mutual Fund | Source: Groww.in

This is the ONLY data source file. No other URLs should be added
without updating the Architecture document.
"""

# Fund House Overview
FUND_HOUSE_URLS = [
    {
        "url": "https://groww.in/mutual-funds/filter?fund_house=%5B%22ICICI+Prudential+Mutual+Fund%22%5D",
        "scheme_name": "ICICI Prudential Fund House Overview",
        "document_type": "Fund House Listing",
        "amc": "ICICI Prudential Mutual Fund",
    },
]

# Individual Scheme Pages (19 Schemes)
SCHEME_URLS = [
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-silver-etf-fof-direct-growth",
        "scheme_name": "ICICI Prudential Silver ETF FoF",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-large-cap-fund-direct-growth",
        "scheme_name": "ICICI Prudential Large Cap Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-dynamic-plan-direct-growth",
        "scheme_name": "ICICI Prudential Dynamic Plan",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-top-100-fund-direct-growth",
        "scheme_name": "ICICI Prudential Top 100 Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-infrastructure-fund-direct-growth",
        "scheme_name": "ICICI Prudential Infrastructure Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-commodities-fund-direct-growth",
        "scheme_name": "ICICI Prudential Commodities Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-balanced-direct-growth",
        "scheme_name": "ICICI Prudential Balanced Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-flexicap-fund-direct-growth",
        "scheme_name": "ICICI Prudential FlexiCap Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-retirement-fund-pure-equity-plan-direct-growth",
        "scheme_name": "ICICI Prudential Retirement Fund Pure Equity Plan",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-short-term-plan-direct-growth",
        "scheme_name": "ICICI Prudential Short Term Plan",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-liquid-fund-direct-plan-growth",
        "scheme_name": "ICICI Prudential Liquid Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-indo-asia-equity-fund-direct-growth",
        "scheme_name": "ICICI Prudential Indo Asia Equity Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-nifty-index-fund-direct-growth",
        "scheme_name": "ICICI Prudential Nifty Index Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-multicap-fund-direct-growth",
        "scheme_name": "ICICI Prudential MultiCap Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-corporate-bond-fund-direct-plan-growth",
        "scheme_name": "ICICI Prudential Corporate Bond Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-nifty-midcap-150-index-fund-direct-growth",
        "scheme_name": "ICICI Prudential Nifty Midcap 150 Index Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-dividend-yield-equity-fund-direct-growth",
        "scheme_name": "ICICI Prudential Dividend Yield Equity Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-aggressive-hybrid-active-fof-direct-growth",
        "scheme_name": "ICICI Prudential Aggressive Hybrid Active FoF",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
    {
        "url": "https://groww.in/mutual-funds/icici-prudential-business-cycle-fund-direct-growth",
        "scheme_name": "ICICI Prudential Business Cycle Fund",
        "document_type": "Scheme Page",
        "amc": "ICICI Prudential Mutual Fund",
    },
]

# Educational / Info Pages
EDUCATIONAL_URLS = [
    {
        "url": "https://groww.in/p/expense-ratio",
        "scheme_name": "General - Expense Ratio",
        "document_type": "Educational",
        "amc": "General",
    },
    {
        "url": "https://groww.in/p/exit-load-in-mutual-funds",
        "scheme_name": "General - Exit Load",
        "document_type": "Educational",
        "amc": "General",
    },
    {
        "url": "https://groww.in/p/sip-systematic-investment-plan",
        "scheme_name": "General - SIP",
        "document_type": "Educational",
        "amc": "General",
    },
]

# Category Pages
CATEGORY_URLS = [
    {
        "url": "https://groww.in/mutual-funds/equity-funds/elss-funds",
        "scheme_name": "ELSS Funds Category",
        "document_type": "Category Listing",
        "amc": "General",
    },
]

# Combined list of all URLs for ingestion (24 total)
ALL_URLS = FUND_HOUSE_URLS + SCHEME_URLS + EDUCATIONAL_URLS + CATEGORY_URLS
