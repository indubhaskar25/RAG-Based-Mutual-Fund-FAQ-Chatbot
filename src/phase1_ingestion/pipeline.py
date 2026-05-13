"""
Phase 1: Ingestion Pipeline Orchestrator
Coordinates the full Phase 1 flow:
  Sources → Scraper → Chunker → Vector Store

Usage:
    from src.phase1_ingestion.pipeline import IngestionPipeline
    pipeline = IngestionPipeline()
    pipeline.run()
"""

import time
import logging
from src.phase1_ingestion.sources import ALL_URLS
from src.phase1_ingestion.html_scraper import HTMLScraper
from src.phase1_ingestion.chunker import TextChunker
from src.phase1_ingestion.vector_store import VectorStoreManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Orchestrates the complete Phase 1 data ingestion."""

    def __init__(
        self,
        persist_directory: str = "chromadb_store",
        chunk_size: int = 800,
        chunk_overlap: int = 150,
        request_delay: float = 1.5,
    ):
        self.scraper = HTMLScraper()
        self.chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.vector_store = VectorStoreManager(persist_directory=persist_directory)
        self.request_delay = request_delay

    def run(self, urls: list = None):
        """
        Runs the full ingestion pipeline on the provided URLs.
        Defaults to ALL_URLS from sources.py if none provided.
        """
        if urls is None:
            urls = ALL_URLS

        total = len(urls)
        success = 0
        failed = 0

        print("=" * 60)
        print("Phase 1: Data Ingestion Pipeline")
        print(f"Total URLs to process: {total}")
        print("=" * 60)

        for i, source in enumerate(urls, 1):
            url = source["url"]
            scheme = source["scheme_name"]
            print(f"\n[{i}/{total}] {scheme}")
            print(f"  URL: {url}")

            # Step 1: Scrape
            text = self.scraper.scrape(url)

            # Save raw text for auditability
            if text:
                filename = f"data/raw_scraped/{scheme.replace(' ', '_').lower()}.txt"
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"  💾 Saved raw text to {filename}")
                except Exception as e:
                    print(f"  ⚠️ Warning: Could not save raw text: {e}")

            if not text:
                failed += 1
                print(f"  ❌ Failed — no usable text extracted")
                continue

            # Step 2: Chunk with metadata
            metadata = {
                "source_url": url,
                "scheme_name": source["scheme_name"],
                "document_type": source["document_type"],
                "amc": source["amc"],
            }
            chunks = self.chunker.chunk_text(text, metadata)

            if not chunks:
                failed += 1
                print(f"  ❌ Failed — chunking produced no results")
                continue

            # Step 3: Embed and store
            self.vector_store.add_chunks(chunks)
            success += 1
            print(f"  ✅ Success — {len(chunks)} chunks, {len(text)} chars")

            # Rate limiting
            time.sleep(self.request_delay)

        print("\n" + "=" * 60)
        print("Phase 1 Ingestion Complete!")
        print(f"  Successful: {success}/{total}")
        print(f"  Failed:     {failed}/{total}")
        print(f"  Total chunks in ChromaDB: {self.vector_store.get_collection_count()}")
        print("=" * 60)

        return {"success": success, "failed": failed, "total": total}
