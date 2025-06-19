# qa_engine.py

import os
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

openai.api_key = os.getenv("OPENAI_API_KEY")

# Lazily-loaded global to avoid hitting API on import
_vectorstore = None

def _load_vectorstore():
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    # Use path relative to this file
    base = os.path.dirname(__file__)
    file_path = os.path.join(base, 'combined_pdf_text.txt')

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        all_text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_text(all_text)

    embeddings = OpenAIEmbeddings()
    _vectorstore = FAISS.from_texts(docs, embedding=embeddings)

    return _vectorstore

def get_relevant_context(question: str, k: int = 4) -> str:
    vectorstore = _load_vectorstore()
    relevant_docs = vectorstore.similarity_search(question, k=k)
    return "\n\n".join([doc.page_content for doc in relevant_docs])

def get_answer(prompt: str) -> str:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()
