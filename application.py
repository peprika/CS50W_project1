import os

from flask import Flask, session, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

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

    # Check if the user is logging or signing up
    form_type = request.form.get("form_type")
    if form_type == "login":
        #TODO: LOG THE USER IN
        input_username = request.form.get("username")
        input_password = request.form.get("password")

    if form_type == "signup":
        # REGISTER A NEW USER
        
        # Collect info from the signup form
        input_email = request.form.get("email")
        input_username = request.form.get("username")
        input_password = request.form.get("password")
        input_password2 = request.form.get("password2")
        
        if input_password != input_password2:
            return render_template("error.html", error_msg="Username already taken.")

        # Create the User class
        class User(db.Model):
            __tablename__ = "users"
            id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
            email = db.Column(db.String, nullable=False)
            username = db.Column(db.String, nullable=False) 
            password = db.Column(db.String, nullable=False)

        # Create an instance of the user class and fill it with the submitted form's data
        user = User(email=input_email, username=input_username, password=input_password)

        # Write the new user info to db
        db.session.add(user)
        db.session.commit()
    
    return render_template("mypage.html", website_title=website_title)
