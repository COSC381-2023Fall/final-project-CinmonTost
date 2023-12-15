from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_movie_reviews():

    response = client.get("/moviereviews/Inception")
    assert response.status_code == 200
    reviews = response.json()
    assert len(reviews) == 10  

    for review in reviews:
        assert "id" in review
        assert "title" in review
        assert "description" in review

    response = client.get("/moviereviews/NonExistentMovie123")
    assert response.status_code == 200
    reviews = response.json()
    assert len(reviews) == 0  

def test_get_video_description():
    test_video_id = "dQw4w9WgXcQ"

    response = client.get(f"/descriptions/{test_video_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['video_id'] == test_video_id
    assert 'description' in data

    non_existent_video_id = "thisisnotarealvideoID"
    response = client.get(f"/descriptions/{non_existent_video_id}")
    assert response.status_code == 404