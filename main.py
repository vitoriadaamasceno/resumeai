from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from extract.pdf_reader import get_pdf_text
from prompts.t5 import gerar_resumo_t5
from prompts.gpt import gerar_resumo_gpt

import logging


app = FastAPI(title='Resume Ai', description='API para resumir textos com IA', version='1.0.0')


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Resumo com IA!"}


@app.post("/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...), ia="t5"):
    if file.content_type != "application/pdf":
        logging.error("O arquivo enviado não é um PDF.")
        return JSONResponse(content={"error": "O arquivo deve ser um PDF."}, status_code=400)
    try:
        contents = await file.read()
        texto_pdf = get_pdf_text(contents)
        if ia == "gpt":
            resumo = gerar_resumo_gpt(texto_pdf)
        else:
            resumo = gerar_resumo_t5(texto_pdf)

        return resumo

    except Exception as e:
        logging.error(f"Erro ao processar o arquivo PDF: {e}")
        return JSONResponse(content={"error": "Erro ao processar o arquivo PDF."}, status_code=500)
    