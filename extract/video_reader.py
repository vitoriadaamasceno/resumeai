import logging
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re


def format_text(transcript) -> str:
    texts = []

    for item in transcript:
        if isinstance(item, dict):
            texts.append(item.get("text", ""))
        else:
            texts.append(getattr(item, "text", ""))

    return " ".join(texts).strip()


def extract_id_video(url: str) -> str | None:

    match = re.search(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        return None
    video_id = match.group(1)
    return video_id


def get_video_transcript(id_url: str):
    try:
        ytt_api = YouTubeTranscriptApi()
        result = ytt_api.fetch(id_url, languages=['pt'])
        formatted_transcript = format_text(result)
        logging.info(f"Transcrição do vídeo obtida com sucesso., id_url: {id_url}")
        return formatted_transcript
    except TranscriptsDisabled:
        raise ValueError("Transcrição desativada para este vídeo.")
    except Exception as e:
        logging.error(f"Erro ao obter a transcrição do vídeo: {e}")
        raise ValueError(f"Erro ao obter a transcrição do vídeo: {e}")

    