# Edge Cases: Phase 3 - Application UI

This document outlines edge cases and usability issues specific to the Streamlit MVP application.

## 1. Environment & Infrastructure
*   **Missing API Keys:**
    *   *Issue:* The user deploys the app but forgets to set `GROQ_API_KEY` in Streamlit Community Cloud secrets.
    *   *Mitigation:* The `app.py` script checks for the key at startup. If missing, it immediately halts (`st.stop()`) and displays a clear error banner instructing the user to configure secrets, preventing ugly stack traces later.
*   **Vector Database Initialization Failure:**
    *   *Issue:* The `chromadb_store` directory is missing, corrupt, or permissions prevent reading it on the server.
    *   *Mitigation:* The `@st.cache_resource` function catches initialization errors and returns a null retriever, which is checked in `main()` to gracefully stop the app and display a user-friendly error.

## 2. UI and State Management
*   **Runaway Chat History:**
    *   *Issue:* The user asks 100+ questions in a single session. Passing the entire history back to the LLM would bloat the prompt and cause token limit errors or rate limiting.
    *   *Mitigation:* For a strict factual FAQ bot, conversational memory is not strictly necessary. We treat each query as independent. The UI retains the visual history, but we do not append the full `st.session_state.messages` to the RAG context string.
*   **Concurrent Users in Local Testing:**
    *   *Issue:* If deployed on a local server, multiple users accessing Streamlit might conflict if relying on global variables.
    *   *Mitigation:* Using `st.session_state` guarantees isolated state per browser tab, preventing cross-talk between different users.

## 3. User Input Anomalies
*   **Extremely Long Queries / Spam:**
    *   *Issue:* User pastes the entire script of a movie into the chat box.
    *   *Mitigation:* Streamlit handles large inputs gracefully, but we should add a character limit constraint before passing it to the embedding model or Groq to save tokens and prevent DoS.
*   **Empty or Nonsense Input:**
    *   *Issue:* User types "asdasd".
    *   *Mitigation:* The vector search will return the closest chunks (which might be irrelevant). The strict prompt ("If the Context does not contain the answer, say 'I don't have this information'") will ensure the LLM politely declines rather than hallucinating an answer.
