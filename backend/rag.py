import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = "data/policies"
VECTOR_DB_DIR = "vector_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def ingest_documents():
    documents = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, file))
            docs = loader.load()
            documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    vectordb.persist()
    return vectordb


def load_vector_db():
    return Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )


def retrieve_context(query, k=4):
    db = load_vector_db()
    results = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])
