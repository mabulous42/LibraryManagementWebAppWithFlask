import json, os
from numpy import random
from flask import Flask, render_template, url_for, request, redirect, flash
from forms import SignupForm
from flask_bcrypt import Bcrypt
from models import User, Book, Library
from helpers import register_user, load_data, save_data
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' #This will make flashing messages work perfectly and support Flask extensions like Flask-WTF.

USER_DB = 'users.json'
BOOK_DB = 'books.json'

bcrypt = Bcrypt(app)
library = Library()
load_data(library)



#i will still add def load and save books too here
# def load_users():
#     if os.path.exists(USER_DB): #os.path.exist is used to check if a path exist
#         try:
#             with open(USER_DB, 'r') as file:
#                 return json.load(file)
#         except json.JSONDecodeError:
#             print("Error: users.json is not a valid JSON file.")
#             return []
#     else:
#         return []

# def save_users(users):
#     with open(USER_DB, 'w') as file:
#         json.dump(users, file, indent=4)





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

        new_user = User(user_id, name, form.email.data, hashed_password, ) #called the class User() constructor to create a new library user
        register_user(library, new_user) 

        # try:
        #     with open('users.json', 'r') as file:
        #         users = json.load(file)
        #         if not isinstance(users, list):
        #             users = []
        # except FileNotFoundError:
        #     users = []

        # users.append(new_user)

        save_data(library)

        # with open('users.json', 'w') as file:
        #     json.dump(users, file, indent=4)

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template("signup.html", form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    
    return render_template("login.html")



if __name__ == '__main__' :
    app.run(debug=True)