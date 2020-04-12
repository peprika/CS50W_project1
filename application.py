import os

from flask import Flask, session, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import re

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

# Create the User class
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False) 
    password = db.Column(db.String, nullable=False)
    

@app.route("/")
def index():
    return render_template("index.html", website_title=website_title)
	
@app.route("/signup", methods=["GET"])
def signup():
        return render_template("signup.html", website_title=website_title)


@app.route("/mypage", methods=["POST"])
def mypage():

    # Check if the user is logging or signing up
    form_type = request.form.get("form_type")
    if form_type == "login":
        #TODO: LOG THE USER IN
        input_username = request.form.get("username")
        input_password = request.form.get("password")
        
        # Check that the username exists:
        username_exists = db.session.query(db.exists().where(User.username == input_username)).scalar()
        if username_exists:
            print("USERNAME FOUND")
        else:
            return render_template("error.html", error_msg="The username does not exist. Go back and try again.")

    if form_type == "signup":
        # REGISTER A NEW USER
        
        # Collect info from the signup form
        input_email = request.form.get("email")
        input_username = request.form.get("username")
        input_password = request.form.get("password")
        input_password2 = request.form.get("password2")
        
        # Check that form info is valid
        email_regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if (re.search(email_regex, input_email)) is None:
            return render_template("error.html", error_msg="The email is invalid. Please go back and check you typed it correctly.")
        if len(input_email) > 320:
            return render_template("error.html", error_msg="The email is too long. Use max 320 characters.")
        if len(input_username) > 16:
            return render_template("error.html", error_msg="The username is too long. Use max 16 characters.")
        if input_password != input_password2:
            return render_template("error.html", error_msg="The passwords do not match. Go back and try again.")
        
        # Check that the email and username are available
        email_exists = db.session.query(db.exists().where(User.email == input_email)).scalar()
        username_exists = db.session.query(db.exists().where(User.username == input_username)).scalar()
        if email_exists:
            return render_template("error.html", error_msg="This email has already been registered. Go back and try again.")
        if username_exists:
            return render_template("error.html", error_msg="Username already exists. Go back and try again.")
        
        # Hash the password
        pw_hash = generate_password_hash(input_password, method='pbkdf2:sha256', salt_length=8)
        
        # Create an instance of the user class and fill it with the submitted form's data
        user = User(email=input_email, username=input_username, password=pw_hash)

        # Write the new user info to db
        db.session.add(user)
        db.session.commit()
    
    return render_template("mypage.html", website_title=website_title)
