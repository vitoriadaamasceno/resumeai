import re


def extract_id_video(url: str) -> str:

    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("URL inválido")
    video_id = match.group(1)
    return video_id


