# Streamlit Community Cloud Deployment Guide

This guide walks you through deploying the **RAG-Based Mutual Fund FAQ Chatbot** to the Streamlit Community Cloud (Phase 4C).

## Prerequisites
1. Ensure all your latest code is committed and pushed to your GitHub repository (`indubhaskar25/RAG-Based-Mutual-Fund-FAQ-Chatbot`).
2. Run the **"Daily Data Ingestion"** GitHub Action manually under the "Actions" tab in your repository. This will securely build and force-push the `chromadb_store/` to your repo.
3. Have your `GROQ_API_KEY` ready.

## Step-by-Step Deployment Instructions

1. **Sign In to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/).
   - Click **Continue with GitHub** and authorize Streamlit to access your repositories.

2. **Create a New App**
   - Click the **New app** button.
   - You might be prompted to authorize additional permissions; accept them.

3. **Configure the Repository Settings**
   - **Repository:** Search for and select `indubhaskar25/RAG-Based-Mutual-Fund-FAQ-Chatbot`.
   - **Branch:** Ensure this is set to `main` (or the branch you pushed your code to).
   - **Main file path:** Enter `app.py` (this is the root entry point that points to `src/phase3_app/streamlit_app.py`).

4. **Add Secrets (API Keys)**
   - Before clicking "Deploy", click on **Advanced settings...**.
   - In the **Secrets** text box, add your Groq API key exactly like this:
     ```toml
     GROQ_API_KEY = "your_actual_api_key_here"
     ```
   - Click **Save**.

5. **Deploy the App**
   - Click the **Deploy!** button.
   - Streamlit will now provision a server, install dependencies from `requirements.txt`, and boot the app. This typically takes 2-3 minutes.

6. **Verify the Deployment**
   - Once the "baking" process finishes, your app will appear live on screen.
   - Test the chatbot by asking a factual question, such as: *"What is the expense ratio of the FlexiCap Fund?"*
   - Verify that the response includes a citation source link and that no errors occur.

## Troubleshooting

- **ModuleNotFoundError**: Ensure all packages are listed in `requirements.txt`.
- **ChromaDB Errors**: Make sure the GitHub Action was successfully run and that `chromadb_store/` files are present in your GitHub repository.
- **Groq API Errors**: Verify your `GROQ_API_KEY` was entered correctly in the Advanced Settings (Secrets).

> [!TIP]
> You can always update your secrets later by clicking the three dots (`...`) in the bottom right corner of your deployed app, selecting **Settings**, and going to the **Secrets** tab.
