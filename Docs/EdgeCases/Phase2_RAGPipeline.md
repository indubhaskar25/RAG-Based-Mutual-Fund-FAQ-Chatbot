# Edge Cases: Phase 2 - RAG Pipeline & Safety

This document outlines the edge cases for the Retrieval, Safety, and LLM Generation phase.

## 1. Query Safety Guardrail Edge Cases
*   **Subtly Advisory Queries:**
    *   *Issue:* The user might ask, "Is a 1% exit load good for me?" The current static keyword list might miss the nuance of "is [fact] good for me".
    *   *Mitigation:* If static keyword matching fails, we can add a lightweight LLM classification step before the main RAG chain to detect advisory intent with higher accuracy.
*   **Complex Factual Queries Triggering False Positives:**
    *   *Issue:* The user asks, "Which fund has the highest expense ratio?" This is factual but might trigger the "highest" keyword in the advisory blocklist.
    *   *Mitigation:* Refine the regex/keyword patterns or upgrade to a semantic similarity check for the guardrail.

## 2. Retrieval Edge Cases
*   **No Relevant Chunks Found:**
    *   *Issue:* The vector database returns chunks with very low similarity scores, meaning the answer isn't in the database.
    *   *Mitigation:* The prompt strictly enforces saying "I don't have this information." However, we should also implement a distance threshold on the retriever to reject chunks before they even reach the LLM.
*   **Contradictory Context:**
    *   *Issue:* The database contains chunks from the 2022 Factsheet and the 2023 Factsheet, presenting conflicting expense ratios.
    *   *Mitigation:* Add a "Recency" filter or sort to the retriever. Ensure metadata includes timestamps, and prioritize the most recent documents in the prompt.
*   **Vocabulary Mismatch (Acronyms):**
    *   *Issue:* The user asks about "TER" but the document only says "Total Expense Ratio". Dense embeddings usually handle this, but BM25 keyword search might fail.
    *   *Mitigation:* Rely on the `all-MiniLM-L6-v2` semantic embeddings, which map acronyms to full words well.

## 3. LLM Generation Edge Cases
*   **Groq API Rate Limits / Timeouts:**
    *   *Issue:* Spikes in traffic or Groq service outages cause generation to fail.
    *   *Mitigation:* Implement exponential backoff retries in `groq_client.py` and provide a graceful fallback message to the user in the UI.
*   **Hallucinated Citations:**
    *   *Issue:* The LLM generates a URL that looks like an official SBI domain but is entirely fabricated, violating the exact citation constraint.
    *   *Mitigation:* The current architecture uses a post-processing safeguard that explicitly appends the exact `source_url` extracted directly from the ChromaDB metadata, bypassing the LLM's own URL generation.
*   **Context Window Overflow:**
    *   *Issue:* If top-k is increased or chunks are too large, the context may exceed the Llama 3 context window.
    *   *Mitigation:* Enforce strict chunk sizes (800 chars) and a low top-k (3) to guarantee the prompt stays well within limits.
