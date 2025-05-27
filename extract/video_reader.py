from functools import lru_cache
import logging
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def format_text(transcript) -> str:
    return " ".join([item['text'] for item in transcript])


@lru_cache(maxsize=30)
def get_video_transcript(id_url: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id_url, languages=['pt'])
        transcript = format_text(transcript)
        return transcript
    except TranscriptsDisabled:
        raise ValueError("Transcrição desativada para este vídeo.")
    except Exception as e:
        logging.error(f"Erro ao obter a transcrição do vídeo: {e}")
        raise ValueError(f"Erro ao obter a transcrição do vídeo: {e}")

    