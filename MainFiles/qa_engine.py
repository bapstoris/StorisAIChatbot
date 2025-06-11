# qa_engine.py
import os
import openai

# pick up your API key however you like
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_answer(prompt: str) -> str:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()
