from os import error
from flask import Flask, render_template, flash, request, jsonify, session, g, redirect
from flask.helpers import url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateTimeField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from db_script import mysql_connect
from functools import wraps

# Create a Flask instance
app = Flask(__name__)

# SECRET KEY
app.config['SECRET_KEY'] = "my super secret"

# DATABASE IS CREATED IF NOT EXIST
mysql_connect.create_mysql_db()

# DB TABLES ARE CREATED IF NOT EXIST
mysql_connect.AdminsTable()

UserAuth = mysql_connect.UserAuth()
mysql_connect.TopicTable()
# mysql_connect.UserTopics()
mysql_connect.ClaimTable()
mysql_connect.Replies()
mysql_connect.ReReplies()
mysql_connect.TagTable()
mysql_connect.ClaimTagTable()

class Users():
    def __init__(self) -> None:
        self.username = None
        self.password_hash = None
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    def __repr__(self) -> str:
        return f"<Name {self.username}>"

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class TopicForm(FlaskForm):
    topic = StringField("Add New Topic", validators=[DataRequired()])
    name = StringField("Add New Topic", validators=[DataRequired()])
    time = DateTimeField(validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = UserAuth.getUser(session['user_id'])
        print("user", user)
        g.user = user

@app.route('/')
def index():
    if g.user:
        user = g.user
    else:
        user = None
    first_name = "john"
    stuff = "This is <strong>Bold</strong> text"
    favorite_pizza = ["Pepperani", "Cheese", "Orange", "Onions", 41]

    return render_template("index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza, user= user)
    # return jsonify({})

@app.route('/login/', methods=["GET", "POST"])
def login_page():
    error = ''
    
    # if request.method == 'POST':
    if request.json:
        session.pop('user_id', None)
        incoming_data = request.json

        username = incoming_data["username"]
        password = incoming_data['password']

        
            #Query the database to get password
        user_name = (username,)
        hashed_password = UserAuth.get_password(user_name)
        if hashed_password and check_password_hash(hashed_password, password):
            session["user_id"] = user_name
            return redirect(url_for('/'))
        return  redirect(url_for('login'))
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register_page():
    try:
        print(request)
        if request.method == 'POST':
            incoming_data = request.json
            username = incoming_data["username"]
            password = incoming_data['password']
            email = incoming_data['email']
            print(password, username, email)
            user_name = (username,)

        # Check if user already exist in db
        if UserAuth.checkAlreadyExist(user_name):
            return jsonify({"msg": "Username already exist!"}), 302

        user = Users()
        user.password = password
        hashed_password = user.password_hash

        status = UserAuth.insert_user(username, hashed_password, email)

        if status: return jsonify({"msg": "Signup successful"}), 201

        return jsonify({"msg": "Signup Fail!"}), 404

        # return render_template("login.html", error = error)
    except Exception as e:
        # return render_template("login.html", error = error)
        return jsonify({error: e.with_traceback()}), 500


    # mysql_connect.create_connection()
    # return ("okay")
# Create a form class


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Invalid URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Create Topic Page


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    topic = None
    form = TopicForm()
    # validate Form
    if form.validate_on_submit():
        topic = form.topic.data
        form.topic.data = ''
        flash("Form Submitted Successfully")

    return render_template("topic.html", topic=topic, form=form)
