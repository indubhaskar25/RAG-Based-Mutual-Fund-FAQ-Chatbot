"""
Phase 1 Entry Point: Run Data Ingestion
Scrapes all 24 Groww URLs and loads them into ChromaDB.

Usage:
    source venv/bin/activate
    python run_ingestion.py
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.phase1_ingestion.pipeline import IngestionPipeline


if __name__ == "__main__":
    pipeline = IngestionPipeline()
    result = pipeline.run()
