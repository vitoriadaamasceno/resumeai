"""Extração de texto de páginas HTML com fallback para um navegador."""

import logging
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright


logger = logging.getLogger("uvicorn.error")

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

BLOCKED_STATUS_CODES = {401, 403, 407, 429, 503}
BLOCKED_MARKERS = (
    "access denied",
    "attention required! | cloudflare",
    "cf-chl-",
    "captcha",
    "checking your browser",
    "enable javascript and cookies to continue",
    "just a moment...",
    "request blocked",
    "verify you are human",
)


def clean_html(html: str) -> str:
    """Remove elementos não textuais e limita o texto devolvido."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "header", "footer", "nav", "form", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:1000])


def _is_blocked(html: str, status_code: int = 200) -> bool:
    """Identifica respostas HTTP e páginas de desafio/bloqueio comuns."""
    if status_code in BLOCKED_STATUS_CODES:
        return True

    sample = html[:100_000].lower()
    return any(marker in sample for marker in BLOCKED_MARKERS)


def _extract_valid_content(html: str, status_code: int = 200) -> Optional[str]:
    if not html or status_code >= 400 or _is_blocked(html, status_code):
        return None

    text = clean_html(html)
    return text if text.strip() else None


async def _fetch_with_httpx(url: str, timeout: int) -> Optional[str]:
    logger.info("[HTML reader] Tentando acessar via HTTPX: %s", url)
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
        ) as client:
            response = await client.get(url)

        content_type = response.headers.get("content-type", "").lower()
        if content_type and "html" not in content_type and "text/" not in content_type:
            logger.info("[HTML reader] HTTPX retornou conteúdo incompatível: %s", content_type)
            return None

        content = _extract_valid_content(response.text, response.status_code)
        if not content:
            logger.info(
                "[HTML reader] HTTPX retornou resposta vazia, inválida ou bloqueada "
                "para %s (status %s)",
                url,
                response.status_code,
            )
        return content
    except httpx.HTTPError as error:
        logger.warning("[HTML reader] HTTPX não conseguiu acessar %s: %s", url, error)
        return None


async def _fetch_with_playwright(url: str, timeout: int) -> Optional[str]:
    logger.info("[HTML reader] Tentando acessar via Playwright: %s", url)
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            try:
                page = await browser.new_page(user_agent=USER_AGENT)
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=timeout * 1000,
                )
                try:
                    await page.wait_for_load_state("networkidle", timeout=timeout * 1000)
                except PlaywrightTimeoutError:
                    logger.info(
                        "[HTML reader] Playwright detectou conexões ativas; "
                        "analisando o HTML: %s",
                        url,
                    )

                content = _extract_valid_content(await page.content())
                return content
            finally:
                await browser.close()
    except (PlaywrightTimeoutError, PlaywrightError) as error:
        logger.warning("[HTML reader] Playwright não conseguiu acessar %s: %s", url, error)
        return None


async def get_html(url: str, timeout: int = 10) -> Optional[str]:
    """Obtém texto via HTTPX e usa Playwright quando a resposta não é válida."""
    content = await _fetch_with_httpx(url, timeout)
    if content:
        logger.info("[HTML reader] Resolvido via HTTPX: %s", url)
        return content

    logger.info("[HTML reader] HTTPX não resolveu; acionando fallback Playwright: %s", url)
    content = await _fetch_with_playwright(url, timeout)
    if content:
        logger.info("[HTML reader] Resolvido via Playwright: %s", url)
    else:
        logger.error("[HTML reader] HTTPX e Playwright falharam para: %s", url)
    return content
