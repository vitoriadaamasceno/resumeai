from unittest.mock import MagicMock, patch
from extract.pdf_reader import get_pdf_text


@patch("extract.pdf_reader.PdfReader")
@patch("extract.pdf_reader.BytesIO")
def test_get_pdf_text(mock_bytes_io, mock_pdf_reader):
    mock_pdf_reader_instance = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()
    mock_page1.extract_text.return_value = "Texto da página 1. "
    mock_page2.extract_text.return_value = "Texto da página 2. "
    mock_pdf_reader_instance.pages = [mock_page1, mock_page2]
    mock_pdf_reader.return_value = mock_pdf_reader_instance
    mock_bytes_io.return_value = MagicMock()

    result = get_pdf_text(b"dummy pdf content")

    assert result == "Texto da página 1. Texto da página 2. "
    mock_bytes_io.assert_called_once_with(b"dummy pdf content")
    mock_pdf_reader.assert_called_once_with(mock_bytes_io.return_value)
    mock_page1.extract_text.assert_called_once()
    mock_page2.extract_text.assert_called_once()


 