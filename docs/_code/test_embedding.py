import sys
from pathlib import Path
import requests

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config


def test_embedding():
    endpoint = "https://ark.cn-beijing.volces.com/api/v3/embeddings"
    model = "doubao-embedding-large-text-250515"

    text = "This is a test sentence for embedding."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.VOLCENGINE_EMBEDDING_API_KEY}",
    }

    data = {
        "model": model,
        "input": text,
    }

    try:
        print(f"Testing Endpoint: {endpoint}")
        print(f"Testing Embedding with Model: {model}")
        print("Sending request...")
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)

        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error Response: {response.text}")
            return False

        result = response.json()
        print("Response structure keys:", result.keys())

        if 'data' in result:
            print("Data type:", type(result['data']))
            if isinstance(result['data'], list):
                print("Data length:", len(result['data']))
                if len(result['data']) > 0:
                    first_item = result['data'][0]
                    print("First item keys:", first_item.keys())
                    if 'embedding' in first_item:
                        emb = first_item['embedding']
                        print(f"Embedding length: {len(emb)}")
                        print("Embedding sample:", emb[:5])
                        print("Selected endpoint:", endpoint)
                        print("Selected model:", model)
                        return True
            elif isinstance(result['data'], dict):
                print("Data keys:", result['data'].keys())
                if 'embedding' in result['data']:
                    emb = result['data']['embedding']
                    print(f"Embedding length: {len(emb)}")
                    print("Embedding sample:", emb[:5])
                    print("Selected endpoint:", endpoint)
                    print("Selected model:", model)
                    return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

    print("No embedding vector found in response.")
    return False

if __name__ == "__main__":
    test_embedding()
