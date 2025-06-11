# app.py

import os
from flask import Flask, request, jsonify, render_template

# Toggle this to False once you're ready to hit the real LLM/RAG
USE_MOCK = True

# Import your prompt-builder and LLM wrapper
from pdfAIprompt import build_prompt
from qa_engine import get_answer

# If you're doing RAG locally (vectorstore + chain), import/setup here
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

app = Flask(__name__, static_folder='static', template_folder='templates')


# ---- Optional: RAG setup (only used if USE_MOCK is False and you want retrieval) ----
# Load & chunk your combined PDF text
with open('combined_pdf_text.txt', 'r', encoding='utf-8') as f:
    all_text = f.read()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
docs = splitter.split_text(all_text)

if not USE_MOCK:
    # 1) create embeddings & FAISS
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=docs, embedding=embeddings)

    # 2) wire up a RetrievalQA chain
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=vectorstore.as_retriever(search_kwargs={'k': 4}),
        return_source_documents=False
    )
# --------------------------------------------------------------------------------------


@app.route('/')
def index():
    return render_template('test.html')  # or 'index.html'—whatever you named it


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'response': 'Please ask a question.'}), 400

    if USE_MOCK:
        # Just echo back for local testing
        mock_response = f"[Mock reply] You asked: {question}"
        return jsonify({'response': mock_response})

    # Build the full prompt (persona + PDF context + user question)
    prompt = build_prompt(question)

    # If you want pure RAG via langchain:
    # answer = qa_chain.run(question)

    # Otherwise, send the wrapped prompt to your qa_engine
    answer = get_answer(prompt)

    return jsonify({'response': answer})


if __name__ == '__main__':
    # In production you might set host='0.0.0.0' and grab PORT from env
    app.run(debug=True)
