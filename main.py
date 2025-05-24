from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import JSONResponse
from extract.pdf_reader import get_pdf_text
from extract.video_reader import get_video_transcript
from extract.utils import extract_id_video
from prompts.t5 import gerar_resumo_t5
from prompts.gpt import gerar_resumo_gpt

import logging


app = FastAPI(title='Resume Ai', description='API para resumir textos com IA', version='1.0.0')


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Resumo com IA!"}


@app.post("/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...), model="t5"):
    if file.content_type != "application/pdf":
        logging.error("O arquivo enviado não é um PDF.")
        return JSONResponse(content={"error": "O arquivo deve ser um PDF."}, status_code=400)
    try:
        contents = await file.read()
        texto_pdf = get_pdf_text(contents)
        if model == "gpt":
            resumo = gerar_resumo_gpt(texto_pdf)
        else:
            resumo = gerar_resumo_t5(texto_pdf)

        return {"resumo": resumo}
    except FileNotFoundError:
        logging.error("Arquivo PDF não encontrado.")
        return JSONResponse(content={"error": "Arquivo PDF não encontrado."}, status_code=404)
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo PDF: {e}")
        return JSONResponse(content={"error": "Erro ao processar o arquivo PDF."}, status_code=500)
    

@app.post("/summarize/video")
def summize_video(url : str = Body(...), model="t5"):
    id_video = extract_id_video(url)
    if not id_video:
        logging.error("URL invalida")
        return JSONResponse(content={"error": "URL inválida"}, status_code=400)
    try:
        logging.info(f"ID do vídeo extraído: {id_video}")
        video_transcript = get_video_transcript(id_video)
        
        if model == "gpt":
            resumo = gerar_resumo_gpt(video_transcript)
        else:
            resumo = gerar_resumo_t5(video_transcript)
        return {"resumo": resumo}
    except ValueError as e:
        logging.error(f"Erro ao obter a transcrição do vídeo: {e}")
        return JSONResponse(content={"error": "Erro ao obter transcrição do vídeo: " + str(e)}, status_code=400)
    except Exception as e:
        logging.error(f"Erro ao processar o vídeo: {e}")
        return JSONResponse(content={"error": "Erro ao processar o vídeo.Erro:" + str(e)}, status_code=500)
    