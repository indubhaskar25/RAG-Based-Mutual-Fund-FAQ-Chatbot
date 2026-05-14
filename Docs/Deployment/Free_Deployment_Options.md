# Free Deployment Options for RAG-Based Mutual Fund FAQ Chatbot

## Overview
This document outlines free deployment options for the RAG-Based Mutual Fund FAQ Chatbot project using various free-tier services.

---

## 1. Streamlit Cloud (Recommended for Frontend)

### Free Tier Features
- **Cost:** $0/month
- **Resources:** 1 CPU, 512MB RAM
- **Apps:** Unlimited public apps
- **Custom Domains:** Not available on free tier
- **Persistence:** File system is ephemeral (resets on redeploy)

### Deployment Steps
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repository: `indubhaskar25/RAG-Based-Mutual-Fund-FAQ-Chatbot`
5. Configure:
   - Main file path: `app.py`
   - Python version: 3.11
6. Add secrets in app settings:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

### Limitations
- No persistent storage (ChromaDB will reset)
- Limited compute resources
- No custom domains
- Sleeps after inactivity (cold starts)

---

## 2. GitHub Actions (Free CI/CD)

### Free Tier Features
- **Cost:** $0/month for public repositories
- **Minutes:** 2000 minutes/month
- **Storage:** 500MB
- **Runners:** Ubuntu, Windows, macOS

### Current Workflow
The project already has a GitHub Actions workflow at `.github/workflows/ingest_data.yml`

### Usage
- Automatically runs on push to main branch
- Can be triggered manually from GitHub Actions tab
- Perfect for data ingestion pipeline automation

### Limitations
- Not suitable for hosting applications
- Limited to CI/CD tasks
- 2000 minutes/month limit

---

## 3. Free Vector Database Options

### Option A: ChromaDB (Local/File-based)
- **Cost:** Free
- **Storage:** Local file system
- **Best for:** Development, testing
- **Limitations:** No persistence on Streamlit Cloud

