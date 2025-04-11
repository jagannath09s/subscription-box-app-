from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.recommender import BoxRecommender
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

recommender = BoxRecommender(
    'data/user_preferences.csv',
    'data/products.csv')

# Database helper
def get_db_connection():
    conn = sqlite3.connect('subscription_box.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- AUTH ROUTES ----------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (name, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Signup successful. Please log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already taken.")
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE name = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['name']
            flash('Login successful.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.')
    return redirect(url_for('home'))

# ---------- MAIN ROUTES ----------



@app.route('/')
def home():
    print(">>> Home page accessed")
    return render_template('index.html')  # This must exist in the 'templates' folder



@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/recommend', methods=['POST'])
def recommend():
    if 'username' not in session:
        return redirect(url_for('login'))

    prefs = [
        int(request.form['beauty']),
        int(request.form['fitness']),
        int(request.form['food']),
        int(request.form['tech']),
        int(request.form['lifestyle'])
    ]

    recommendations = recommender.recommend(prefs)
    print(">>> Recommendations generated:", recommendations)  # 🔍 See this in console

    if not recommendations:
        flash("No recommendations found. Please try different preferences.")
        return redirect(url_for('dashboard'))

    return render_template('result.html', recommendations=recommendations)




if __name__ == '__main__':
    app.run(debug=True)
