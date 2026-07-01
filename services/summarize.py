from schema import LlmModel
from prompts.gpt import generate_summary_gpt
from prompts.t5 import generate_summary_t5


def summarize(text: str, model: LlmModel) -> str:
    strategy = {LlmModel.GPT: generate_summary_gpt, LlmModel.T5: generate_summary_t5}
    return strategy[model](text)
