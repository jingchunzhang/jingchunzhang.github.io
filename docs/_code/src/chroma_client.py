import chroma
from chroma.errors import ChromaConnectionError
import config

def get_chroma_client():
    """获取 ChromaDB 客户端"""
    try:
        client = chroma.Client(
            http_config={"host": config.CHROMA_HOST, "port": 8000}
        )
        return client
    except ChromaConnectionError as e:
        raise Exception(f"无法连接到 ChromaDB: {e}")

def get_or_create_collection(client, name=None):
    """获取或创建 collection"""
    collection_name = name or config.CHROMA_COLLECTION
    try:
        collection = client.get_collection(name=collection_name)
    except:
        collection = client.create_collection(name=collection_name)
    return collection

def test_connection():
    """测试 ChromaDB 连接"""
    client = get_chroma_client()
    client.heartbeat()
    return True
