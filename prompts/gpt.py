from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_GPT = os.getenv("API_KEY_GPT")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=API_KEY_GPT,
    temperature=0,
)


def gerar_resumo(texto):
    """
    Gera um resumo do texto usando o modelo GPT-3.5 Turbo.
    
    Args:
        texto (str): Texto a ser resumido em tópicos.
    
    Returns:
        str: Resumo do texto.
    """
 
    prompt = f"Resuma este texto em tópicos simplificados: {texto}"
    
    resposta = llm.invoke(prompt)
    
    return resposta.content
