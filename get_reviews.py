from googleapiclient.discovery import build
from config import GOOGLE_API_KEY  # Assuming you have your API key in config.py

def translate_title(title, target_language):
    translate_service = build('translate', 'v2', developerKey=GOOGLE_API_KEY)
    translation_result = translate_service.translations().list(
        q=title, target=target_language
    ).execute()
    translated_title = translation_result['translations'][0]['translatedText']
    return translated_title

def search_youtube_videos(query, language):
    youtube_service = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)
    search_response = youtube_service.search().list(
        q=query,
        part='snippet',
        maxResults=10,
        relevanceLanguage=language
    ).execute()
    videos = []
    for item in search_response.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            videos.append({
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'description': item['snippet']['description']
            })
    return videos

def get_movie_reviews_in_language(movie_title, language_code):
    translated_title = translate_title(movie_title, language_code)
    query = f"{translated_title} review"
    reviews = search_youtube_videos(query, language_code)
    return reviews