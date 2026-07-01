import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from extract.pdf_reader import get_pdf_text
from extract.html_reader import get_html
from extract.video_reader import get_video_transcript, extract_id_video
from services.summarize import summarize
from schema import LlmModel, VideoRequest, HtmlInput, PDFRequest


app = FastAPI(title='Resume Ai', description='API para resumir textos com IA', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://*",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Resumo com IA!"}


@app.post("/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...), model: LlmModel = LlmModel.T5.value):
    if file.content_type != "application/pdf":
        logging.error("O arquivo enviado não é um PDF.")
        return JSONResponse(content={"error": "O arquivo deve ser um PDF."}, status_code=400)
    try:
        contents = await file.read()
        texto_pdf = get_pdf_text(contents)
        resumo = summarize(texto_pdf, model)
        return {"resumo": resumo}
    except FileNotFoundError:
        logging.error("Arquivo PDF não encontrado.")
        return JSONResponse(content={"error": "Arquivo PDF não encontrado."}, status_code=404)
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo PDF: {e}")
        return JSONResponse(content={"error": "Erro ao processar o arquivo PDF."}, status_code=500)
    

@app.post("/summarize/video")
def summarize_video(request: VideoRequest, model: LlmModel = LlmModel.T5.value):
    url = request.url
    id_video = extract_id_video(url)
    if not id_video:
        logging.error("URL inválida, não foi possível extrair o ID do vídeo.")
        return JSONResponse(content={"error": "URL inválida"}, status_code=400)
    try:
        logging.info(f"ID do vídeo extraído: {id_video}")
        video_transcript = get_video_transcript(id_video)
        resumo = summarize(video_transcript, model)
        return {"resumo": resumo}
    except ValueError as e:
        logging.error(f"Erro ao obter a transcrição do vídeo: {e}")
        return JSONResponse(content={"error": "Erro ao obter transcrição do vídeo"}, status_code=400)
    except Exception as e:
        logging.error(f"Erro ao processar o vídeo: {e}")
        return JSONResponse(content={"error": "Erro ao processar o vídeo."}, status_code=500)
    

@app.post("/summarize/html")
async def summarize_html(url_body: HtmlInput, model: LlmModel = LlmModel.T5.value):
    url = url_body.url
    if not url:
        logging.error("URL não fornecida.")
        return JSONResponse(content={"error": "URL não fornecida."}, status_code=400)
    try:
        html_content = await get_html(url)
        if not html_content:
            logging.error("Não foi possível obter o conteúdo HTML.")
            return JSONResponse(content={"error": "Não foi possível obter o conteúdo HTML."}, status_code=404)
     
        resumo = summarize(html_content, model)

        return {"resumo": resumo}
    except Exception as e:
        logging.error(f"Erro ao processar o HTML: {e}")
        return JSONResponse(content={"error": "Erro ao processar o HTML."}, status_code=500)