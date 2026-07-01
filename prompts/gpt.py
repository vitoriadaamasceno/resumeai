import logging
from config import OPENAI_API_KEY as api_key
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def get_llm():
    if not api_key:
        logging.warning("Chave da OpenAI não configurada.")
        return None

    return ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=api_key,
        temperature=0,
    )


def generate_summary_gpt(texto):
    try:
        llm = get_llm()

        if llm is None:
            return "Resumo indisponível no momento. A chave da OpenAI não foi configurada."

        mensagens = [
            SystemMessage(
                content="""
                Você é um assistente especializado em resumir textos de forma clara, objetiva e fiel ao conteúdo original.
                Seu objetivo é transformar textos longos em tópicos simples, bem organizados e fáceis de entender.
                Não invente informações. Preserve dados importantes como nomes, datas, números e termos técnicos.
                """
            ),
            HumanMessage(
                content=f"""
            Resuma o texto abaixo em tópicos simplificados.

            Regras:
            - Use linguagem simples e direta.
            - Destaque apenas as informações mais importantes.
            - Organize o conteúdo em tópicos com marcadores.
            - Agrupe ideias relacionadas.
            - Evite repetições.
            - Não adicione opiniões ou informações externas.
            - Se houver ações, decisões ou conclusões, destaque-as claramente.

            Texto:
            \"\"\"
            {texto}
            \"\"\"
            """
            ),
        ]

        resposta = llm.invoke(mensagens)
        logging.info("Resposta do GPT recebida com sucesso.")
        return resposta.content

    except Exception as e:
        logging.error(f"Erro ao gerar resumo com GPT: {e}")
        return f"Erro ao gerar resumo: {str(e)}"