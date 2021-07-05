from os import error
from flask import Flask, render_template, flash, request
from flask.helpers import url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateTimeField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from db import mysql_connect
from config import credentials

# Create a Flask instance
app = Flask(__name__)

# SECRET KEY
app.config['SECRET_KEY'] = "my super secret"

# DATABASE IS CREATED IF NOT EXIST
mysql_connect.create_mysql_db()

# DB TABLES ARE CREATED IF NOT EXIST
mysql_connect.AdminsTable()
mysql_connect.UserAuth()
mysql_connect.TopicTable()
mysql_connect.TopicUsers()
mysql_connect.ClaimTable()
mysql_connect.Replies()


class TopicForm(FlaskForm):
    topic = StringField("Add New Topic", validators=[DataRequired()])
    name = StringField("Add New Topic", validators=[DataRequired()])
    time = DateTimeField(validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a route decorator


@app.route('/')
def index():
    first_name = "john"
    stuff = "This is <strong>Bold</strong> text"

    favorite_pizza = ["Pepperani", "Cheese", "Orange", "Onions", 41]
    return render_template("index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza)


@app.route('/login/', methods=["GET", "POST"])
def login_page():
    error = ''
    try:
        if request.method == 'POST':
            attempted_username = request.form["username"]
            attempted_password = request.form['password']

            if attempted_username == 'admin' and attempted_password == 'password':
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid credentials. Try Again"

        return render_template("login.html", error=error)
    except Exception as e:
        return render_template("login.html", error=error)


@app.route('/register/', methods=["GET", "POST"])
def register_page():
    return ("okay")
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
