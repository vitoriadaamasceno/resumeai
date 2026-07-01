from enum import Enum
from fastapi import File, UploadFile
from pydantic import BaseModel


class LlmModel(Enum):
    T5 = "t5"
    GPT = "gpt"


class VideoRequest(BaseModel):
    url: str


class HtmlInput(BaseModel):
    url: str


class PDFRequest(BaseModel):
    file: UploadFile = File(...)
