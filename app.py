import json, os
from numpy import random
from flask import Flask, render_template, url_for, request, redirect, flash
from forms import SignupForm, LoginForm
from flask_bcrypt import Bcrypt
from models import User, Book, Library
from helpers import register_user, load_books, load_users, save_books, save_users, get_user_by_id
from datetime import datetime
from flask_login import login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' #This will make flashing messages work perfectly and support Flask extensions like Flask-WTF.


bcrypt = Bcrypt(app)
library = Library()
load_users(library)


# flask-login parameters
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    user = library.get_user_by_id(user_id)
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

    return render_template("signup.html", form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = library.get_user_email(form.email.data)

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('userDashboard'))    
    
    return render_template("login.html", form=form)


@app.route('/userDashboard', methods=['GET', 'POST'])
@login_required
def userDashboard():
    user = current_user
    print(user)

    return render_template('userdashboard.html', user = user)



if __name__ == '__main__' :
    app.run(debug=True)