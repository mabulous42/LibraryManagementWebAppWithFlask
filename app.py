import json, os
from numpy import random
from flask import Flask, render_template, url_for, request, redirect, flash, abort
from forms import SignupForm, LoginForm, AddBookForm
from flask_bcrypt import Bcrypt
from models import User, Book, Library, AdminUser
from helpers import register_user, load_books, load_users, save_books, save_users, get_user_by_id, add_book
from datetime import datetime
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' #This will make flashing messages work perfectly and support Flask extensions like Flask-WTF.


bcrypt = Bcrypt(app)
library = Library()
load_users(library)
load_books(library)

admin_user = AdminUser()

# Hard-coded admin credentials
ADMIN_EMAIL = admin_user.email
ADMIN_PASSWORD = admin_user.password


# flask-login parameters
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader # this keeps track of the logged in user (current_user)
def load_user(user_id):
    if user_id == 'admin':      # checks if the user_id is admin then load user to be admin instead of the normal library users
        return AdminUser()
    
    user = library.get_user_by_id(user_id)  # this is where the actual library users is been loaded after the id is been fetched successfully
    return user



# admin decorator to make sure any user cannot have access to the admin features
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        # Check if current user is admin
        if not isinstance(current_user, AdminUser):
            abort(403)  # Forbidden
        
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
def home():
    return render_template("index.html")
    



@app.route("/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        num = random.randint(0, 9999)
        id = "{:03}".format(num)
        user_id = 'LU0' + id
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        firstName = form.firstName.data
        lastName = form.lastName.data
        name = firstName + " " + lastName

        new_user = User(name, user_id, form.email.data, hashed_password) #called the class User() constructor to create a new library user
        register_user(library, new_user) #called the register function from the helpers.py to register a new user

        save_users(library) #saving the new user into json storage

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    flash('User Already Exist', 'fail')

    return render_template("signup.html", form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = library.get_user_email(form.email.data)
        admin_email = form.email.data
        admin_password = form.password.data

        if admin_email == ADMIN_EMAIL and admin_password == ADMIN_PASSWORD:
            login_user(admin_user)
            flash('Admin login successful!', 'success')
            return redirect(url_for('adminDashboard'))

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('userDashboard'))
        
    
    return render_template("login.html", form=form)


@app.route('/userDashboard', methods=['GET', 'POST'])
@login_required
def userDashboard():
    user = current_user
    print(f"User authenticated: {user.is_authenticated}")
    print(f"User ID: {user.id}")
    print(f"User object: {user}")

    return render_template('user/userdashboard.html', user = user)

@app.route('/adminDashboard', methods=['GET', 'POST'])
@login_required
def adminDashboard():
    admin_user = current_user
    print(f"User authenticated: {admin_user.is_authenticated}")
    print(f"User ID: {admin_user.id}")
    print(f"User object: {admin_user}")

    library_users = load_users(library)
    library_books = load_books(library)
    # library_users = [user.to_dict() for user in library_users.values()]
    print((library_users))
    print((library_books))

    return render_template('admin/adminDashboard.html', 
                           admin_user = admin_user,
                           library_users = library_users,
                           library_books = library_books                           
                           )

@app.route('/admin/add_books', methods=['GET', 'POST'])
@login_required
@admin_required
def add_books():
    form = AddBookForm()

    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        isbn = form.isbn.data
        available_copies = form.copies.data

        # creating and instance of class Book to add new book
        new_book = Book(title, author, isbn, available_copies)
        

        # adding a new book, using the add_book function from helper.py
        add_book(library, new_book)

        # saving the added book to json storage   
        save_books(library) 

        flash('Book added successfully!', 'success')
        return redirect(url_for('adminDashboard'))
    flash('Book ISBN Already Exist', 'fail')


    return render_template("admin/add_books.html", form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    print(f"Logging out user: {current_user.id}")
    logout_user()  # Fixed - no parameter
    print("User logged out")
    return redirect(url_for('login'))




if __name__ == '__main__' :
    app.run(debug=True)