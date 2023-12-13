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

