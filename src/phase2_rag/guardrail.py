class QueryGuardrail:
    """Detects advisory questions and enforces facts-only safety."""
    
    # Simple keyword/pattern matching for MVP. 
    ADVISORY_KEYWORDS = [
        "should i invest",
        "best fund",
        "highest return",
        "recommend a fund",
        "is it good to",
        "where should i put my money",
        "better to invest",
        "top fund",
        "which fund should i",
        "buy or sell",
        "good investment"
    ]
    
    @classmethod
    def is_advisory(cls, query: str) -> bool:
        """Returns True if the query asks for advice rather than facts."""
        query_lower = query.lower()
        for keyword in cls.ADVISORY_KEYWORDS:
            if keyword in query_lower:
                return True
        return False
        
    @staticmethod
    def get_refusal_response() -> dict:
        """Standard refusal response for advisory queries."""
        return {
            "answer": "I am a factual mutual fund assistant. I can only provide objective details such as expense ratios, exit loads, and lock-in periods based on official documents. I cannot provide investment advice, predict returns, or recommend specific funds.",
            "source_url": "https://www.investor.sebi.gov.in/mutual-funds.html" # Educational link
        }
