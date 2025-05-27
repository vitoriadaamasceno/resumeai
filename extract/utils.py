import re


def extract_id_video(url: str) -> str | None:

    match = re.search(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        return None
    video_id = match.group(1)
    return video_id


