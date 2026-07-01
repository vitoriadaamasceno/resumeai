import logging
from transformers import T5ForConditionalGeneration, T5Tokenizer


model_name = "recogna-nlp/ptt5-base-summ-xlsum"


def clean_text(texto: str) -> str:
    return " ".join(texto.split())


def generate_summary_t5(texto: str) -> str:
    """
    Gera um resumo do texto usando modelo T5 treinado para sumarização em PT-BR.
    """
    try:
        if not texto:
            return "Texto vazio. Não foi possível gerar resumo."

        prompt = clean_text(texto)
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
        )

        output = model.generate(
            inputs.input_ids,
            max_length=180,
            min_length=40,
            num_beams=4,
            length_penalty=1.0,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )

        resumo = tokenizer.decode(
            output[0],
            skip_special_tokens=True
        )

        return resumo.strip()

    except Exception as e:
        logging.error(f"Erro ao gerar resumo com T5: {e}")
        return f"Erro ao gerar resumo: {str(e)}"