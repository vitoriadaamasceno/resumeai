from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch


def test_invalid_file_type():
    client = TestClient(app)
    with patch("main.gerar_resumo_t5") as mock_generate_summary:
        mock_generate_summary.return_value = "Resumo gerado pela IA."
        with open("tests/test_files/invalid.txt", "rb") as f:
            response = client.post("/summarize/pdf", files={"file": ("invalid.txt", f, "text/plain")})
            assert response.status_code == 400
            assert response.json() == {"error": "O arquivo deve ser um PDF."}


def test_valid_pdf_file():
    client = TestClient(app)
    with patch("main.gerar_resumo_t5") as mock_generate_summary:
        mock_generate_summary.return_value = "Resumo gerado pela IA."
        with open("tests/test_files/valid.pdf", "rb") as f:
            response = client.post("/summarize/pdf", files={"file": ("valid.pdf", f, "application/pdf")})
            assert response.status_code == 200
            assert response.json() == {"resumo": "Resumo gerado pela IA."}


def test_missing_pdf_file():
    client = TestClient(app)
    with patch("main.gerar_resumo_t5") as mock_generate_summary:
        mock_generate_summary.return_value = "Resumo gerado pela IA."
        response = client.post("/summarize/pdf", files={"file": (None, None, "application/pdf")})
        assert response.status_code == 400


def test_corrupted_pdf_file():
    client = TestClient(app)
    with patch("main.gerar_resumo_t5") as mock_generate_summary:
        mock_generate_summary.return_value = "Resumo gerado pela IA."
        with open("tests/test_files/corrupted.pdf", "rb") as f:
            response = client.post("/summarize/pdf", files={"file": ("corrupted.pdf", f, "application/pdf")})
            assert response.status_code == 500
            assert response.json() == {"error": "Erro ao processar o arquivo PDF."}
