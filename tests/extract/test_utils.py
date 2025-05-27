import pytest
import extract.utils as extract_id_video


def test_extract_id_video():
    url = "https://www.youtube.com/watch?v=abcdefghijk"
    expected_id = "abcdefghijk"
    assert extract_id_video.extract_id_video(url) == expected_id


def test_extract_id_video_invalid_url():
    url = "https://www.example.com/watch?v=abcdefghijk"
    id_video = extract_id_video.extract_id_video(url)
    assert id_video is None
