import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.phase1_ingestion.vector_store import VectorStoreManager
from src.phase2_rag.groq_client import GroqRAGClient
from src.phase2_rag.guardrail import QueryGuardrail

# Initialize FastAPI app
app = FastAPI(title="RAG Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG components
vs_manager = VectorStoreManager(persist_directory="../chromadb_store")
retriever = vs_manager.get_retriever(top_k=5)
groq_client = GroqRAGClient()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return the RAG response."""
    try:
        query = request.message
        
        # Check if query is advisory (should be filtered)
        if QueryGuardrail.is_advisory(query):
            refusal = QueryGuardrail.get_refusal_response()
            return ChatResponse(
                answer=refusal['answer'],
                sources=[]
            )
        
        # Retrieve relevant documents
        docs = retriever.invoke(query)
        
        if not docs:
            return ChatResponse(
                answer="No relevant documentation found for your query. Please try rephrasing your question or ask about specific mutual fund topics.",
                sources=[]
            )
        
        # Generate answer using Groq
        answer = groq_client.generate_answer(query, docs)
        
        # Extract sources from document metadata
        sources = list(set([
            doc.metadata.get('source', 'Official Doc').split('/')[-1] 
            for doc in docs
        ]))[:4]
        
        # Clean up answer (remove "Source:" prefix if present)
        if "Source:" in answer:
            answer = answer.split("Source:")[0].strip()
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
        
    except Exception as e:
        print(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Failed to process your request")

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "RAG Chatbot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
