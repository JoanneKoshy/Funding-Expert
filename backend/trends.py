import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.llm import ask_gemini

DATA_DIR = "data/funding"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_funding_trends(question: str) -> str:
    documents = []

    # Load trend documents
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, file))
            documents.extend(loader.load())

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # Create temporary vector DB
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # Retrieve context
    retrieved_docs = vectordb.similarity_search(question, k=4)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Hybrid reasoning prompt
    prompt = f"""
    You are an AI analyst summarizing startup funding trends in India.

    Use the data below as grounding.
    If the data is partial, use informed reasoning
    based on known market patterns.

    DATA:
    {context}

    QUESTION:
    {question}

    Provide:
    - Key trends
    - Sector-level insights
    - Stage-wise observations
    - Practical takeaways for founders

    Keep it concise and actionable.
    """

    return ask_gemini(prompt)
