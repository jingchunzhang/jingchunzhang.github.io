import sys
from pathlib import Path
import requests
import json

sys.path.insert(0, str(Path(__file__).parent))
import config

def list_models():
    print("Attempting to list models...")
    url = f"{config.VOLCENGINE_EMBEDDING_API_BASE}/models" # Assuming standard OpenAI compatible list endpoint
    headers = {
        "Authorization": f"Bearer {config.VOLCENGINE_EMBEDDING_API_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
