import requests

OMDB_API_KEY = "4e6dfc6d"  

def fetch_movie_details(title):
    """Fetch movie details from OMDB API using the title."""
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "genre": data.get("Genre"),
                "plot": data.get("Plot"),
                "poster": data.get("Poster"),
                "rating": data.get("imdbRating"),
            }
    return None