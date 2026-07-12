from enum import Enum
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class LlmModel(Enum):
    T5 = "t5"
    GPT = "gpt"


class VideoRequest(BaseModel):
    url: str


class HtmlInput(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None


class PDFRequest(BaseModel):
    file: UploadFile = File(...)
