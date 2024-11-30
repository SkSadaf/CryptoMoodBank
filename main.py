from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app and the database
app = Flask(__name__)

# Use an environment variable for security key or fallback
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_fallback_key')

# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Store hashed password
    moods = db.relationship('Mood', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Mood model
class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    reward = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Mood('{self.user_id}', '{self.mood}', '{self.date}', '{self.reward}')"

# Route for the home page
@app.route('/')
def index():
    return render_template("home.html", data="")

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the database for a user with the provided email
        user = User.query.filter_by(email=email).first()

        # If the user exists and the password matches
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store the user_id in session
            return redirect(url_for('mood_tracking'))  # Redirect to mood tracking page
        else:
            flash("Invalid email or password. Please try again.", 'danger')
    
    return render_template("login.html", data="")

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user_id from session
    return redirect(url_for('index'))  # Redirect to home page

# Route for mood tracking (logged-in users only)
@app.route('/mood', methods=['GET', 'POST'])
def mood_tracking():
    user_id = session.get('user_id')  # Get the logged-in user's ID from session

    # If user_id is not found (i.e., user is not logged in), redirect to login page
    if user_id is None:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))  # Redirect to login page

    if request.method == 'POST':
        mood = request.form['mood']  # Get mood from form
        date = datetime.today().date()  # Get today's date

        # Assign a random coin reward based on mood
        reward = random.randint(5, 20)

        # Create a new Mood record
        new_mood = Mood(user_id=user_id, mood=mood, date=date, reward=reward)
        db.session.add(new_mood)
        db.session.commit()  # Save to database

        return redirect('/mood')  # Redirect back to the mood page to see the updated list
    
    # Fetch all moods of the logged-in user
    moods = Mood.query.filter_by(user_id=user_id).order_by(Mood.date.desc()).all()

    # Calculate total rewards for the month
    total_rewards = sum([m.reward for m in moods])

    return render_template("mood.html", moods=moods, total_rewards=total_rewards)

# Route for user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new User record
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()  # Save to the database
        flash("User registered successfully! You can now log in.", "success")

        return redirect(url_for('login'))  # Redirect to login page
    
    return render_template("signup.html", data="")

# Route for about page
@app.route('/about')
def about():
    return render_template("about.html", data="")

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables if they don't exist
    app.run(debug=True, host='0.0.0.0', port=8000)