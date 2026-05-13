import os
from groq import Groq
from src.phase2_rag.prompts import RAG_SYSTEM_PROMPT

class GroqRAGClient:
    """Handles interaction with Groq LLM API."""
    
    def __init__(self, api_key: str = None, model: str = "llama-3.1-8b-instant"):
        # Uses GROQ_API_KEY from environment if not explicitly passed
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate_answer(self, query: str, context_chunks: list) -> str:
        """Constructs prompt with context and generates an answer."""
        
        # Build context string
        context_str = ""
        primary_source_url = None
        
        for i, chunk in enumerate(context_chunks):
            # Extract source URL for citation (take the first one as primary)
            metadata = chunk.metadata
            if primary_source_url is None and "source_url" in metadata:
                primary_source_url = metadata["source_url"]
                
            context_str += f"--- Document {i+1} ---\n{chunk.page_content}\n"
            if "source_url" in metadata:
                context_str += f"(Source URL: {metadata['source_url']})\n"
                
        # If no source URL was found in the chunks, use a generic fallback
        if not primary_source_url:
            primary_source_url = "No valid official source found."

        # Format prompt
        prompt = RAG_SYSTEM_PROMPT.format(context=context_str, query=query)
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.0, # Strict facts-only
                max_tokens=200,  # 3 sentences shouldn't need many tokens
            )
            
            answer = chat_completion.choices[0].message.content
            
            # Post-processing safeguard to ensure citation is present
            if "Source:" not in answer:
                answer += f"\n\nSource: {primary_source_url}"
                
            return answer
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return "An error occurred while connecting to the AI service. Please try again later."
