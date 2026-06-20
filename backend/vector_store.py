import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="memories"
)

conversation_collection = (
    client.get_or_create_collection(
        name="conversations"
    )
)
summary_collection = (
    client.get_or_create_collection(
        name="summaries"
    )
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

def save_conversation_embedding(
    conversation_id,
    text
):

    embedding = model.encode(
        text
    ).tolist()

    try:

        conversation_collection.add(
            ids=[str(conversation_id)],
            documents=[text],
            embeddings=[embedding]
        )

    except:
        pass


def search_conversations(
    query,
    top_k=5
):

    embedding = model.encode(
        query
    ).tolist()

    results = (
        conversation_collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
    )

    return results["documents"][0]


def build_hybrid_context(
    query
):

    memories = search_memories(
        query,
        top_k=3
    )

    conversations = (
        search_conversations(
            query,
            top_k=3
        )
    )

    return (
        "MEMORIES:\n"
        + "\n".join(memories)
        + "\n\nCONVERSATIONS:\n"
        + "\n".join(conversations)
    )

def save_summary_embedding(
    summary_id,
    text
):

    embedding = model.encode(
        text
    ).tolist()

    summary_collection.add(
        ids=[str(summary_id)],
        documents=[text],
        embeddings=[embedding]
    )

def search_summaries(
    query,
    top_k=3
):

    embedding = model.encode(
        query
    ).tolist()

    results = (
        summary_collection.query(
            query_embeddings=[
                embedding
            ],
            n_results=top_k
        )
    )

    return results["documents"][0]