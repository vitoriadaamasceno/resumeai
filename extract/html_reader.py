from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from extract.utils import limpar_html_para_resumo
from bs4 import BeautifulSoup
import time, logging


async def get_html(url: str, timeout: int = 5) -> str:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(timeout)

        if driver.execute_script("return document.readyState") != "complete":
            driver.quit()
            return None

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        texto = limpar_html_para_resumo(soup.prettify())
        return texto if texto else None

    except Exception as e:
        logging.error(f"Erro ao ler HTML: {e}")
        return None
