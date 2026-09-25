import os
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


PDF_PATH = "documents/Apple_2022_Annual_Report.pdf"
CHROMA_PATH = "chroma_db"

# Local embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def extract_text_from_pdf():
    reader = PdfReader(PDF_PATH)

    pages = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    return pages


def split_text(text, chunk_size=1000, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_vector_database():
    pages = extract_text_from_pdf()

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="financial_documents"
    )

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    counter = 0

    for page in pages:

        chunks = split_text(page["text"])

        for chunk in chunks:

            embedding = embedding_model.encode(
                chunk
            ).tolist()

            documents.append(chunk)
            embeddings.append(embedding)

            metadatas.append({
                "source": "Apple 2022 Annual Report",
                "page": page["page"]
            })

            ids.append(
                f"chunk_{counter}"
            )

            counter += 1

    if documents:

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    return collection


def search_documents(question, top_k=3):

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="financial_documents"
    )

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results