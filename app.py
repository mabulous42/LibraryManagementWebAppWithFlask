import json
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")



if __name__ == '__main__' :
    app.run(debug=True)