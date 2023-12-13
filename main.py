from typing import List
from googleapiclient.discovery import build
from fastapi import FastAPI
from pydantic import BaseModel
from config import YOUTUBE_API_KEY

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

class ReviewData:
    def __init__(self, id: str, title: str, description: str):
        self.id = id
        self.title = title
        self.description = description

class ReviewData(BaseModel):
    id: str
    title: str
    description: str

def fetch_movie_reviews(movie_name: str) -> List[ReviewData]:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    search_response = youtube.search().list(
        q=f"{movie_name} review",
        part='snippet',
        type='video',
        maxResults=10
    ).execute()

    reviews = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            title = search_result['snippet']['title']
            description = search_result['snippet']['description']
            reviews.append(ReviewData(id=video_id, title=title, description=description))

    return reviews

@app.get("/moviereviews/{movie_name}", response_model=List[ReviewData])
def get_movie_reviews(movie_name: str):
    reviews = fetch_movie_reviews(movie_name)
    return reviews