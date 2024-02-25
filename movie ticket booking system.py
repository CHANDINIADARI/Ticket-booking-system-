from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key'  # Change this to a more secure secret key

# In a real-world scenario, you would use a database to store movie and booking information
movies = [
    {'id': 1, 'title': 'Movie 1', 'seats': 100},
    {'id': 2, 'title': 'Movie 2', 'seats': 150},
    {'id': 3, 'title': 'Movie 3', 'seats': 200}
]

# In-memory bookings storage (for demonstration purposes)
bookings = {}

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie is None:
        flash('Movie not found.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        num_tickets = int(request.form['num_tickets'])
        if num_tickets <= 0:
            flash('Number of tickets must be greater than zero.')
        elif num_tickets > movie['seats']:
            flash('Not enough seats available.')
        else:
            movie['seats'] -= num_tickets
            bookings.setdefault(movie_id, 0)
            bookings[movie_id] += num_tickets
            flash(f'{num_tickets} ticket(s) booked for {movie["title"]}.')
            return redirect(url_for('index'))

    return render_template('book.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
