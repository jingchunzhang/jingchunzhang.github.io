from typing import List, Dict
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
import config


def get_local_embedding(texts: List[str]) -> List[List[float]]:
    """使用本地 ONNXMiniLM_L6_V2 模型生成 embeddings"""
    ef = ONNXMiniLM_L6_V2()
    return ef(texts)


class VectorStore:
    def __init__(self, persist_dir: str = None):
        if persist_dir is None:
            persist_dir = "./chroma_data"
        
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        self.collection_name = config.CHROMA_COLLECTION
        self.embedding_function = ONNXMiniLM_L6_V2()
        self._init_collection()
    
    def _init_collection(self):
        try:
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        except Exception:
            # 如果 collection 已存在且 embedding function 不兼容，则删除重建
            try:
                self.client.delete_collection(name=self.collection_name)
            except Exception:
                pass
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Blog content vectors for deduplication"}
            )
    
    def _embed_text(self, texts: List[str]) -> List[List[float]]:
        return get_local_embedding(texts)
    
    def add_documents(self, ids: List[str], documents: List[str], metadatas: List[dict]):
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
    
    def search(self, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    def check_similarity(self, text: str) -> float:
        results = self.search(text, n_results=1)
        if results and results['documents'] and results['documents'][0]:
            if results['distances'] and results['distances'][0]:
                distance = results['distances'][0][0]
                similarity = 1 - distance
                return similarity
        return 0.0
    
    def find_similar_for_linking(self, text: str, min_sim: float = 0.4) -> List[dict]:
        results = self.search(text, n_results=10)
        similar_articles = []
        
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                distance = results['distances'][0][i]
                similarity = 1 - distance
                
                if min_sim <= similarity < config.SIMILARITY_THRESHOLD:
                    similar_articles.append({
                        'id': results['ids'][0][i],
                        'similarity': similarity,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                    })
        
        return similar_articles
    
    def get_all_documents(self, limit: int = 1000) -> List[dict]:
        try:
            result = self.collection.get(limit=limit)
            return result.get('metadatas', [])
        except Exception:
            return []
    
    def delete_collection(self):
        self.client.delete_collection(name=self.collection_name)
