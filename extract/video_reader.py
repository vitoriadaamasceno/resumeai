from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from utils import extract_id_video


def format_text(transcript: dict) -> str:
    return " ".join([item['text'] for item in transcript])


def get_video_transcript(url: str) -> str:

    video_id = extract_id_video(url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
        transcript = format_text(transcript)
        return transcript
    except TranscriptsDisabled:
        raise ValueError("Transcrição desativada para este vídeo.")

    