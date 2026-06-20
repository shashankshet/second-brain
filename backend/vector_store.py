import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="memories"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def save_memory_embedding(memory_id, text):

    embedding = model.encode(text).tolist()

    try:
        collection.add(
            ids=[str(memory_id)],
            documents=[text],
            embeddings=[embedding]
        )
    except:
        pass


def search_memories(query, top_k=5):

    embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results["documents"][0]


def build_relevant_context(query):

    memories = search_memories(query)

    return "\n".join(memories)