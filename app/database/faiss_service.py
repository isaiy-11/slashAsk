import faiss
import numpy as np


def create_faiss_index(embeddings):

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index


def save_index(
    index,
    index_path
):

    faiss.write_index(
        index,
        index_path
    )


def load_index(
    index_path
):

    return faiss.read_index(
        index_path
    )
def search_index(
    index,
    query_embedding,
    top_k=3
):

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return indices
def add_embeddings_to_index(
    index,
    embeddings
):

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    index.add(embeddings)

    return index