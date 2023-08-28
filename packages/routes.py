from flask import render_template, redirect,url_for,flash
from packages import app
from packages import db
from packages.forms import SignupForm, LoginForm
from packages.models import Product, Category, User
from flask_login import login_user,login_required,logout_user


# route to display the homepage of the website
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')




#route to display the market page of the webiste
@app.route('/market')
@login_required
def market():
    products_data = Product.query.all()
    return render_template('market.html', products=products_data)


# root to display the products category page
@app.route('/products')
@login_required
def products():
    # Fetch product categories from data/category.py
    categories = Category.query.all()

    return render_template('products.html', categories=categories)


@app.route('/category/<string:category>')
@login_required
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
                              budget=form.budget.data + 1000,
                              dob=form.dob.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('dashboard'))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There was an error creating a user: {error_msg}',category='danger')
    return render_template('signup.html',form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction (attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Successfully logged in as {attempted_user.username}!', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username or password is wrong! Please try again.',category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have been logged out!',category='info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
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
