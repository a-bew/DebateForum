from os import error
from flask import Flask, render_template, flash, request, jsonify, session, g, redirect
from flask.helpers import url_for
from flask.json import tag
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
TopicTable = mysql_connect.TopicTable()
# mysql_connect.UserTopics()
ClaimTable = mysql_connect.ClaimTable()
Replies = mysql_connect.Replies()
ReReplies = mysql_connect.ReReplies()
TagTable = mysql_connect.TagTable()
ClaimTagTable = mysql_connect.ClaimTagTable()


class Users():
    def __init__(self, id=None, createdAt=None, updatedAt=None, username=None, email=None, password_hash=None) -> None:
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.username = username
        self.email = email
        self.password_hash = password_hash

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
        try:
            user = UserAuth.getUser((session['user_id'],))
            print("user before", user)
            user = Users(*user)
            print("user after", user)
            g.user = user
        except:
            pass


@app.route('/log-out', methods=['GET', 'POST'])
def logout():
    print('logging out workin')
    session.pop('user_id', None)
    return redirect(url_for("index"))


@app.route('/', methods=["GET", "POST"])
def index():
    print('logging out1----')

    # if g.user:
    #     user = g.user
    #     return redirect(url_for('user'))

    first_name = "john"
    stuff = "This is <strong>Bold</strong> text"
    topics = [{'topic': "Python", 'description': 'Learn Python'}, {'topic': "Python", 'description': 'Learn Python'}, {
        'topic': "Python", 'description': 'Learn Python'}, {'topic': "Python", 'description': 'Learn Python'}]
    error = ''

    all_topics = TopicTable.get_all_topic()
    # try:
    if request.method == 'POST':
        session.pop('user_id', None)
        # incoming_data = request.form
        # print(incoming_data)
        username = request.form["username_login"]
        password = request.form['password_login']

        # Query the database to get password
        user_name = (username,)
        hashed_password = UserAuth.get_password(user_name)[0]

        if hashed_password and check_password_hash(hashed_password, password):
            user_id = UserAuth.get_id(user_name)[0]
            session["user_id"] = user_id
            return redirect(url_for("index"))
        else:
            error = "Invalid credentials. Try Again."
        return render_template("index.html", first_name=first_name, stuff=stuff, topics=topics, error=error)

    return render_template("index.html", first_name=first_name, stuff=stuff, topics=all_topics)


@app.route('/add-topic', methods=["GET", "POST"])
def add_topic():
    error = ''

    if request.method == 'POST':
        # incoming_data = request.form
        user_id = session["user_id"]
        topic = request.form.get("add_topic_subject", False)
        description = request.form.get("add_topic_description", False)
        print(user_id, topic, description)
        # Query the database to get password
        result = TopicTable.insert_topic(user_id, topic, description)
        if result:
            flash("Form Submitted Successfully")
            return redirect(url_for("index"))
        else:
            error = "Topic not added successfully"
        return render_template("add_topic.html", error=error)
    return render_template("add_topic.html")


@app.route('/postreply', methods=["GET", "POST"])
def postAReply():

    try:
        error = ""
        if request.method == 'POST':
            incoming_data = request.json
            claim_id = incoming_data["claim_id"]
            from_user = incoming_data['from_user']
            to_user = incoming_data['to_user']
            type = incoming_data['type']
            reply_text = incoming_data['reply_text']
            print(claim_id, from_user, to_user, type, reply_text)

            # Check if user already exist in db
            # if UserAuth.checkAlreadyExist(user_name):
            response = Replies.insert_replies(
                claim_id, from_user, type, reply_text)
            if response:
                flash("Form Submitted Successfully")
                # return redirect(url_for("index"))
                return jsonify({"message": "Form Submitted Successfully", "data": response}), 200
            else:
                error = "Reply not added successfully"
            return jsonify({"message": error}), 500
        return jsonify({"msg": "Something went wrong"}), 500
    except Exception as e:
        return jsonify({error: e.with_traceback()}), 500

