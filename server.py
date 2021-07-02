from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateTimeField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

# Create a Flask instance
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'DebateForumDB'

# SECRET KEY
app.config['SECRET_KEY'] = "my super secret"

# Initialize the db
db = MySQL(app)

# Creating a connection cursor
# cursor = db.connection.cursor()

# Create a form class


class TopicForm(FlaskForm):
    topic = StringField("Add New Topic", validators=[DataRequired()])
    author = IntegerField("Add New Topic", validators=[DataRequired()])
    time = DateTimeField(validators=[DataRequired()])
    submit = SubmitField("Submit")


class TopicForm(FlaskForm):
    topic = StringField("Add New Topic", validators=[DataRequired()])
    name = StringField("Add New Topic", validators=[DataRequired()])
    time = DateTimeField(validators=[DataRequired()])
    submit = SubmitField("Submit")

# safe
# capitalize
# lower
# upper
# title
# trim
# striptags

# Create a route decorator


@app.route('/')
def index():
    first_name = "john"
    stuff = "This is <strong>Bold</strong> text"

    favorite_pizza = ["Pepperani", "Cheese", "Orange", "Onions", 41]
    return render_template("index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza)


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
