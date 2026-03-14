from typing import List, Dict
import chromadb
from chromadb.config import Settings
import config
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba


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
        self._vectorizer = TfidfVectorizer(max_features=512)
        self._doc_count = 0
        self._init_collection()
    
    def _init_collection(self):
        try:
            self.client.delete_collection(name=self.collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Blog content vectors for deduplication"}
        )
    
    def _tokenize(self, text: str) -> str:
        words = jieba.cut(text)
        return " ".join(words)
    
    def _embed_text(self, texts: List[str], fit: bool = False) -> List[List[float]]:
        processed = [self._tokenize(t) for t in texts]
        
        if fit:
            self._vectorizer.fit(processed)
        
        matrix = self._vectorizer.transform(processed)
        vectors = matrix.toarray().tolist()
        
        self._doc_count += len(texts)
        return vectors
    
    def add_documents(self, ids: List[str], documents: List[str], metadatas: List[dict]):
        embeddings = self._embed_text(documents, fit=(self._doc_count == 0))
        
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
    
    def search(self, query: str, n_results: int = 5):
        query_embedding = self._embed_text([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding,
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
        except:
            return []
    
    def delete_collection(self):
        self.client.delete_collection(name=self.collection_name)
