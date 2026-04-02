import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "_code"))

import config
from src.content_generator import ContentGenerator

print(f"Model: {config.VOLCENGINE_LLM_MODEL}")
print(f"Base: {config.VOLCENGINE_LLM_API_BASE}")

try:
    generator = ContentGenerator()
    response = generator.generate("Hello, are you working?", lang="en")
    print(f"Success: {response[:50]}...")
except Exception as e:
    print(f"Failed: {e}")
