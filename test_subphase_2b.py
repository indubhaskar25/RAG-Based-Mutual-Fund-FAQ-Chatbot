import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.phase1_ingestion.vector_store import VectorStoreManager

def test_subphase_2b():
    print("=== Testing Subphase 2B: Vector Retrieval ===")
    
    # 2B.1 Load the existing ChromaDB store
    try:
        vs_manager = VectorStoreManager(persist_directory="chromadb_store")
        print("✅ VectorStoreManager initialized successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize VectorStoreManager: {e}")
        return

    # 2B.4 Test Query
    query = "What is the exit load for ICICI Prudential Large Cap Fund?"
    print(f"\nQuerying: '{query}'")
    
    # 2B.2 Implement similarity_search
    chunks = vs_manager.similarity_search(query, top_k=3)
    
    if not chunks:
        print("❌ No chunks returned.")
        return
        
    print(f"Retrieved {len(chunks)} chunks.")
    
    passed = True
    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---")
        metadata = chunk.metadata
        print(f"Metadata: {metadata}")
        
        # Check for source_url
        if "source_url" not in metadata:
            print("❌ Missing 'source_url' in metadata!")
            passed = False
        else:
            print(f"✅ 'source_url' found: {metadata['source_url']}")
            
        print(f"Snippet: {chunk.page_content[:100]}...")

    if passed:
        print("\n✅ Subphase 2B Test Passed!")
    else:
        print("\n❌ Subphase 2B Test Failed due to missing metadata.")

if __name__ == "__main__":
    test_subphase_2b()
