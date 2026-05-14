import sys
import os

# --- SQLite3 fix for Streamlit Community Cloud (ChromaDB requirement) ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass # Local dev might not need this
# ------------------------------------------------------------------------

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Delegate execution to the Phase 3 app
from src.phase3_app.streamlit_app import main

if __name__ == "__main__":
    main()
