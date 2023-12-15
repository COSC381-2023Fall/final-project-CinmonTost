from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY
from pydantic import BaseModel

def fetch_video_description(video_id: str) -> str:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    if video_response['items']:
        description = video_response['items'][0]['snippet']['description']
        return description
