from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

PDF_DIR = "data/manuals"

def ingest_pdfs():
    docs = []
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(PDF_DIR, file))
            docs.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(os.path.join(PDF_DIR, file), encoding="utf-8")
            docs.extend(loader.load())

    # Split docs
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    # Use HuggingFace free embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(split_docs, embedding=embeddings, persist_directory="chroma_db")

    print(f"Ingested {len(split_docs)} chunks into ChromaDB.")

if __name__ == "__main__":
    ingest_pdfs()
