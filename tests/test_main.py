from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

def test_summarize_pdf():

    client = TestClient(app)

    # Mock da função de geração de IA
    with patch("main.gerar_resumo_t5") as mock_generate_summary:
        mock_generate_summary.return_value = "Resumo gerado pela IA."

        # Teste com arquivo não PDF
        with open("tests/test_files/invalid.txt", "rb") as f:
            response = client.post("/summarize/pdf", files={"file": ("invalid.txt", f, "text/plain")})
            assert response.status_code == 400
            assert response.json() == {"error": "O arquivo deve ser um PDF."}

        # Teste com arquivo PDF válido
        with open("tests/test_files/valid.pdf", "rb") as f:
            response = client.post("/summarize/pdf", files={"file": ("valid.pdf", f, "application/pdf")})
            assert response.status_code == 200
            assert response.json() == {"resumo": "Resumo gerado pela IA."}

        # Teste com arquivo PDF inválido (não encontrado)
        response = client.post("/summarize/pdf", files={"file": (None, None, "application/pdf")})
        assert response.status_code == 400


        # Teste com erro ao processar o arquivo PDF
        with open("tests/test_files/corrupted.pdf", "rb") as f:
            response = client.post("/summarize/pdf", files={"file": ("corrupted.pdf", f, "application/pdf")})
            assert response.status_code == 500
            assert response.json() == {"error": "Erro ao processar o arquivo PDF."}