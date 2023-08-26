from flask import render_template, redirect,url_for,flash

from packages import app
from packages import db
from packages.forms import SignupForm, LoginForm
from packages.models import Product, Category, User


# route to display the homepage of the website
@app.route('/')
@app.route('/home')
def index():
    products_data = Product.query.all()
    return render_template('index.html', products=products_data)


# root to display the products category page
@app.route('/products')
def products():
    # Fetch product categories from data/category.py
    categories = Category.query.all()

    return render_template('products.html', categories=categories)


@app.route('/category/<string:category>')
def category(category):
    products = Product.query.filter_by(category=category).all()
    return render_template('category.html', category=category, products=products)

# route to display the sign-up page
@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              phone=form.phone.data,
                              dob=form.dob.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('dashboard'))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There was an error creating a user: {error_msg}',category='danger')
    return render_template('signup.html',form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html',user=users)


# route to display the about page
@app.route('/about')
def about():
    return render_template('about.html')


# route to display the contact us page
@app.route('/contact')
def contact():
    return render_template('contact.html')
