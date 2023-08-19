from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

# sqlite3 connecting
def get_connection():
    try:
        return sqlite3.connect("url_shortener.db")
    except sqlite3.Error as e:
        print("Error connecting to the database: " + str(e))
        return None


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Table-structuring
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT NOT NULL
            )
        ''')
        conn.commit()
init_db()

# Function for URL Shortening: --using string
def generate_short_code(length):
    characters = string.ascii_letters + string.digits
    # range() for the length of the shortened-link
    return ''.join(random.choice(characters) for _ in range(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    shortened_url = None  # Initializing the variable outside the if-block

    if request.method == 'POST':
        original_url = request.form['original_url']
        # user-input for the length of the link
        short_code_length = int(request.form['short_code_length'])
        short_code = generate_short_code(short_code_length)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
            conn.commit()

        # Assigning the value to shortened_url
        shortened_url = f'/{short_code}'

    return render_template('index.html', shortened_url=shortened_url, request=request)


# Implementing Redirection:
@app.route('/<short_code>')
def redirect_to_original(short_code):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
        result = cursor.fetchone()
        if result:
            original_url = result[0]
            return redirect(original_url)

    return "URL not found."


if __name__ == '__main__':
    app.run(debug=True)
