import logging
import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

API_KEY_GPT = os.getenv("API_KEY_GPT")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=API_KEY_GPT,
    temperature=0,
)


@lru_cache(maxsize=30)
def gerar_resumo_gpt(texto):
    """
    Gera um resumo do texto usando o modelo GPT-3.5 Turbo.
    
    Args:
        texto (str): Texto a ser resumido em tópicos.
    
    Returns:
        str: Resumo do texto ou mensagem de erro.
    """
    try:
        prompt = f"Resuma este texto em tópicos simplificados: {texto}"
        resposta = llm.invoke(prompt)
        logging.info("Resposta do GPT")
        return resposta.content
    except Exception as e:
        logging.error(f"Erro ao gerar resumo com GPT: {e}")
        return f"Erro ao gerar resumo: {str(e)}"
