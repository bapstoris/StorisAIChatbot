# app.py

import os
from flask import Flask, request, jsonify, render_template

# Toggle this to False once you're ready to hit the real LLM/RAG
USE_MOCK = True

# Import your prompt-builder and LLM wrapper
from pdfAIprompt import build_prompt
from qa_engine import get_answer
from qa_engine import get_relevant_context

# If you're doing RAG locally (vectorstore + chain), import/setup here
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

app = Flask(__name__, static_folder='static', template_folder='templates')


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

    context = get_relevant_context(question)
    # Build the full prompt (persona + PDF context + user question)
    prompt = build_prompt(question, context)

    # If you want pure RAG via langchain:
    # answer = qa_chain.run(question)

    # Otherwise, send the wrapped prompt to your qa_engine
    answer = get_answer(prompt)

    return jsonify({'response': answer})


if __name__ == '__main__':
    # In production you might set host='0.0.0.0' and grab PORT from env
    app.run(debug=True)
