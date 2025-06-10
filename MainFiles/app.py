# flask web application to power chatbot on html page.
USE_MOCK = True #for testing mock only
from flask import Flask, request, jsonify, render_template
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load and prepare embeddings and vector store at startup
# 1) Load combined text
with open('combined_pdf_text.txt', 'r', encoding='utf-8') as f:
    all_text = f.read()
# 2) Chunk text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
docs = splitter.split_text(all_text)
# 3) Create embeddings & FAISS index
if not USE_MOCK:
    embeddings = OpenAIEmbeddings() 
    vectorstore = FAISS.from_texts(texts=docs, embedding=embeddings) 
    # Optionally load existing index: vectorstore = FAISS.load_local('faiss_index_openai', embeddings)

    # 4) Create QA chain
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=vectorstore.as_retriever(search_kwargs={'k': 4}),
        return_source_documents=False
    )

@app.route('/')
def index():
    # Serve the chatbot HTML page
    return render_template('test.html')

#@app.route('/chatbot', methods=['POST'])
'''def chatbot():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'response': 'Please ask a question.'})

    # Run the QA chain
    answer = qa_chain.run(question)
    return jsonify({'response': answer})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)'''

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'response': 'Please ask a question.'})
    
    if USE_MOCK:
        mock_response = f"[Mock reply] You asked: {question}"
        return jsonify({"response": mock_response})
    else:
        answer = qa_chain.run(question)
        return jsonify({'response': answer})
    
if __name__ == '__main__':
    app.run(debug=True)