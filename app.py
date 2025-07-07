import json, os
from numpy import random
from flask import Flask, render_template, url_for, request, redirect, flash
from forms import SignupForm, LoginForm
from flask_bcrypt import Bcrypt
from models import User, Book, Library, AdminUser
from helpers import register_user, load_books, load_users, save_books, save_users, get_user_by_id
from datetime import datetime
from flask_login import login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' #This will make flashing messages work perfectly and support Flask extensions like Flask-WTF.


bcrypt = Bcrypt(app)
library = Library()
load_users(library)

# Hard-coded admin credentials
ADMIN_EMAIL = "admin@mustyllibrary.com"
ADMIN_PASSWORD = "admin101"


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
            admin_user = AdminUser()
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

    return render_template('userdashboard.html', user = user)

@app.route('/adminDashboard', methods=['GET', 'POST'])
@login_required
def adminDashboard():
    admin_user = current_user
    print(f"User authenticated: {admin_user.is_authenticated}")
    print(f"User ID: {admin_user.id}")
    print(f"User object: {admin_user}")

    return render_template('adminDashboard.html', admin_user = admin_user)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    print(f"Logging out user: {current_user.id}")
    logout_user()  # Fixed - no parameter
    print("User logged out")
    return redirect(url_for('login'))




if __name__ == '__main__' :
    app.run(debug=True)