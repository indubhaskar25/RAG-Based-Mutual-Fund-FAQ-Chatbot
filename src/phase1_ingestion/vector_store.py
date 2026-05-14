"""
Phase 1: Vector Store Manager
Handles embedding generation and ChromaDB persistence using NATIVE FastEmbed.
Completely bypasses LangChain/Torch wrappers to prevent Mac 'meta tensor' errors.
"""

from typing import List, Dict, Any
import os
import logging
import numpy as np
from fastembed import TextEmbedding
from langchain_community.vectorstores import Chroma

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NativeFastEmbeddings:
    """Native FastEmbed wrapper that completely bypasses Torch/LangChain logic."""
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        # This uses ONNX runtime, NO TORCH involved. 100% stable on Mac.
        self.model = TextEmbedding(model_name=model_name)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = list(self.model.embed(texts))
        return [e.tolist() for e in embeddings]
    
    def embed_query(self, text: str) -> List[float]:
        embedding = list(self.model.embed([text]))[0]
        return embedding.tolist()

class VectorStoreManager:
    def __init__(self, persist_directory: str = "chromadb_store"):
        self.persist_directory = persist_directory
        self.embeddings = NativeFastEmbeddings()
        
        # Initialize or Load ChromaDB
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        # If empty, auto-index
        if not os.path.exists(persist_directory) or len(self.vector_store.get()['ids']) == 0:
            self._auto_index()
            
        logger.info(f"VectorStoreManager active with NATIVE FastEmbed backend.")

    def _auto_index(self):
        """Automatically index source documents."""
        data_path = "data/raw_scraped"
        if not os.path.exists(data_path): return

        try:
            from langchain_core.documents import Document
        except ImportError:
            from langchain.docstore.document import Document

        documents = []
        for file_name in os.listdir(data_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(data_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    chunks = [text[i:i+1000] for i in range(0, len(text), 800)]
                    for i, chunk in enumerate(chunks):
                        documents.append(Document(page_content=chunk, metadata={"source": file_name}))

        if documents:
            self.vector_store.add_documents(documents)

    def add_documents(self, documents: List[Any]):
        """Add LangChain documents to the vector store."""
        if not documents: return
        self.vector_store.add_documents(documents)

    def add_chunks(self, chunks: List[Dict]):
        """Converts raw chunk dicts from chunker.py into Document objects and adds them."""
        try:
            from langchain_core.documents import Document
        except ImportError:
            from langchain.docstore.document import Document

        docs = []
        for c in chunks:
            docs.append(Document(
                page_content=c["text"],
                metadata=c["metadata"]
            ))
        self.add_documents(docs)

    def get_collection_count(self) -> int:
        """Returns the total number of chunks in the collection."""
        return len(self.vector_store.get()['ids'])

    def get_retriever(self, top_k: int = 5):
        return self.vector_store.as_retriever(search_kwargs={"k": top_k})
