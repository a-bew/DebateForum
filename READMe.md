## To set flask to listen for changes do the following

```
    export FLASK_ENV=development
    export FLASK_APP=server.py

```

## Set up version control

```
 git config --global user.name "Your Name"
 git config --global user.email "you@youraddress.com"
 git config --global push.default matching
 git config --global alias.co checkout
 git init
```

## Install MySQL locally - use the following links to get started

Mac/Ubuntu installation guide; https://flaviocopes.com/mysql-how-to-install/

## Additional Useful MySQL command for mac

` sudo chown -R \_mysql:mysql /usr/local/var/mysql`

## Start Mysql Server -

` mysql.server start`

## Access Mysql command on the terminal

` sudo mysql -u root -p`

## Connect to mysql database

```
    pip install mysql-connector-python
```

# Config file format (config/credential.py)

```
    mysql_host="localhost",
    mysql_user="root",
    mysql_password="password",
    mysql_database = "database"
    db_credentials =  ["localhost", 'root', "password", "database_name"]
```

# How to start mysql service

```
    Ubuntu:

        mysql.server start

    And if you are on a mac and used brew to install mysql, simply use:

        brew services start mysql

```

# MYSQL Tables Relations

```
    Table: Admins
    Columns: id(pk), name

    Table: Users
    Columns: id(pk), createdAt, updatedAt, username, password, email

    Table: Topics
    Columns: id(pk), createdAt, updatedAt, user_id(fk), topic, description

    <!-- Table: TopicUsers
    Columns: (user_id, topic_id)(pk), createdAt, updatedAt, user_id(fk), user_id(fk) -->

    Table: Claims
    Columns: id(pk), createdAt, updatedAt, (user_id, topic_id)(fk), heading, message

    Table: Tag
    Columns: id(pk), Title

    Table: ClaimTag
    Columns: (claim_id, tag_id)(pk), createdAt, updatedAt, claim_id(fk), tag_id(fk)

    NB: Claims can be related to another(one or more) as opposed to equivalent

    Table: Replies
    Columns: id(pk), createdAt, updatedAt, type(ENUM), reply_text, (claim_id)(fk)

    Table: ReReplies
    Columns: id(pk), createdAt, updatedAt, type(ENUM), re_reply_text, (reply_id)(fk)

```

# Wireframing

'''
To draw your wireframes you can use the draw.io service, it’s free.
'''
