from fastapi import FastAPI


app = FastAPI(title='Resume Aê', description='API para resumir textos com IA', version='1.0.0')


@app.get("/summarize")
def summarize(text: str, type: str):
    """
    Resumir um texto usando IA

    Args:
        text (str): Texto a ser resumido
        type (str): Tipo de entrada (PDF, VIDEO, HTML)
    """

    if type == "PDF":
        # Resumir PDF
        pass
    elif type == "VIDEO":
        # Resumir VIDEO
        pass
    elif type == "HTML":
        # Resumir HTML
        pass
    else:
        return {"message": "Tipo de entrada inválido"}

    return {"message": "Texto resumido com sucesso"}