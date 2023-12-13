import youtube_search

def test_get_movie_reviews(mocker):
    mock_result = {
        'result': [
            {'title': 'Review 1', 'link': 'link1', 'description': 'Description 1'},
            {'title': 'Review 2', 'link': 'link2', 'description': 'Description 2'},
        ]
    }
    mocker.patch.object(youtube_search.VideosSearch, 'result', return_value=mock_result)

    movie_title = 'Interstellar'
    reviews = youtube_search.get_movie_reviews(movie_title)

    assert len(reviews) == 2  
    assert reviews[0]['title'] == 'Review 1'
    assert reviews[0]['url'] == 'link1'
    assert reviews[0]['description'] == 'Description 1'
    assert reviews[1]['title'] == 'Review 2'
    assert reviews[1]['url'] == 'link2'
    assert reviews[1]['description'] == 'Description 2'