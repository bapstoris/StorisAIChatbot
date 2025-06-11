import os
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Load and prepare vectorstore at module load (app startup)
with open('combined_pdf_text.txt', 'r', encoding='utf-8') as f:
    all_text = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_text(all_text)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(docs, embedding=embeddings)

def get_relevant_context(question: str, k: int = 4) -> str:
    relevant_docs = vectorstore.similarity_search(question, k=k)
    return "\n\n".join([doc.page_content for doc in relevant_docs])

def get_answer(prompt: str) -> str:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()
