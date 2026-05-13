import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.phase2_rag.guardrail import QueryGuardrail

def test_subphase_2a():
    print("=== Testing Subphase 2A: Query Safety Guardrail ===")
    
    # Test 1: Advisory Query
    advisory_query = "Should I invest in ICICI Prudential Large Cap Fund?"
    is_blocked = QueryGuardrail.is_advisory(advisory_query)
    print(f"Query: '{advisory_query}'")
    print(f"Blocked? {is_blocked} (Expected: True)")
    if is_blocked:
        refusal = QueryGuardrail.get_refusal_response()
        print(f"Response: {refusal['answer']}")
        print(f"Source: {refusal['source_url']}")
        
    print("-" * 40)
    
    # Test 2: Factual Query
    factual_query = "What is the expense ratio of ICICI Prudential FlexiCap Fund?"
    is_blocked_factual = QueryGuardrail.is_advisory(factual_query)
    print(f"Query: '{factual_query}'")
    print(f"Blocked? {is_blocked_factual} (Expected: False)")

    if is_blocked and not is_blocked_factual:
        print("✅ Subphase 2A Test Passed!")
    else:
        print("❌ Subphase 2A Test Failed!")

if __name__ == "__main__":
    test_subphase_2a()
