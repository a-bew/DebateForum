from logging import error
import mysql.connector
from config import credentials
from datetime import datetime

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
            c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            c.execute('''DROP TABLE IF EXISTS Users;''')
            c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

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
                password TEXT NOT NULL,
                email TEXT NOT NULL
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

    def checkAlreadyExist(self, username):
            c, conn = create_connection()
            #conn.text_factory = bytes

            with conn:
                c.execute("SELECT username FROM Users WHERE username = %s", username)
                result = c.fetchone()

                if result:
                    return True
                else:
                    return False    

    def insert_user(self, username, password, email):
            c, conn = create_connection()

            """
            insert user, 
            :param username:
            :param password:
            :param email:
            :return: True
            """
            createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            conn.text_factory = bytes

            with conn:
                c.execute('INSERT INTO Users (createdAt, updatedAt, username, password, email) VALUES (%s, %s, %s, %s, %s)', (createdAt, updatedAt, username, password, email))        
                conn.commit()
            print("User signed-up successfully")
            return True

    def get_password(self, username):        
        c, conn = create_connection()
        #conn.text_factory = bytes

        with conn:
            c.execute("SELECT password FROM users WHERE username = ?", username)
            result = c.fetchone()
            return result

    def getUser(self, username):
        c, conn = create_connection()
        #conn.text_factory = bytes

        with conn:
            c.execute("SELECT * FROM users WHERE username = ?", username)
            result = c.fetchone()
            return result

    def getUserTopics(self, user_id):
        c, conn = create_connection()

        with conn:
            c.execute(
                ''' SELECT U.id AS user_id, U.username AS user_name, T.topic AS topic_name, T.id AS topic_id 
                    FROM Users U LEFT JOIN Topics T ON U.id = T.user_id
                    WHERE T.user_id = user_id; 
                ''') 

            myresult = c.fetchone()
            return myresult

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

    # One to many relationship
    def topic_claims(self, topicId):
        c, conn = create_connection()

        with conn:
            c.execute(
                ''' SELECT T.id AS topic_id, T.username AS user_name, T.createdAt AS topic_createdAt, C.id AS claim_id, C.user_id as user_id 
                    FROM Topics T 
                    LEFT JOIN Claims C ON T.id = C.topic_id
                    GROUP BY C.user_id, C.topic.id,
                    WHERE C.topic_id = topicId; 
                ''') 

            myresult = c.fetchone()
            return myresult
            
            
# class UserTopics:
#     def __init__(self):
#         self.create_table()

#     def create_table(self):
#         """
#         create table Topic, Topic is a child or subset of forum
#         this table use composite primary key (user_id, topic_id)
#         """
#         c, conn = create_connection()

#         # conn = create_connection(db_name)
#         #conn.text_factory = bytes

#         with conn:

#             c.execute(
#                 ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'TopicUsers') ''')
#             # if the count is 1, then table exists
#             if c.fetchone()[0] > 0:
#                 #print('Table exists.')
#                 return True

#             c.execute('''CREATE TABLE TopicUsers (
#                     PRIMARY KEY (user_id, topic_id),
#                     user_id INTEGER NOT NULL,
#                     topic_id INTEGER NOT NULL,
#                     createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#                     updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    
#                     CONSTRAINT Constr_TopicUsers_Users_fk
#                         FOREIGN KEY (user_id) REFERENCES Users (id)
#                         ON DELETE CASCADE ON UPDATE CASCADE,

#                     CONSTRAINT Constr_TopicUsers_Topics_fk
#                         FOREIGN KEY (topic_id) REFERENCES Topics (id)
#                         ON DELETE CASCADE ON UPDATE CASCADE
#                 );
#             ''')

#             print("TopicUsers Table created successfully")

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

    # Many to many relationship
    # def getClaimTopics(self, topic_id):
    #     c, conn = create_connection()

    #     with conn: 
    #         c.execute(
    #             '''
    #                 SELECT T.id, T.email, T.username, C.id AS claim_id, C.name AS claim_name
    #                 FROM Topic T 
    #                 JOIN user_roles on (user.id=user_roles.user_id)
    #                 JOIN role on (role.id=user_roles.role_id);
    #             '''
    #         )

    


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
                        FOREIGN KEY (claim_id) REFERENCES Claims (id)
                        ON DELETE RESTRICT ON UPDATE CASCADE,

                    CONSTRAINT Constr_ClaimTag_Tag_fk
                        FOREIGN KEY (tag_id) REFERENCES Tags (id)
                        ON DELETE RESTRICT ON UPDATE CASCADE,
                        
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
