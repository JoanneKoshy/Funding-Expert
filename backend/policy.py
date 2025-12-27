import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.llm import ask_gemini

# Embedding model (local, free)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def simplify_policy(pdf_file, user_question: str) -> str:
    """
    Perform RAG over an uploaded policy PDF and return simplified explanation
    """

    # 1️⃣ Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        pdf_path = tmp.name

    # 2️⃣ Load and split document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # 3️⃣ Create temporary vector store
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # 4️⃣ Retrieve relevant context
    retrieved_docs = vectordb.similarity_search(user_question, k=4)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # 5️⃣ LLM simplification prompt
    prompt = f"""
    You are an AI assistant helping founders understand government policies.

    Use the policy excerpts below to answer the question.
    If sections are complex, simplify them.
    Do NOT refuse to answer.

    POLICY EXCERPTS:
    {context}

    USER QUESTION:
    {user_question}

    Explain clearly, briefly, and in founder-friendly language.
    """

    return ask_gemini(prompt)
