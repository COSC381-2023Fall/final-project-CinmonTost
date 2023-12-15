import pytest
from unittest.mock import Mock, patch
from get_description import fetch_video_description
from config import YOUTUBE_API_KEY

@pytest.fixture
def mock_youtube_response():
    return {
        'items': [
            {
                'snippet': {
                    'description': 'Test Description'
                }
            }
        ]
    }

def test_fetch_video_description(mock_youtube_response):
    with patch('get_description.build') as mock_build:
        mock_service = Mock()
        mock_videos = Mock()
        mock_list = Mock()
        
        mock_build.return_value = mock_service
        mock_service.videos.return_value = mock_videos
        mock_videos.list.return_value = mock_list
        mock_list.execute.return_value = mock_youtube_response

        description = fetch_video_description('test_video_id')

        assert description == 'Test Description'
        mock_build.assert_called_once_with('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        mock_videos.list.assert_called_once_with(part='snippet', id='test_video_id')
