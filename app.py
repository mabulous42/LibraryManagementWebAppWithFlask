import json, os
from flask import Flask, render_template, url_for, request, redirect
from forms import SignupForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' #This will make flashing messages work perfectly and support Flask extensions like Flask-WTF.

USER_DB = 'users.json'
BOOK_DB = 'books.json'


#i will still add def load and save books too here
def load_users():
    if os.path.exists(USER_DB): #os.path.exist is used to check if a path exist
        try:
            with open(USER_DB, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: users.json is not a valid JSON file.")
            return []
    else:
        return []

def save_users(users):
    with open(USER_DB, 'w') as file:
        json.dump(users, file, indent=4)





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()


    return render_template("signup.html", form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    
    return render_template("login.html")



if __name__ == '__main__' :
    app.run(debug=True)