from main import get_all_movies, Movie
from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

all_movies = get_all_movies(20)

def compare_release_dates(movie1: Movie, movie2: Movie) -> Movie:
    date1 = datetime.strptime(movie1.release_date, "%Y-%m-%d")
    date2 = datetime.strptime(movie2.release_date, "%Y-%m-%d")
    return movie1 if date1 > date2 else movie2

@app.route('/')
def index():
    session['score'] = 0  # Reset the score
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    session['current_movies'] = random.sample(all_movies, 2)

    if request.method == 'POST':
        guessed_movie_index = int(request.form['guess'])
        guessed_movie: Movie = session['current_movies'][guessed_movie_index]
        correct_movie = compare_release_dates(*session['current_movies'])

        print(f"Guess {guessed_movie.title} date : {guessed_movie.release_date} - Correct {correct_movie.title} date {correct_movie.release_date}")

        if guessed_movie.id == correct_movie.id:
            print("Correct Guess!")
            session['score'] += 1
            session['current_movies'] = random.sample(all_movies, 2)
            print(f"Session after picking {session}")
            return redirect(url_for('game'))
        else:
            return redirect(url_for('game_over'))

    # Initialize game
    if 'current_movies' not in session:
        session['score'] = 0
        session['current_movies'] = random.sample(all_movies, 2)

    return render_template('game.html', movies=session['current_movies'], score=session['score'])

@app.route('/game_over')
def game_over():
    return render_template('gameover.html', score=session['score'])

@app.route('/save_score', methods=['POST'])
def save_score():
    # Logic to save the score, for example in a database or file
    player_name = request.form['player_name']
    # Save player_name and session['score'] to leaderboard (not implemented here)
    return redirect(url_for('leaderboard'))

@app.route('/leaderboard')
def leaderboard():
    # Logic to display the leaderboard (not implemented here)
    leaderboard_data = []  # Replace with actual leaderboard data
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

if __name__ == '__main__':
    app.run(debug=True)
