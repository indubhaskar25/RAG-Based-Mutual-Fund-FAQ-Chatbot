📄 Problem Statement
RAG-Based Mutual Fund FAQ Chatbot
Project Domain
FinTech · AI/ML · Retrieval-Augmented Generation (RAG)

1. Problem Overview
Mutual fund investors frequently need quick, reliable answers to factual questions such as expense ratios, exit loads, minimum SIP amounts, lock-in periods, risk classifications, and benchmark indices. However, this information is often scattered across multiple official documents such as factsheets, Key Information Memorandums (KIM), Scheme Information Documents (SID), and regulatory websites like SEBI and AMFI.
Existing platforms either:
provide generic search results without clear answers, or
offer advice-driven responses, which may be biased or non-compliant
This creates a gap for users who want accurate, verifiable, and concise factual information without any investment advice.

2. Objective
Design and implement a Retrieval-Augmented Generation (RAG) based FAQ chatbot that:
Answers fact-based queries only about selected mutual fund schemes
Uses only official public sources (AMC websites, SEBI, AMFI)
Provides concise answers (≤3 sentences)
Includes exactly one source citation link in every response
Clearly refuses opinion-based or advisory questions

3. Scope
The system will focus on:
One selected Asset Management Company (AMC):
 Example: SBI Mutual Fund
3–5 mutual fund schemes under that AMC
A curated dataset of 15–25 official public pages, including:
Scheme pages
Factsheets
KIM/SID documents
Expense ratio and fee pages
Riskometer and benchmark explanations
Statement and tax document guides

4. Supported Queries
The chatbot will answer only factual queries such as:
“What is the expense ratio of SBI Bluechip Fund?”
“What is the exit load?”
“What is the minimum SIP amount?”
“What is the lock-in period for ELSS funds?”
“What is the riskometer and benchmark?”
“How can I download the capital gains statement?”

5. Constraints
The system must strictly adhere to:
Facts-only responses — no recommendations or opinions
Mandatory citation — every answer must include one source link
Public sources only — no blogs or third-party content
No personal data handling — no PAN, Aadhaar, or financial details
Concise answers — maximum 3 sentences

6. Expected Outcome
The final system will:
Deliver accurate, grounded, and verifiable answers
Reduce misinformation by relying only on official documents
Provide a safe and compliant user experience by avoiding advisory content
Demonstrate effective use of RAG for domain-specific factual QA systems

7. Key Insight
Unlike general chatbots, this system prioritizes:
retrieval accuracy over generation creativity
compliance and safety over opinion
traceability through citations

