from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# Create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret"

# Create a form class
class NamerForm(FlaskForm):
    name = StringField("What is your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")
#safe
#capitalize
#lower
#upper
#title
#trim
# striptags

# Create a route decorator
@app.route('/')
def index():
    first_name = "john"
    stuff = "This is <strong>Bold</strong> text"

    favorite_pizza = ["Pepperani", "Cheese", "Orange", "Onions", 41]
    return render_template("index.html", first_name=first_name, stuff = stuff, favorite_pizza=favorite_pizza)

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