### Option B: Pinecone (Free Tier)
- **Cost:** Free tier available
- **Storage:** 1 project, 1 index
- **Vectors:** Up to 5 million vectors
- **Best for:** Production with persistence
- **Sign up:** [pinecone.io](https://www.pinecone.io)

### Option C: Qdrant Cloud (Free Tier)
- **Cost:** Free tier available
- **Storage:** 1GB
- **Vectors:** 10,000 vectors
- **Best for:** Small to medium projects
- **Sign up:** [cloud.qdrant.io](https://cloud.qdrant.io)

### Option D: Weaviate Cloud (Free Tier)
- **Cost:** Free sandbox
- **Storage:** 1GB
- **Vectors:** 1 million vectors
- **Best for:** Testing and development
- **Sign up:** [weaviate.cloud](https://weaviate.cloud)

---

## 4. Free Hosting Alternatives

### Option A: Render (Free Tier)
- **Cost:** $0/month
- **Resources:** 512MB RAM, 0.1 CPU
- **Sleep:** Spins down after 15 minutes inactivity
- **Best for:** Web apps, APIs
- **Sign up:** [render.com](https://render.com)
- **Deployment:** Connect GitHub repo

### Option B: Railway (Free Tier)
- **Cost:** $5/month credit (effectively free for small apps)
- **Resources:** 512MB RAM
- **Best for:** Full-stack applications
- **Sign up:** [railway.app](https://railway.app)
- **Deployment:** Connect GitHub repo

### Option C: PythonAnywhere (Free Tier)
- **Cost:** Free tier available
- **Resources:** Limited CPU, 512MB RAM
- **Best for:** Python web apps
- **Sign up:** [pythonanywhere.com](https://www.pythonanywhere.com)
- **Limitations:** No background tasks on free tier

### Option D: Vercel (Free Tier)
- **Cost:** $0/month
- **Resources:** Serverless functions
- **Best for:** Static sites, APIs
- **Sign up:** [vercel.com](https://vercel.com)
- **Note:** Best for Next.js/React, not ideal for Streamlit

### Option E: Hugging Face Spaces (Free)
- **Cost:** Free
- **Resources:** CPU, limited GPU options
- **Best for:** ML models, demos
- **Sign up:** [huggingface.co/spaces](https://huggingface.co/spaces)
- **Perfect for:** Streamlit apps with ML components

---

## 5. Recommended Free Architecture

### Option 1: Streamlit Cloud + Pinecone (Recommended)
```
Frontend: Streamlit Cloud (Free)
Vector DB: Pinecone Free Tier
LLM: Groq (Free tier available)
CI/CD: GitHub Actions (Free)
```

**Pros:**
- Fully persistent vector database
- Easy deployment
- No backend server needed
- Free LLM inference

**Cons:**
- Streamlit Cloud has cold starts
- Limited compute resources

### Option 2: Hugging Face Spaces + Qdrant
```
Frontend: Hugging Face Spaces (Free)
Vector DB: Qdrant Cloud Free Tier
LLM: Groq (Free tier available)
CI/CD: GitHub Actions (Free)
```

**Pros:**
- Better for ML demos
- Persistent vector database
- Community visibility

**Cons:**
- Limited resources
- May have queue times

### Option 3: Render + ChromaDB (Local Persistence)
```
Frontend: Render (Free)
Vector DB: ChromaDB (with volume mount - paid)
LLM: Groq (Free tier available)
CI/CD: GitHub Actions (Free)
```

**Pros:**
- More flexible hosting
- Can add custom domain

**Cons:**
- Persistent storage requires paid tier
- Cold starts on free tier

---

## 6. Deployment Guide: Streamlit Cloud + Pinecone

### Step 1: Set up Pinecone
1. Sign up at [pinecone.io](https://www.pinecone.io)
2. Create a new index:
   - Name: `mutual-fund-rag`
   - Dimension: 384 (for sentence-transformers)
   - Metric: cosine
3. Get API key from dashboard

### Step 2: Update Code for Pinecone
Modify `src/phase1_ingestion/vector_store.py`:
```python
# Add Pinecone support
import pinecone

# Initialize Pinecone
pinecone.init(api_key="your-pinecone-api-key")
index = pinecone.Index("mutual-fund-rag")
```

### Step 3: Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository and deploy
4. Add secrets:
   ```
   GROQ_API_KEY=your_groq_key
   PINECONE_API_KEY=your_pinecone_key
   ```

### Step 4: Run Ingestion Locally
Since Streamlit Cloud doesn't support long-running background tasks:
1. Run ingestion locally:
   ```bash
   python run_ingestion.py
   ```
2. Data will be stored in Pinecone (persistent)
3. Streamlit Cloud app will query Pinecone

---

## 7. Cost Comparison (Free Tiers)

| Service | Free Tier | Limitations | Best For |
|---------|-----------|-------------|----------|
| Streamlit Cloud | $0 | 512MB RAM, no persistence | Frontend |
| Pinecone | Free | 5M vectors, 1 project | Vector DB |
| Qdrant Cloud | Free | 10K vectors, 1GB | Small projects |
| Groq | Free tier | Rate limits apply | LLM |
| GitHub Actions | Free (public) | 2000 min/month | CI/CD |
| Render | $0 | Cold starts, 512MB RAM | Web apps |
| Hugging Face | Free | Limited resources | ML demos |

---

## 8. Next Steps

### For Immediate Deployment:
1. **Deploy to Streamlit Cloud** (easiest, no code changes)
2. **Set up Pinecone** for persistent vector storage
3. **Configure GitHub Actions** for automated data ingestion

### For Production-Ready Setup:
1. Migrate to Pinecone or Qdrant for persistence
2. Set up monitoring and logging
3. Implement error handling and retries
4. Add rate limiting for API calls

### For Scaling:
1. Upgrade to paid tiers as needed
2. Consider custom domain (requires paid plan)
3. Implement caching layer
4. Add CDN for static assets

---

## 9. Troubleshooting

### Common Issues:
1. **Cold starts on Streamlit Cloud**
   - Solution: Use persistent vector DB (Pinecone)
   - Consider upgrading to paid tier for always-on

2. **Memory limits**
   - Solution: Optimize chunking size
   - Use streaming responses
   - Consider paid tier for more RAM

3. **API rate limits**
   - Solution: Implement caching
   - Use exponential backoff
   - Consider paid API tiers

---

## 10. Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Pinecone Documentation](https://docs.pinecone.io)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Groq API Documentation](https://console.groq.com/docs)
- [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)
