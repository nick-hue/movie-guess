import random
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

BASE_URL = "https://image.tmdb.org/t/p/w"

class Movie:
    def __init__(self, id, title, release_date, img_path) -> None:
        self.id = id 
        self.title = title
        self.release_date = release_date
        self.img_path = img_path
        self.img_url_500 = BASE_URL + '500' + self.img_path
        self.img_url_1200 = BASE_URL + '1200' + self.img_path

    def display(self):
        print(f"{self.id} - {self.title}")

def get_random_movies(movies):
    """Randomly select two different movies from the list."""
    movie1, movie2 = random.sample(movies, 2)
    return movie1, movie2

def compare_release_dates(movie1, movie2):
    """Compare the release dates of two movies."""
    date1 = datetime.strptime(movie1.release_date, "%Y-%m-%d")
    date2 = datetime.strptime(movie2.release_date, "%Y-%m-%d")

    if date1 > date2:
        return movie1
    else:
        return movie2

def play_round(movies, show_images):
    """Play a single round of the game."""
    movie1, movie2 = get_random_movies(movies)
    
    print(f"Which movie was released later?")
    print(f"1: {movie1.title} (Release Date: {movie1.release_date})")
    print(f"2: {movie2.title} (Release Date: {movie2.release_date})")

    if show_images:
        image1 = show_image(movie1)
        image2 = show_image(movie2)

    guess = input("Enter 1 or 2: ")
    
    if guess not in ['1', '2']:
        print("Invalid input! Please enter 1 or 2.")
        return False
    
    if guess == '1':
        player_choice = movie1
    else:
        player_choice = movie2
    
    correct_movie = compare_release_dates(movie1, movie2)
    
    if show_images:
        close_images(image1, image2)

    if player_choice == correct_movie:
        print("Correct! Well done.")
        return True
    else:
        print(f"Incorrect. The correct answer was {correct_movie.title}.")
        return False
    
    

def show_image(movie):
    response = requests.get(movie.img_url_500)
    img = Image.open(BytesIO(response.content))
    img.show()

    return img

def close_images(img1, img2):
    print("Closing Images...")
    img1.close()
    img2.close()

def play_game(movies, show_images):
    """Main game loop."""
    score = 0
    
    while True:
        result = play_round(movies, show_images)
        if result:
            score += 1
            print(f"Your current score: {score}")
        else:
            print(f"Game over! Your final score: {score}")
            break

def get_all_movies(movies_amount):
    # Number of pages scanned, each page has 20 movies
    iterations = movies_amount//20 + 2
 
    # Get the <movies_amount> best movies 
    base_url = "https://api.themoviedb.org/3/movie/top_rated"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MGY4OWNiNGNkMWU3MjRkZGFkOWYyYWNjMDkyMWVjZCIsIm5iZiI6MTcyMzY2MDUwOC43MzkwMTEsInN1YiI6IjY2YmNmNWFjNGEzZjUxNWVjOGNmNTZhZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.uJIGPCOFZBZp27MJUo6uUemUk49Z0wHhg2DlP6xsXGs"
    }

    all_movies = []

    # Loop for given pages
    for page in range(1, iterations):
        # Get movies for current page number
        url = f"{base_url}?language=en-US&page={page}"
        response = requests.get(url, headers=headers)
        
        # If request was good, store results into the list
        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
            all_movies.extend([Movie(item['id'], item['title'], item['release_date'], item['poster_path']) for item in movies])
            # all_movies.extend(movies)
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")
        
    return all_movies

if __name__ == "__main__":
    movies_amount = 500
    print(f"Main is running...")
    all_movies = get_all_movies(500)
    
    print(f"{len(all_movies)} movies fetched.")

    play_game(all_movies, show_images=False)
