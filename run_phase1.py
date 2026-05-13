from src.phase1_ingestion.pipeline import IngestionPipeline
import os

# Ensure data directory exists
os.makedirs("data/raw_scraped", exist_ok=True)

# Run full Phase 1 ingestion
print("--- Starting Phase 1: Data Foundation ---")
pipeline = IngestionPipeline(persist_directory="chromadb_store")
results = pipeline.run()
print(f"\nPhase 1 Results: {results}")
