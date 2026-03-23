import argparse
import math
from pathlib import Path
from typing import List, Tuple

import requests

import config


def load_markdown_files(root: Path) -> List[Path]:
    return sorted(root.rglob("*.md"))


def read_markdown_text(path: Path, max_chars: int) -> str:
    content = path.read_text(encoding="utf-8", errors="ignore")
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            content = content[end + 5 :]
    content = " ".join(content.split())
    if len(content) > max_chars:
        content = content[:max_chars]
    return content


def get_embedding(text: str) -> List[float]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.VOLCENGINE_EMBEDDING_API_KEY}",
    }
    payload = {
        "model": config.VOLCENGINE_EMBEDDING_MODEL,
        "input": [{"type": "text", "text": text}],
    }
    response = requests.post(
        config.VOLCENGINE_EMBEDDING_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    vector_data = data.get("data")
    if isinstance(vector_data, dict) and "embedding" in vector_data:
        return vector_data["embedding"]
    if isinstance(vector_data, list) and vector_data and "embedding" in vector_data[0]:
        return vector_data[0]["embedding"]
    raise ValueError(f"Unexpected embedding response: {data}")


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b):
        dot += x * y
        norm_a += x * x
        norm_b += y * y
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def find_duplicates(
    files: List[Path],
    vectors: List[List[float]],
    threshold: float,
) -> List[Tuple[str, str, float]]:
    hits: List[Tuple[str, str, float]] = []
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            sim = cosine_similarity(vectors[i], vectors[j])
            if sim >= threshold:
                hits.append((str(files[i]), str(files[j]), sim))
    hits.sort(key=lambda item: item[2], reverse=True)
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.9)
    parser.add_argument("--max-chars", type=int, default=8000)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    blog_root = Path(config.BLOG_SOURCE_DIR)
    files = load_markdown_files(blog_root)
    if not files:
        print("No markdown files found.")
        return

    vectors: List[List[float]] = []
    valid_files: List[Path] = []

    print(f"Embedding files: {len(files)}")
    for idx, path in enumerate(files, start=1):
        text = read_markdown_text(path, args.max_chars)
        if not text:
            continue
        try:
            emb = get_embedding(text)
            vectors.append(emb)
            valid_files.append(path)
            print(f"[{idx}/{len(files)}] OK {path}")
        except Exception as exc:
            print(f"[{idx}/{len(files)}] FAIL {path} :: {exc}")

    print(f"Embedded documents: {len(valid_files)}")
    pairs = find_duplicates(valid_files, vectors, args.threshold)

    if args.limit > 0:
        pairs = pairs[: args.limit]

    print("\nPotential duplicates:")
    if not pairs:
        print("None")
        return

    for file_a, file_b, score in pairs:
        print(f"{score:.4f}\t{file_a}\t{file_b}")


if __name__ == "__main__":
    main()
