def build_prompt(question: str) -> str:
    with open('combined_pdf_text.txt', 'r', encoding='utf-8') as f:
        docs = f.read()
    persona = ( #change storis ai personality
        "You are StorisAI name Tallulah, an expert on all things Storis. "
        "Answer user questions based solely on the PDF content and your domain knowledge."
    )
    return f"{persona}\n\nContext:\n{docs}\n\nUser asks: {question}\nAnswer:"
