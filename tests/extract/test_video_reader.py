import pytest
from unittest.mock import patch
from extract.video_reader import get_video_transcript
from youtube_transcript_api import TranscriptsDisabled


@patch("extract.video_reader.YouTubeTranscriptApi.get_transcript")
@patch("extract.video_reader.extract_id_video")
def test_get_video_transcript_success(mock_extract_id_video, mock_get_transcript):
    mock_extract_id_video.return_value = "video123"
    mock_get_transcript.return_value = [
        {"text": "Olá", "start": 0, "duration": 2},
        {"text": "mundo", "start": 2, "duration": 2},
    ]

    url = "https://www.youtube.com/watch?v=video123"
    result = get_video_transcript(url)

    mock_extract_id_video.assert_called_once_with(url)
    mock_get_transcript.assert_called_once_with("video123", languages=["pt"])
    assert result == "Olá mundo"


@patch("extract.video_reader.YouTubeTranscriptApi.get_transcript")
@patch("extract.video_reader.extract_id_video")
def test_get_video_transcript_transcripts_disabled(mock_extract_id_video, mock_get_transcript):
    mock_extract_id_video.return_value = "video123"
    mock_get_transcript.side_effect = TranscriptsDisabled("video123")

    url = "https://www.youtube.com/watch?v=video123"

    with pytest.raises(ValueError, match="Transcrição desativada para este vídeo."):
        get_video_transcript(url)

    mock_extract_id_video.assert_called_once_with(url)
    mock_get_transcript.assert_called_once_with("video123", languages=["pt"])