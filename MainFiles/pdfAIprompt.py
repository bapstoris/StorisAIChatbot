def build_prompt(question: str, context: str) -> str:
    persona = (
        "No policy numbers and no names of departments or employees please"
    )
    return f"{persona}\n\nContext:\n{context}\n\nUser asks: {question}\nAnswer:"
