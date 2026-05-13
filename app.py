import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Delegate execution to the Phase 3 app
from src.phase3_app.streamlit_app import main

if __name__ == "__main__":
    main()
