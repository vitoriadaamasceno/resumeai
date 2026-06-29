import logging
from functools import lru_cache

from transformers import T5ForConditionalGeneration, T5Tokenizer


model_name = "unicamp-dl/ptt5-base-portuguese-vocab"

tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def montar_prompt_t5(texto: str) -> str:
    return f"""
summarize: Create a clear and concise summary of the following text.
Focus only on the most important information.
Do not add information that is not present in the text.
Preserve relevant names, dates, numbers and technical terms.

Text:
{texto}
"""


@lru_cache(maxsize=30)
def gerar_resumo_t5(texto):
    """
    Gera um resumo do texto usando o modelo T5 da Hugging Face.

    Args:
        texto (str): Texto a ser resumido.

    Returns:
        str: Resumo do texto ou mensagem de erro.
    """
    try:
        prompt = montar_prompt_t5(texto)

        input_ids = tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True,
        ).input_ids

        output = model.generate(
            input_ids,
            max_length=180,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )

        resumo = tokenizer.decode(output[0], skip_special_tokens=True)
        return resumo

    except Exception as e:
        logging.error(f"Erro ao gerar resumo com T5: {e}")
        return f"Erro ao gerar resumo: {str(e)}"