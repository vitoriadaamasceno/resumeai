const API_BASE_URL = "http://localhost:8000";

const closePanelBtn = document.getElementById("closePanelBtn");

const summarizePageBtn = document.getElementById("summarizePageBtn");
const summarizeLinkBtn = document.getElementById("summarizeLinkBtn");
const summarizeVideoBtn = document.getElementById("summarizeVideoBtn");
const summarizePdfBtn = document.getElementById("summarizePdfBtn");


const linkInput = document.getElementById("linkInput");
const videoInput = document.getElementById("videoInput");
const pdfInput = document.getElementById("pdfInput");
const fileName = document.getElementById("fileName");

const loading = document.getElementById("loading");
const errorBox = document.getElementById("errorBox");
const resultBox = document.getElementById("resultBox");
const summaryContent = document.getElementById("summaryContent");
const copySummaryBtn = document.getElementById("copySummaryBtn");

function showLoading() {
  loading.classList.remove("hidden");
  errorBox.classList.add("hidden");
  resultBox.classList.add("hidden");
}

function hideLoading() {
  loading.classList.add("hidden");
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
  resultBox.classList.add("hidden");
}

function showResult(summary) {
  summaryContent.textContent = summary;
  resultBox.classList.remove("hidden");
  errorBox.classList.add("hidden");
}

function getSummaryFromResponse(data) {
  return (
    data.resumo ||
    "Resumo gerado, mas o backend não retornou o campo esperado."
  );
}

async function requestJson(url, options) {
  const response = await fetch(url, options);

  if (!response.ok) {
    throw new Error(`Erro HTTP: ${response.status}`);
  }

  return response.json();
}

async function getCurrentTab() {
  const tabs = await chrome.tabs.query({
    active: true,
    currentWindow: true,
  });

  return tabs[0];
}

async function getCurrentPageText() {
  const tab = await getCurrentTab();

  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      return {
        url: window.location.href,
        title: document.title,
        text: document.body.innerText,
      };
    },
  });

  return results[0].result;
}


closePanelBtn.addEventListener("click", () => {
  window.close();
});

pdfInput.addEventListener("change", () => {
  const file = pdfInput.files[0];

  if (file) {
    fileName.textContent = file.name;
  } else {
    fileName.textContent = "Nenhum arquivo selecionado";
  }
});

summarizePageBtn.addEventListener("click", async () => {
  try {
    showLoading();

    const pageData = await getCurrentPageText();

    const data = await requestJson(`${API_BASE_URL}/summarize/html?model=gpt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: pageData.url,
      }),
    });

    showResult(getSummaryFromResponse(data));
  } catch (error) {
    console.error(error);
    showError("Não foi possível resumir a página atual.");
  } finally {
    hideLoading();
  }
});

summarizeLinkBtn.addEventListener("click", async () => {
  try {
    const link = linkInput.value.trim();

    if (!link) {
      showError("Informe um link de site.");
      return;
    }

    showLoading();

    const data = await requestJson(`${API_BASE_URL}/summarize/html?model=gpt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: link,
      }),
    });

    showResult(getSummaryFromResponse(data));
  } catch (error) {
    console.error(error);
    showError("Não foi possível resumir o link informado.");
  } finally {
    hideLoading();
  }
});

summarizeVideoBtn.addEventListener("click", async () => {
  try {
    const videoUrl = videoInput.value.trim();

    if (!videoUrl) {
      showError("Informe um link de vídeo.");
      return;
    }

    showLoading();

    const data = await requestJson(`${API_BASE_URL}/summarize/video?model=gpt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: videoUrl,
      }),
    });

    showResult(getSummaryFromResponse(data));
  } catch (error) {
    console.error(error);
    showError("Não foi possível resumir o vídeo.");
  } finally {
    hideLoading();
  }
});

summarizePdfBtn.addEventListener("click", async () => {
  try {
    const file = pdfInput.files[0];

    if (!file) {
      showError("Selecione um arquivo PDF.");
      return;
    }

    if (file.type !== "application/pdf") {
      showError("O arquivo selecionado precisa ser um PDF.");
      return;
    }

    showLoading();

    const formData = new FormData();
    formData.append("file", file);

    const data = await requestJson(`${API_BASE_URL}/summarize/pdf?model=gpt`, {
      method: "POST",
      body: formData,
    });

    showResult(getSummaryFromResponse(data));
  } catch (error) {
    console.error(error);
    showError("Não foi possível resumir o PDF.");
  } finally {
    hideLoading();
  }
});

async function copyTextToClipboard(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;

  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  textarea.style.top = "-9999px";

  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();

  const copied = document.execCommand("copy");

  document.body.removeChild(textarea);

  if (!copied) {
    throw new Error("Falha ao copiar usando fallback.");
  }
}

async function copySummary() {
  const summary = summaryContent.textContent.trim();

  if (!summary) {
    showError("Não há resumo para copiar.");
    return;
  }

  try {
    await copyTextToClipboard(summary);

    copySummaryBtn.textContent = "✅";
    copySummaryBtn.classList.add("copied");

    setTimeout(() => {
      copySummaryBtn.textContent = "📋";
      copySummaryBtn.classList.remove("copied");
    }, 2000);
  } catch (error) {
    console.error("Erro ao copiar resumo:", error);
    showError("Não foi possível copiar o resumo.");
  }
}

copySummaryBtn.addEventListener("click", copySummary);