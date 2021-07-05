## To set flask to listen for changes do the following
```
    export FLASK_ENV=development
    export FLASK_APP=server.py

```
## Set up version control

> git config --global user.name "Your Name"
> git config --global user.email "you@youraddress.com"
> git config --global push.default matching
> git config --global alias.co checkout
> git init

## Install MySQL locally - use the following links to get started

Mac/Ubuntu installation guide; https://flaviocopes.com/mysql-how-to-install/

## Additional Useful MySQL command for mac
`
    sudo chown -R \_mysql:mysql /usr/local/var/mysql
`
## Start Mysql Server - 
`
    sudo mysql.server start
`
## Access Mysql command on the terminal 
`
    sudo mysql -u root -p
`
## Connect to mysql database
```
    pip install mysql-connector-python
```
## Create MySQL db from terminal using the following lines of code

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