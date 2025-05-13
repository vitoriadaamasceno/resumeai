from fastapi import FastAPI


app = FastAPI(title='Resume Ai', description='API para resumir textos com IA', version='1.0.0')


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Resumo com IA!"}