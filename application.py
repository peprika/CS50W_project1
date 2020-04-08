import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

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

    # SIGN UP A NEW USER
    # This is assuming you come from submitting the Signup Form
    # TODO: How to differentiate between login/signup form submissions?
    
    # Collect info from the sign up form
    input_email = request.form.get("email")
    input_username = request.form.get("username")
    input_password = request.form.get("password")
    input_password2 = request.form.get("password2")
    
    # Create user class
    class User:
        def __init__(self, email, username, password, password2):
            self.email = input_email
            self.username = input_username
            self.password = input_password
            self.password2 = input_password2
        
    # Create an instance of the user class and fill it with the submitted form's data
    user = User(input_email, input_username, input_password, input_password2)            

    return render_template("mypage.html", website_title=website_title)
