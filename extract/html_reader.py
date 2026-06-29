import asyncio
import logging
import os
from typing import Optional

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from extract.utils import limpar_html_para_resumo


CHROME_BIN = os.getenv("CHROME_BIN", "/usr/bin/chromium")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")


async def get_html(url: str, timeout: int = 10) -> Optional[str]:
    def fetch_html() -> Optional[str]:
        driver = None

        try:
            options = Options()
            options.binary_location = CHROME_BIN

            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument(
                "--user-agent=Mozilla/5.0 "
                "(X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            service = Service(CHROMEDRIVER_PATH)

            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(timeout)

            driver.get(url)

            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            return driver.page_source

        except TimeoutException:
            logging.warning("Timeout ao carregar a página: %s", url)
            return None

        except WebDriverException as e:
            logging.exception("Erro do Selenium/ChromeDriver ao ler HTML: %s", e)
            return None

        except Exception as e:
            logging.exception("Erro inesperado ao ler HTML: %s", e)
            return None

        finally:
            if driver:
                driver.quit()

    html = await asyncio.to_thread(fetch_html)

    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    texto = limpar_html_para_resumo(soup.prettify())

    return texto if texto else None