## To set flask to listen for changes do the following

export FLASK_ENV=development
export FLASK_APP=server.py

## Set up version control

$ git config --global user.name "Your Name"
$ git config --global user.email "you@youraddress.com"
$ git config --global push.default matching
$ git config --global alias.co checkout
$ git init

## Install MySQL locally - use the following links to get started

Mac installation guide; https://flaviocopes.com/mysql-how-to-install/

Utuntu 20.4 installation guide; https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04?fbclid=IwAR0Y3ocKmn8srWdlxb3IbutqDyuV2UGvh_NTCoFZS2vu-AhulcyCtx8myRU

## Create MySQL db on using the following lines of code

```
    import mysql.connector

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password123",
        auth_plugin='mysql_native_password'
    )

    my_cursor = mydb.cursor()

    my_cursor.execute("CREATE DATABASE DebateForumDB")

    my_cursor.execute("SHOW DATABASES")

    for db in my_cursor:
        print(db)
```
