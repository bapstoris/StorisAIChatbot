from flask import Flask, render_template, request, jsonify
from langchain_community.chat_models import ChatOpenAI  # Use langchain_community, not langchain.chat_models
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence  # New pattern replacing LLMChain


# Load website content (used as part of the prompt)
with open('LaptopSetup_pdf_txt', 'r') as f:
    prompt = f.read()

# Construct prompt template
hotel_assistant_template = prompt + """
You are the hotel manager of Landon Hotel, named "Mr. Landon".
Your expertise is exclusively in providing information and advice about anything related to Landon Hotel.
This includes any general Landon Hotel related queries.
You do not provide information outside of this scope.
If a question is not about Landon Hotel, respond with, "I can't assist you with that, sorry!"
Question: {question}
Answer:
"""

# Define the LangChain prompt object
hotel_assistant_prompt_template = PromptTemplate(
    input_variables=["question"],
    template=hotel_assistant_template
)

# Initialize the LLM
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

# Create the chain using the modern pipe syntax
llm_chain = hotel_assistant_prompt_template | llm

# Function to query the model
def query_llm(question):
    response = llm_chain.invoke({'question': question})
    return response.content

# Simple CLI loop
while True:
    user_question = input("Ask me about Landon Hotel: ")
    query_llm(user_question)

app = Flask(__name__) 

@app.route("/") 
def index(): 
    return render_template("index.html") 

@app.route("/chatbot", methods=["POST"]) 
def chatbot(): 
    data = request.get_json() 
    question = data["question"] 
    response = query_llm(question) 
    return jsonify({"response": response}) 

if __name__ == "__main__": 
    app.run(debug=True)