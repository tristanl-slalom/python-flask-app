from flask import Flask, render_template, request, redirect, url_for, session
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username.startswith('nick'):
            session['username'] = username
            return redirect(url_for('home'))
        elif username.startswith('tristan'):
            error = 'Please change your password before logging in.'
        else:
            error = 'Invalid username. Must start with "nick" or "Tristan".'

    return render_template('login.html', error=error)


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/dad_joke', methods=['GET', 'POST'])
def dad_joke():
    if 'username' not in session:
        return redirect(url_for('login'))

    joke = None
    timestamp = None

    if request.method == 'POST':
        response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
        joke = response.json().get('joke')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('dad_joke.html', joke=joke, timestamp=timestamp)


@app.route('/about')
def about():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)