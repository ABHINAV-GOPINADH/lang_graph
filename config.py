import os
from dotenv import load_dotenv

# Load .env file (only needed if you want to store keys there)
load_dotenv()

# === Gemini Config ===
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"  # or "gemini-1.5", "gemini-2.0-pro", etc.

# === Embeddings Config ===
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# === Chroma Config ===
CHROMA_DIR = "chroma_db"

# === Data Paths ===
MANUALS_DIR = "data/manuals"
