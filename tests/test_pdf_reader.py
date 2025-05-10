from unittest.mock import MagicMock, patch
from extract.pdf_reader import extract_text_from_pdf

@patch("resumeai.extract.pdf_reader.pymupdf.open")
def test_extract_text_from_pdf(mock_pymupdf_open):

    mock_doc = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()
    mock_page1.get_text.return_value = "Page 1 text. "
    mock_page2.get_text.return_value = "Page 2 text. "
    mock_doc.__iter__.return_value = [mock_page1, mock_page2]
    mock_pymupdf_open.return_value = mock_doc

    result = extract_text_from_pdf("dummy.pdf")

    assert result == "Page 1 text. Page 2 text. "
    mock_pymupdf_open.assert_called_once_with("dummy.pdf")
    mock_page1.get_text.assert_called_once()
    mock_page2.get_text.assert_called_once()