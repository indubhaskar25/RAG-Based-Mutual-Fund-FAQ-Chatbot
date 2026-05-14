# Monitoring and Maintenance Plan

This document outlines the operational procedures for maintaining the **RAG-Based Mutual Fund FAQ Chatbot** in a production environment (Phase 4E).

## 1. Monitoring via Streamlit Community Cloud

Streamlit Community Cloud provides built-in metrics and logs.

- **App Uptime**: Your app will automatically spin down after several days of inactivity. If a user visits the URL, it will wake up (taking ~1-2 minutes). To prevent this, you can ping the app periodically or rely on the fact that Streamlit will automatically wake it up.
- **Resource Usage**: You can monitor memory and CPU usage from the Streamlit Cloud dashboard. If the app exceeds 1GB of RAM, it will be automatically restarted. Keep an eye on memory limits during heavy vector retrieval.
- **Logs**: Click "Manage app" in the bottom right corner of the live app to view real-time logs. This is critical for debugging API timeouts or errors.

## 2. API Monitoring and Alerting

### Groq LLM API
- Monitor usage limits and costs via the [Groq Console](https://console.groq.com/).
- Check for Rate Limiting (`429 Too Many Requests`). If these occur frequently, consider adding backoff logic or upgrading the tier.

### GitHub Actions (Data Ingestion)
- The scheduled `ingest_data.yml` runs daily at 00:00 UTC.
- To monitor this, go to the **Actions** tab in your GitHub repository.
- GitHub will automatically send an email to the repository owner if a workflow run fails (e.g., if Groww changes their HTML structure and breaks the scraper).

## 3. Maintenance Procedures

### Updating Dependencies
Periodically update packages in `requirements.txt` to patch security vulnerabilities.
1. Create a branch: `git checkout -b update-deps`
2. Test locally: `pip install -r requirements.txt` and run `streamlit run app.py`
3. Merge to `main`. Streamlit Cloud will automatically trigger a rebuild.

### Changing LLM Prompts or Logic
All changes pushed to the `main` branch will automatically trigger a hot reload on Streamlit Cloud. If the change breaks the app, Streamlit will show an error trace on the screen. Always test locally first!

## 4. Rollback Plan

If a bad commit brings down the application, rollback immediately:

1. Find the last stable commit hash using `git log`.
2. Revert the repository locally:
   ```bash
   git revert <bad_commit_hash>
   ```
3. Push the revert commit:
   ```bash
   git push origin main
   ```
4. Streamlit Cloud will automatically pull the revert commit and redeploy the stable version within 1-2 minutes.

## 5. Vector Database Backup Strategy

Since we are using Local ChromaDB with Streamlit Cloud:
- The authoritative source of truth for the vector database is the `chromadb_store/` directory committed to the `main` branch.
- The GitHub Action runs daily, creating fresh `chromadb_store/` files and committing them.
- **Backup**: Every GitHub commit acts as an automatic backup. If the vector database becomes corrupted, you can easily restore `chromadb_store/` from a previous commit.
