import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.data_source_loader import load_all_sources
from src.vector_store import VectorStore
from src.content_generator import ContentGenerator

print("Testing data source loader...")
try:
    topics = load_all_sources()
    print(f"Loaded {len(topics)} topics.")
    
    print("Testing VectorStore init...")
    vs = VectorStore()
    print("VectorStore initialized.")
    
    print("Testing ContentGenerator init...")
    cg = ContentGenerator()
    print("ContentGenerator initialized.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
