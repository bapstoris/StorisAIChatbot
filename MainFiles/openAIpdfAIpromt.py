import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 1) Load combined text (all PDFs)
with open("combined_pdf_text.txt", "r", encoding="utf-8") as f:
    all_text = f.read()

# 2) Chunk the text into ~1,000‐token passages
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
docs = splitter.split_text(all_text)
# `docs` is a list of strings, each ~1k chars (not tokens, but this works in practice).

# 3) Create embeddings for each chunk
embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY
vectorstore = FAISS.from_texts(
    texts=docs,
    embedding=embeddings
)

# (Optional) Persist FAISS to disk
vectorstore.save_local("faiss_index_openai")

# 4) Build a RetrievalQA chain with GPT-3.5 (or GPT-4)
#    - Set temperature=0 for deterministic answers if you like.
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",         # “stuff” will stuff top passages directly in one prompt.
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=False
)

# 5) Example usage
def ask_openai(question: str) -> str:
    result = qa_chain.run(question)
    return result

if __name__ == "__main__":
    while True:
        q = input("Ask a question about the PDFs: ")
        answer = ask_openai(q)
        print("→", answer)
