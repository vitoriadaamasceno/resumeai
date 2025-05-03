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
        texto (str): Texto a ser resumido.
    
    Returns:
        str: Resumo do texto.
    """
 
    prompt = f"Resuma este texto em tópicos simplificados: {texto}"
    
    resposta = llm.invoke(prompt)
    
    return resposta.content


texto = """
A inteligência artificial (IA) é uma área da ciência da computação que enfatiza a criação de máquinas inteligentes que trabalham e reagem como seres humanos.
Algumas das atividades que os computadores com inteligência artificial são
projetados para fazer incluem: reconhecimento de fala, aprendizado, planejamento e resolução de problemas. A pesquisa associada à inteligência artificial é altamente técnica e especializada.Os principais problemas da inteligência artificial incluem programação de computadores para certos traços como conhecimento,
raciocínio, solução de problemas, percepção, aprendizado, planejamento, habilidade
de manipular e mover objetos.
"""

print("----------------------------------------------------")
print(gerar_resumo(texto))
