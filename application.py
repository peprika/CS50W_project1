import os

from flask import Flask, session, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import re

app = Flask(__name__)
app.secret_key = "super secret key"

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
    
# Create the Book class
class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False) 
    year = db.Column(db.Integer, nullable=False)

# Create the Review class
class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    isbn = db.Column(db.String, nullable=False) 
    rating = db.Column(db.Integer, nullable=False)
    

@app.route("/")
def index():
    return render_template("index.html", website_title=website_title)
	
@app.route("/signup", methods=["GET"])
def signup():
        return render_template("signup.html", website_title=website_title)

@app.route("/mypage", methods=["GET", "POST"])
def mypage():

    # There are 3 ways the user can reach mypage.html: 1) GET 2) POST (logging in), and 3) POST (signing up)
    # GET: Check if user is logged in; if yes, allow to view mypage
    if request.method == "GET":
        if not session:
            return render_template("index.html", website_title=website_title)
        else:
            user_info = db.session.query(User).filter(User.username == session["username"]).first()
            return render_template("mypage.html", website_title=website_title, user_info=user_info)
    
    # POST: Check if the user is logging or signing up
    if request.method == "POST":
        session.clear()
        form_type = request.form.get("form_type")
        
        if form_type == "login":
            # LOG THE USER IN
            
            # Get the login form data
            input_username = request.form.get("username")
            input_password = request.form.get("password")
            
            # Check that the username exists
            username_exists = db.session.query(db.exists().where(User.username == input_username)).scalar()
            if username_exists:
            
                # Check that the password is correct
                user_info = db.session.query(User).filter(User.username == input_username).first()
                if check_password_hash(user_info.password, input_password):
                    # Log the user in, and redirect to mypage.html
                    session["username"] = input_username
                    return render_template("mypage.html", website_title=website_title, user_info=user_info)
                else:
                    return error_page("Incorrect password. Go back and try again.")
            else:
                return error_page("The username does not exists. Go back and try again.")

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
                return error_page("The email is invalid. Please go back and check you typed it correctly.")
            if len(input_email) > 320:
                return error_page("The email is too long. Use max 320 characters.")
            if len(input_username) > 16:
                return error_page("The username is too long. Use max 16 characters.")
            if input_password != input_password2:
                return error_page("The passwords do not match. Go back and try again.")
            
            # Check that the email and username are available
            email_exists = db.session.query(db.exists().where(User.email == input_email)).scalar()
            username_exists = db.session.query(db.exists().where(User.username == input_username)).scalar()
            if email_exists:
                return error_page("This email has already been registered. Go back and try again.")
            if username_exists:
                return error_page("Username already exists. Go back and try again.")
            
            # Hash the password
            pw_hash = generate_password_hash(input_password, method='pbkdf2:sha256', salt_length=8)
            
            # Create an instance of the user class and fill it with the submitted form's data
            user = User(email=input_email, username=input_username, password=pw_hash)

            # Write the new user info to db
            db.session.add(user)
            db.session.commit()
            
            # Log the user in, and redirect to mypage.html
            session["username"] = input_username
            return render_template("mypage.html", website_title=website_title)

@app.route("/logout", methods=["GET"])
def logout():
        session.clear()
        return render_template("logout.html", website_title=website_title)
        
def error_page(error_msg):
    return render_template("error.html", error_msg=error_msg)