import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings   # you can keep using OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import AnthropicClaude
from langchain.chains import RetrievalQA

# 1) Load text
with open("combined_pdf_text.txt", "r", encoding="utf-8") as f:
    all_text = f.read()

# 2) Chunk the text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = splitter.split_text(all_text)

# 3) Create embeddings (we’re still using OpenAIEmbeddings here; Claude doesn’t offer its own embeddings API yet)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(docs, embeddings)

# 4) Build a RetrievalQA chain with Claude
claude = AnthropicClaude(model="claude-v1", temperature=0)  # or “claude-2” if available
qa_chain_claude = RetrievalQA.from_chain_type(
    llm=claude,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
)

def ask_claude(question: str) -> str:
    return qa_chain_claude.run(question)

if __name__ == "__main__":
    while True:
        q = input("Ask the Claude chatbot: ")
        print(ask_claude(q))