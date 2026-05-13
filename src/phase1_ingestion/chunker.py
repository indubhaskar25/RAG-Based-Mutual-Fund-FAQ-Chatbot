"""
Phase 1: Text Chunker
Splits scraped text into semantically coherent chunks with metadata tagging.
Ensures every chunk carries source_url for mandatory citation.
"""

import uuid
from typing import Dict, Any, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextChunker:
    """Chunks text and attaches metadata for citation tracking."""

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict]:
        """
        Splits text into chunks and attaches metadata to each.
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to chunker, skipping.")
            return []

        # Contextual prefix to help RAG accuracy
        scheme_name = metadata.get("scheme_name", "Unknown ICICI Mutual Fund")
        prefix = f"FUND: {scheme_name}\nCONTEXT: Detailed facts and figures for {scheme_name}\n---\n"

        chunks = self.splitter.split_text(text)
        results = []

        for chunk in chunks:
            # Prepend context to the text itself for better embedding matching
            contextualized_text = prefix + chunk
            results.append({
                "id": str(uuid.uuid4()),
                "text": contextualized_text,
                "metadata": metadata.copy(),
            })

        logger.info(f"Created {len(results)} chunks from {metadata.get('scheme_name', 'unknown')}")
        return results
