import re
from bs4 import BeautifulSoup as bs


def extract_id_video(url: str) -> str | None:

    match = re.search(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        return None
    video_id = match.group(1)
    return video_id


def limpar_html_para_resumo(html: str) -> str:
    soup = bs(html, "html.parser")

    for tag in soup(["script", "style", "header", "footer", "nav", "form", "noscript"]):
        tag.decompose()

    texto = soup.get_text(separator="\n", strip=True)

    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    return "\n".join(linhas[:1000])