import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.phase2_rag.prompts import RAG_SYSTEM_PROMPT
from src.phase2_rag.groq_client import GroqRAGClient
from src.phase1_ingestion.vector_store import VectorStoreManager

def test_subphase_2c_2d():
    print("=== Testing Subphases 2C & 2D: Prompt Eng & Groq LLM Integration ===")
    
    # Check if GROQ_API_KEY is available
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️  Warning: GROQ_API_KEY not found in environment. Testing skipped.")
        # Alternatively, we could read from secrets.toml for testing.
        import toml
        try:
            secrets = toml.load(".streamlit/secrets.toml")
            if "GROQ_API_KEY" in secrets:
                os.environ["GROQ_API_KEY"] = secrets["GROQ_API_KEY"]
                print("✅ Found GROQ_API_KEY in secrets.toml.")
            else:
                print("❌ GROQ_API_KEY missing from secrets.toml.")
                return
        except Exception as e:
            print(f"❌ Could not load secrets.toml: {e}")
            return
            
    # 1. Test Retrieval + Generation
    print("\nInitializing VectorStore and GroqClient...")
    try:
        vs_manager = VectorStoreManager(persist_directory="chromadb_store")
        groq_client = GroqRAGClient()
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
        
    query = "What is the expense ratio of ICICI Prudential FlexiCap Fund?"
    print(f"\nQuerying: '{query}'")
    
    chunks = vs_manager.similarity_search(query, top_k=3)
    
    if not chunks:
        print("❌ Retrieval failed, cannot test Generation.")
        return
        
    print(f"Retrieved {len(chunks)} context chunks.")
    
    print("\nCalling Groq LLM...")
    response = groq_client.generate_answer(query, chunks)
    
    print("\n--- LLM Response ---")
    print(response)
    print("--------------------")
    
    # Validation against Acceptance Criteria
    passed = True
    
    # 1. <= 3 sentences
    # Basic sentence counting logic
    sentence_count = len([s for s in response.replace("\n\n", " ").split(". ") if s.strip()])
    print(f"\nSentence Count (approx): {sentence_count}")
    if sentence_count > 3 and "Source:" not in response.split(". ")[-1]:
        # Account for the Source: URL line
        print("❌ Output exceeds 3 sentences!")
        passed = False
        
    # 2. Contains exactly one Source URL
    source_count = response.count("Source:")
    print(f"Source Link Count: {source_count}")
    if source_count != 1:
        print("❌ Output must contain exactly one 'Source:' link!")
        passed = False
        
    if passed:
        print("\n✅ Subphases 2C & 2D Tests Passed!")
    else:
        print("\n❌ Subphases 2C & 2D Tests Failed!")

if __name__ == "__main__":
    test_subphase_2c_2d()
