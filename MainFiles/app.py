# app.py

import os
from flask import Flask, request, jsonify, render_template
import traceback

# Toggle this to False once you're ready to hit the real LLM/RAG
USE_MOCK = False

app = Flask(__name__, static_folder='static', template_folder='templates')

# Import prompt builder (always safe)
from pdfAIprompt import build_prompt

# Only import heavy modules if not mocking (avoids API calls on import)
if not USE_MOCK:
    from qa_engine import get_answer, get_relevant_context
    # Optionally, initialize your vectorstore or other RAG components here

@app.route('/')
def index():
    return render_template('test.html')  # Update if using a different template


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'response': 'Please ask a question.'}), 400

    if USE_MOCK:
        return jsonify({'response': f"[Mock reply] You asked: {question}"})

    try:
        context = get_relevant_context(question)
        prompt = build_prompt(question, context)
        answer = get_answer(prompt)
        return jsonify({'response': answer})
    except Exception as e:
        print("Exception in /chatbot endpoint:")
        traceback.print_exc()
        return jsonify({'response': f"Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
