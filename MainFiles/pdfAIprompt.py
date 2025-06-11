def build_prompt(question: str, context: str) -> str:
    persona = (
        "You are StorisAI name Tallulah, an expert on all things Storis. "
        "Answer user questions based solely on the PDF content and your domain knowledge."
    )
    return f"{persona}\n\nContext:\n{context}\n\nUser asks: {question}\nAnswer:"
