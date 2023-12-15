import pytest
from unittest.mock import Mock, patch
from get_reviews import get_movie_reviews_in_language  # Replace 'your_module' with the actual name of your Python file
from config import GOOGLE_API_KEY

@pytest.fixture
def mock_translate_response():
    return {'translations': [{'translatedText': 'Translated Title'}]}

@pytest.fixture
def mock_youtube_search_response():
    return {
        'items': [
            {
                'id': {'kind': 'youtube#video', 'videoId': 'video_id_1'},
                'snippet': {
                    'title': 'Video Title 1',
                    'description': 'Description 1',
                    'thumbnails': {'default': {'url': 'thumbnail_url_1'}}
                }
            },
        ]
    }

@patch('get_reviews.build')
def test_get_movie_reviews_in_language(mock_build, mock_translate_response, mock_youtube_search_response):
    mock_translate_service = Mock()
    mock_translate_list = Mock()
    mock_translate_service.translations.return_value = mock_translate_list
    mock_translate_list.list.return_value = mock_translate_list
    mock_translate_list.execute.return_value = mock_translate_response

    mock_youtube_service = Mock()
    mock_youtube_search = Mock()
    mock_youtube_service.search.return_value = mock_youtube_search
    mock_youtube_search.list.return_value = mock_youtube_search
    mock_youtube_search.execute.return_value = mock_youtube_search_response

    def mock_build_service(serviceName, version, developerKey):
        if serviceName == 'translate':
            return mock_translate_service
        elif serviceName == 'youtube':
            return mock_youtube_service

    mock_build.side_effect = mock_build_service

    reviews = get_movie_reviews_in_language('Inception', 'es')

    assert len(reviews) > 0
    assert reviews[0]['title'] == 'Video Title 1'
    assert reviews[0]['description'] == 'Description 1'
    assert 'url' in reviews[0]

    mock_translate_service.translations().list.assert_called_once_with(q='Inception', target='es')
    mock_youtube_service.search().list.assert_called_once_with(
        q='Translated Title review', part='snippet', maxResults=10, relevanceLanguage='es'
    )
