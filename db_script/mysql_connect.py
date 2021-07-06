from logging import error
import mysql.connector
from config import credentials

databaseSet = "DebateForumDB"

mysql_credentials = credentials.db_credentials


def create_mysql_db():
    try:
        [host, user, passd, database] = mysql_credentials
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=passd,
            auth_plugin='mysql_native_password'
        )
        my_cursor = mydb.cursor()
        my_cursor.execute("CREATE DATABASE IF NOT EXISTS DebateForumDB")
        my_cursor.execute("SHOW DATABASES")
        for db in my_cursor:
            print(db)

    except error:
        print(error)


def create_connection():

    host, user, passd, db = mysql_credentials

    """ create a database connection to the MSQLite database
        specified by the db_file
    :param host: database host
    :param user: database user
    :param passd: database password
    :return: Cursor object, Connection object or None
    """
    try:
        conn = mysql.connector.connect(
            host=host, user=user, password=passd, database=databaseSet)
        c = conn.cursor()
        return c, conn
    except error as er:
        print(er)

    return None


class AdminsTable:
    def __init__(self):
        self.create_table()
        print("-------Working")

    def create_table(self):
        """
        create table Forum, Forum can add topics

        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Admins') ''')
            # if the count is 1, then table exists
            # print("count(*)", cursor)
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute(''' CREATE TABLE Admins (
                id INTEGER NOT NULl AUTO_INCREMENT,
                createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                name TEXT,
                PRIMARY KEY (id)
            );''')

            print("users Table created successfully")


class UserAuth:
    '''
        user can create accounts with a name and password and post messages
    '''

    def __init__(self):
        self.create_table()

    def create_table(self):
        """
        create table UserAuth, 

        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Users') ''')
            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute(''' CREATE TABLE Users (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                username VARCHAR(100) NOT NULL,
                password TEXT
            );''')

            # conn.execute('''
            #     CREATE TABLE IF NOT EXISTS users
            #     (
            #         user_id INTEGER PRIMARY KEY,
            #         username TEXT,
            #         password TEXT,
            #         online INTEGER,
            #         onlineAt DATETIME,
            #         created DATETIME DEFAULT CURRENT_TIMESTAMP );'''
            # )
            print("users Table created successfully")


class TopicTable:
    def __init__(self):
        self.create_table()

    def create_table(self):
        """
        create table Topic, Topic is a child or subset of forum

        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Topics') ''')
            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE Topics (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    user_id INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    topic VARCHAR(200) NOT NULL,
                    CONSTRAINT Constr_Topics_Users_fk
                        FOREIGN KEY (user_id) REFERENCES Users (id)
                );
            ''')

            print("Topics Table created successfully")


class TopicUsers:
    def __init__(self):
        self.create_table()

    def create_table(self):
        """
        create table Topic, Topic is a child or subset of forum
        this table use composite primary key (user_id, topic_id)
        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'TopicUsers') ''')
            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE TopicUsers (
                    PRIMARY KEY (user_id, topic_id),
                    user_id INTEGER NOT NULL,
                    topic_id INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    
                    CONSTRAINT Constr_TopicUsers_Users_fk
                        FOREIGN KEY (user_id) REFERENCES Users (id)
                        ON DELETE CASCADE ON UPDATE CASCADE,

                    CONSTRAINT Constr_TopicUsers_Topics_fk
                        FOREIGN KEY (topic_id) REFERENCES Topics (id)
                        ON DELETE CASCADE ON UPDATE CASCADE
                );
            ''')

            print("TopicUsers Table created successfully")


class ClaimTable:
    '''
        claims(messages) are linked to topics
        claim(s) is(are) posted by users
        claims has one or more replies
    '''

    def __init__(self):
        self.create_table()

    def create_table(self):
        """
        create table Claims, 
        Each Claim Has a heading message(topic_id)

        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        # FOREIGN KEY (user_id) REFERENCES Users (id)
        # FOREIGN KEY (topic_id) REFERENCES Topics (id)

        with conn:
            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Claims') ''')
            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE Claims (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    user_id INTEGER NOT NULL,
                    topic_id INTEGER NOT NULL,  
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    heading VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    CONSTRAINT Constr_Claims_TopicUsers_fk
                        FOREIGN KEY (user_id, topic_id) REFERENCES TopicUsers
                            (user_id, topic_id)
                );
            ''')

            print("Claims Table created successfully")


class TagTable:

    def __init__(self):
        self.create_table()

    def create_table(self):
        """
        create table Tags, 

        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Tags') ''')
            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute(''' CREATE TABLE Tags (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                Title Text NOT NULL
            );''')

            # conn.execute('''
            #     CREATE TABLE IF NOT EXISTS users
            #     (
            #         user_id INTEGER PRIMARY KEY,
            #         username TEXT,
            #         password TEXT,
            #         online INTEGER,
            #         onlineAt DATETIME,
            #         created DATETIME DEFAULT CURRENT_TIMESTAMP );'''
            # )
            print("Tags Table created successfully")


class ClaimTagTable:
    def __init__(self):
        self.create_table()

    def create_table(self):
        """
        create table Topic, Topic is a child or subset of forum
        this table use composite primary key (user_id, topic_id)
        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'ClaimTags') ''')
            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE ClaimTags (
                    PRIMARY KEY (claim_id, tag_id),
                    claim_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    
                    CONSTRAINT Constr_ClaimTag_Claim_fk
                        FOREIGN KEY (claim_id) REFERENCES Claims (id),

                    CONSTRAINT Constr_ClaimTag_Tag_fk
                        FOREIGN KEY (tag_id) REFERENCES Tags (id)
                        
                );
            ''')

            print("ClaimTags Table created successfully")


class Replies:
    def __init__(self):
        self.create_table()

    def create_table(self):
        """
            create table MessagesTable, 
            Each Reply Has a user(user_id) and claim(claim_id)

        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:
            c.execute('''DROP TABLE IF EXISTS Replies;''')
            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Replies') ''')

            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE Replies (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    claim_id INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                    
                    type ENUM('CLARIFICATION', 'SUPPORTING ARGUMENT', 'COUNTERARGUMENT'),
                    reply_text TEXT NOT NULL,
                    FOREIGN KEY (claim_id) REFERENCES Claims (id)
                );
            ''')

            print("Replies Table created successfully")


class ReReplies:
    def __init__(self):
        self.create_table()

    def create_table(self):
        """
            create table MessagesTable, 
            Each Reply Has a user(user_id) and claim(claim_id)

        """

        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:
            c.execute('''DROP TABLE IF EXISTS ReReplies;''')
            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'ReReplies') ''')

            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE ReReplies (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    reply_id INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                    
                    type ENUM('EVIDENCE', 'SUPPORT', 'REBUTTAL'),
                    re_reply_text TEXT NOT NULL,
                    FOREIGN KEY (reply_id) REFERENCES Claims (id)
                );
            ''')

            print("ReReplies Table created successfully")
