import pytest
from unittest.mock import patch
from extract.video_reader import get_video_transcript
from youtube_transcript_api import TranscriptsDisabled


@patch("extract.video_reader.YouTubeTranscriptApi.get_transcript")
def test_get_video_transcript_success(mock_get_transcript):
    extract_id_video = "video123"
    mock_get_transcript.return_value = [
        {"text": "Olá", "start": 0, "duration": 2},
        {"text": "mundo", "start": 2, "duration": 2},
    ]

    result = get_video_transcript(extract_id_video)

    mock_get_transcript.assert_called_once_with("video123", languages=["pt"])
    assert result == "Olá mundo"
    