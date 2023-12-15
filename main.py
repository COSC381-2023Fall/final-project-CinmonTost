from typing import List
from googleapiclient.discovery import build
from get_description import fetch_video_description
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import YOUTUBE_API_KEY
from get_reviews import get_movie_reviews_in_language


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

class VideoDescription(BaseModel):
    video_id: str
    description: str

class Video(BaseModel):
    title: str
    url: str
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

@app.get("/descriptions/{video_id}", response_model=VideoDescription)
def get_video_description(video_id: str):
    description = fetch_video_description(video_id)
    if description is None:
        raise HTTPException(status_code=404, detail="Video not found or has no description")
    return VideoDescription(video_id=video_id, description=description)

@app.get("/moviereviews/{language}/{movie_name}", response_model=List[Video])
def get_movie_reviews(language: str, movie_name: str):
    reviews_data = get_movie_reviews_in_language(movie_name, language)
    return [Video(**video) for video in reviews_data]