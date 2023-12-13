from youtubesearchpython import VideosSearch

def get_movie_reviews(movie_title):
    videos_search = VideosSearch(movie_title + " review", limit = 10)  # Search for reviews specifically

    videos = videos_search.result()['result']

    reviews = []
    for video in videos:
        title = video['title']
        url = video['link']
        description = video['description']
        
        reviews.append({
            'title': title,
            'url': url,
            'description': description
        })

    return reviews