# 
@app.route('/postrereply', methods=["GET", "POST"])
def postRereplies():
    try:

        error = ""
        if request.method == 'POST':
            incoming_data = request.json
            reply_id = incoming_data["reply_id"]
            from_user = incoming_data['from_user']
            to_user = incoming_data['to_user']
            type = incoming_data['re_reply_type']
            re_reply_text = incoming_data['re_reply_text']
            print(reply_id, from_user, to_user, type, re_reply_text)

            # Check if user already exist in db
            # if UserAuth.checkAlreadyExist(user_name):
            response = ReReplies.insert_re_replies(
                reply_id, from_user, type, re_reply_text)
            if response:
                flash("Form Submitted Successfully")
                # return redirect(url_for("index"))
                return jsonify({"message": "Form Submitted Successfully", "data": response}), 200
            else:
                error = "ReReply not added successfully"
            return jsonify({"message": error}), 500
        return jsonify({"msg": "Something went wrong"}), 500
    except Exception as e:
        return jsonify({error: e.with_traceback()}), 500


@app.route('/get-rereply-for-reply', methods=['GET', "POST"])
def getReRepliesForReply():

    try:
        # claim_id, from_user, to_user, type, reply_text
        incoming_data = request.json
        reply_id = incoming_data["id"]
        # topic_id = request.args.get('topic_id')
        print("reply_id", reply_id)
        replies = ReReplies.get_rereplies_to_replay(reply_id)
        if replies:
            flash("Form Submitted Successfully")
            # return redirect(url_for("index"))
            return jsonify({'data': replies, "message": "Form Submitted Successfully"}), 200
        else:
            error = "Reply not added retrieved"
        return jsonify({"message": error}), 500

    except:
        return jsonify({error: e.with_traceback()}), 500

@app.route('/get-replies-for-claims', methods=["GET", "POST"])
def getRepliesForClaims():

    try:
        # claim_id, from_user, to_user, type, reply_text
        incoming_data = request.json
        claim_id = incoming_data["id"]
        # topic_id = request.args.get('topic_id')
        print("claim_id", claim_id)
        replies = Replies.get_replies_to_claim(claim_id)
        if replies:
            flash("Form Submitted Successfully")
            # return redirect(url_for("index"))
            return jsonify({'data': replies, "message": "Form Submitted Successfully"}), 200
        else:
            error = "Reply not added retrieved"
        return jsonify({"message": error}), 500

    except:
        return jsonify({error: e.with_traceback()}), 500


@app.route('/topic', methods=["GET", "POST"])
def show_single_topic():
    # return ('you asked for question{0}'.format(topic_id))
    # user_id = session["user_id"]
    # topic_id = topic_id

    # claim_id, from_user, to_user, type, reply_text
    author_id = request.args.get('user_id')
    topic_id = request.args.get('topic_id')
    topic = request.args.get('topic')

    print("author_id, user_id", author_id, session["user_id"])

    # Query the database to get claims related to topic from a single user
    result = ClaimTable.get_claim_by_topic(topic_id)  # user_id,
    selectedTags = ClaimTable.getTags(topic_id, author_id)  # current_user_id,

    print('selectedTags', selectedTags)
    if request.method == 'POST':
        # incoming_data = request.form
        user_id = session["user_id"]
        claim_heading = request.form.get("claim_heading", False)
        claim_message = request.form.get("claim_message", False)
        claim_tags = request.form.get("claim_tags", False)

        print(claim_heading, claim_message, claim_tags)
        # Query the database to get password
        tags = claim_tags.strip().split(",")

        resultId = ClaimTable.insert_claim(
            user_id, topic_id, claim_heading, claim_message)

        done = False
        if (tags):
            for tag in tags:
                tagId = TagTable.insert_tag(tag)
                print(resultId, tagId)
                ClaimTagTable.insert_claim_tag(tagId, resultId)
                done = True
            # claim_tags
        else:
            done = True

        if done:
            flash("Form Submitted Successfully")
            return redirect(url_for("index"))
        else:
            error = "Topic not added successfully"
        return render_template("add_topic.html", error=error)

    return render_template("list_claims.html", claims=result, topic=topic, selectedTags=selectedTags, author_id=int(author_id))


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

        if status:
            return jsonify({"msg": "Signup successful"}), 201

        return jsonify({"msg": "Signup Fail!"}), 404

        # return render_template("login.html", error = error)
    except Exception as e:
        # return render_template("login.html", error = error)
        return jsonify({error: e.with_traceback()}), 500

    # mysql_connect.create_connection()
    # return ("okay")
# Create a form class


# @app.route('/user/<name>')
# def user(name):
#     return render_template("user.html", user_name=name)

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
