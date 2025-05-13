from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name) #carrega o tokenizador para o modelo T5
model = T5ForConditionalGeneration.from_pretrained(model_name)


def gerar_resumo(texto):
    """
    Gera um resumo do texto usando o modelo T5 da Hugging Face.
    O modelo T5 é um modelo de linguagem pré-treinado que pode ser ajustado para várias tarefas de NLP, incluindo resumo.
    
    Args:
        texto (str): Texto a ser resumido.
    
    Returns:
        str: Resumo do texto.
    """
    input_ids = tokenizer("summarize: " + texto, return_tensors="pt", max_length=512, truncation=True).input_ids #Prepares the input text for the T5 model by tokenizing and truncating it to the maximum length
    output = model.generate(input_ids, max_length=600, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True) #gera o resumo

    resumo = tokenizer.decode(output[0], skip_special_tokens=True)
    return resumo

