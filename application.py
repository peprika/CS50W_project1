import os

from flask import Flask, session, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)


# Site name
website_title = "Book Reviews"

@app.route("/")
def index():
    return render_template("index.html", website_title=website_title)
	
@app.route("/signup", methods=["GET"])
def signup():
        return render_template("signup.html", website_title=website_title)


@app.route("/mypage", methods=["POST"])
def mypage():

    # REGISTER A NEW USER
    # TODO: How to differentiate between login/signup form submissions?
    
    # Collect info from the signup form
    input_email = request.form.get("email")
    input_username = request.form.get("username")
    input_password = request.form.get("password")
    input_password2 = request.form.get("password2")
    
    # Create the User class
    class User:
        def __init__(self, email, username, password, password2):
            self.email = input_email
            self.username = input_username
            self.password = input_password
            self.password2 = input_password2
        
    # Create an instance of the user class and fill it with the submitted form's data
    user = User(input_email, input_username, input_password, input_password2)

    return render_template("mypage.html", website_title=website_title)
