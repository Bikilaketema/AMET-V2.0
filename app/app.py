import configparser
import bcrypt
from flask import Flask, render_template, request, redirect, session
import json
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amet.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(length=20),nullable=False,unique=True)
    category = db.Column(db.String(length=20),nullable=False)
    image = db.Column(db.String(length=20),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    description = db.Column(db.String(length=1024),nullable=False,unique=True)

class Category(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=20),nullable=False,unique=True)
    image = db.Column(db.String(length=20),nullable=False,unique=True)


# Read the secret key from the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

app.secret_key = config.get('flask', 'SECRET_KEY')


#route to display the homepage of the website
@app.route('/home')
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

#root to display the products category page
@app.route('/products')
def products():
    # Fetch product categories from data/category.py
    categories = Category.query.all()

    return render_template('products.html', categories=categories)

@app.route('/category/<string:category>')
def category(category):
    products = Product.query.filter_by(category=category).all()
    return render_template('category.html', category=category, products=products)


#route to display the about page
@app.route('/about')
def about():
    return render_template('about.html')

#route to display the contact us page
@app.route('/contact')
def contact():
    return render_template('contact.html')

#route to display the sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        phnum = request.form['phnum']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Password hashing using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if len(password) < 6:
            # Password is too short
            return render_template('signup.html', error='Password must be at least 6 characters long.', email=email)

        if password == confirm_password:
            # Create a dictionary with user information
            user_data = {
                'fname': fname,
                'lname': lname,
                'phnum': phnum,
                'email': email,
                'dob': dob,
                'password': hashed_password
            }

            file_path = 'users_data.json'

            # Check if the JSON file exists
            if not os.path.exists(file_path):
                # Create the file if it doesn't exist
                with open(file_path, 'w') as file:
                    json.dump([], file)

            # Read existing user data from the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Check if a user with the given email already exists
            if any(user['email'] == email for user in data):
                return render_template('signup.html', error='Email already exists.', email=email)

            # Add the new user data to the existing data
            data.append(user_data)

            # Write the updated JSON data
            with open(file_path, 'w') as file:
                json.dump(data, file)

            # Set the session to mark the user as logged in
            session['user'] = email
            session['userfname'] = fname
            session['userlname'] = lname

            return redirect('/dashboard')
        else:
            # Passwords do not match
            return render_template('signup.html', error='Passwords do not match.', email=email)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        # User is already logged in, redirect to the dashboard
        return redirect('/dashboard')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the 'users_data.json' file exists
        file_path = 'users_data.json'
        if not os.path.exists(file_path):
            return render_template('login.html', error='No users found. Please sign up first.')

        # Read user data from the JSON file
        with open(file_path, 'r') as file:
            user_data = json.load(file)

        # Check if a user with the given email exists
        user = next((user for user in user_data if user['email'] == email), None)

        if user is not None and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Password matches, store user email in the session
            session['user'] = email
            return redirect('/dashboard')
        else:
            # Incorrect email or password
            return render_template('login.html', error='Invalid email or password.', email=email)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        # User is logged in, retrieve the user email from the session
        email = session['user']

        # Read user data from the JSON file
        file_path = 'users_data.json'
        with open(file_path, 'r') as file:
            user_data = json.load(file)

        # Find the user's data based on their email
        user = next((user for user in user_data if user['email'] == email), None)

        if user is not None:
            # User data found, display the profile on the dashboard
            return render_template('dashboard.html', user=user, signed_in=True)
        else:
            # User not found in the JSON data (shouldn't happen if data is consistent)
            return redirect('/login')
    else:
        # User is not logged in, redirect to the login page
        return redirect('/login')


#route to logout the user from the platform
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
