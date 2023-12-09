import itertools
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

            # c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            # c.execute('''DROP TABLE IF EXISTS ClaimTags;''')
            # c.execute('''DROP TABLE IF EXISTS Users;''')
            # c.execute('''DROP TABLE IF EXISTS Topics;''')
            # c.execute('''DROP TABLE IF EXISTS Claims;''')
            # c.execute('''DROP TABLE IF EXISTS ClaimTags;''')
            # c.execute('''DROP TABLE IF EXISTS Replies;''')
            # c.execute('''DROP TABLE IF EXISTS ReReplies;''')

            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Admins') ''')
            # if the count is 1, then table exists
            # print("count(*)", cursor)
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            # c.execute(''' CREATE TABLE Admins (
            #     id INTEGER NOT NULl AUTO_INCREMENT,
            #     createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            #     updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            #     name TEXT,
            #     PRIMARY KEY (id)
            # );''')

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
            # c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            # c.execute('''DROP TABLE IF EXISTS Users;''')
            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

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
                username TEXT NOT NULL,
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

        # conn.text_factory = bytes

        with conn:
            c.execute('INSERT INTO Users (createdAt, updatedAt, password, email, username) VALUES (%s, %s, %s, %s, %s)',
                      (createdAt, updatedAt, password, email, username))
            conn.commit()
        print("User signed-up successfully")
        return True

    def get_password(self, username):
        c, conn = create_connection()
        #conn.text_factory = bytes

        with conn:
            # c.execute("SELECT * FROM Users")
            c.execute("SELECT password FROM Users WHERE username = %s", username)
            result = c.fetchone()

            # myresult = mycursor.fetchall()

            # for x in myresult:
            #     print(x)

            print(result)
            return result

    def get_id(self, username):
        c, conn = create_connection()

        with conn:
            c.execute("SELECT id FROM Users WHERE username = %s", username)
            result = c.fetchone()
            return result

    def getUser(self, id):
        c, conn = create_connection()
        #conn.text_factory = bytes

        with conn:
            c.execute("SELECT * FROM Users WHERE id = %s", id)
            result = c.fetchone()
            print("result", result)
            return result


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

            # c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            # c.execute('''DROP TABLE IF EXISTS Topics;''')
            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

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
                    topic Text NOT NULL,
                    description Text NOT NULL, 
                    CONSTRAINT Constr_Topics_Users_fk
                        FOREIGN KEY (user_id) REFERENCES Users (id)
                );
            ''')

            print("Topics Table created successfully")

    def insert_topic(self, user_id, topic, description):
        c, conn = create_connection()

        """
            insert user, 
            :param user_id:
            :param topic:
            :return: True
            """
        createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        conn.text_factory = bytes

        with conn:
            c.execute('INSERT INTO Topics (createdAt, updatedAt, user_id, topic, description) VALUES (%s, %s, %s, %s, %s)',
                      (createdAt, updatedAt, user_id, topic, description))
            conn.commit()
        print("New Topic added successfully")
        return True

    def get_all_topic(self):
        c, conn = create_connection()

        with conn:
            c.execute(
                ''' SELECT U.id AS user_id, U.username AS user_name, T.createdAt AS topic_createdAt, T.topic AS topic_name, T.description AS description, T.id AS topic_id 
                    FROM Users U LEFT JOIN Topics T ON U.id = T.user_id; 
                ''')
            desc = c.description
            myresult = c.fetchall()
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in myresult]
            print(data)
            return data

    def get_topic_by_user(self, user_id):
        c, conn = create_connection()

        with conn:
            c.execute(
                ''' SELECT U.id AS user_id, U.username AS user_name, T.topic AS topic_name, T.id AS topic_id 
                    FROM Users U LEFT JOIN Topics T ON U.id = T.user_id
                    WHERE T.user_id = %s; 
                ''', (user_id,))

            myresult = c.fetchall()
            print(myresult)
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

            # c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            # c.execute('''DROP TABLE IF EXISTS Claims;''')
            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

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
                    FOREIGN KEY (user_id) REFERENCES Users (id),                     
                    FOREIGN KEY (topic_id) REFERENCES Topics (id)
                );
            ''')

            print("Claims Table created successfully")

    def insert_claim(self, user_id, topic_id, claim_heading, claim_message):

        print("forign key constraint fails", user_id,
              topic_id, claim_heading, claim_message)
        c, conn = create_connection()

        createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # conn.text_factory = bytes

        with conn:
            c.execute('INSERT INTO Claims (createdAt, updatedAt, user_id, topic_id, heading, message) VALUES (%s, %s, %s, %s, %s, %s)',
                      (createdAt, updatedAt, user_id, topic_id, claim_heading, claim_message))
            conn.commit()
            print("Last Row Id", c.lastrowid)
            return c.lastrowid

    # def insert_tag(self, name):

    # def get_claim_by_topic(user_id, topic_id):
    #     pass

    # One to many relationship

    def get_claim_by_topic(self, topic_id):
        c, conn = create_connection()
        # with conn:
        #     c.execute('''
        #         SELECT T.id AS topic_id, C.id AS claim_id, C.user_id as user_id, C.heading AS claim_heading, C.message as claim_message
        #         FROM Topics T INNER JOIN CLAIM C
        #         ON T.id = C.topic_id
        #         WHERE C.user_id = user_id and C.topic_id = topic
        #     ''')

        with conn:
            c.execute(
                ''' SELECT T.id AS topic_id, C.id AS claim_id, C.user_id as user_id,
                    C.createdAt AS claim_createdAt, C.heading as claim_heading, C.message as claim_message
                    FROM Topics T 
                    LEFT JOIN Claims C ON T.id = C.topic_id
                    WHERE C.topic_id = %s; 
                ''', (topic_id, ))  # && C.user_id = %s  user_id

            desc = c.description
            myresult = c.fetchall()
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in myresult]
            print(data)
            return data
            # myresult = c.fetchone()
            # return myresult

    def getTags(self, topic_id, author_id):
        c, conn = create_connection()

        try:
            with conn:
                c.execute(
                    '''
                        SELECT C.id, T.id AS T_id, T.Title AS tagWord
                        FROM Claims C 
                        JOIN ClaimTags CT on (C.id=CT.claim_id)
                        JOIN Tags T on (T.id=CT.tag_id)
                        WHERE C.topic_id = %s && C.user_id = %s; 
                    ''', (topic_id, author_id)
                    # && C.user_id = %s  user_id,
                )

                desc = c.description
                myresult = c.fetchall()
                column_names = [col[0] for col in desc]
                data = [dict(zip(column_names, row)) for row in myresult]
                print(data)
                return data

        except:
            pass

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
            # c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            # c.execute('''DROP TABLE IF EXISTS Tags;''')
            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')
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
                Title TEXT NOT NULL
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

    def insert_tag(self, tag):

        c, conn = create_connection()

        createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        with conn:
            c.execute(
                '''INSERT INTO Tags (createdAt, updatedAt, Title) VALUES (%s, %s, %s);
                ''', (createdAt, updatedAt, tag)
            )

            conn.commit()
            print("Last Row Id", c.lastrowid)
            return c.lastrowid


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

            # c.execute('''ALTER TABLE ClaimTags
            # DROP FOREIGN KEY Constr_ClaimTag_Claim_fk;''')
            # c.execute('''ALTER TABLE ClaimTags
            # DROP FOREIGN KEY Constr_ClaimTag_Tag_fk;''')
            # c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            # c.execute('''DROP TABLE IF EXISTS ClaimTags;''')

            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'ClaimTags') ''')
            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE ClaimTags (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    claim_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (claim_id) REFERENCES Claims (id),
                    FOREIGN KEY (tag_id) REFERENCES Tags (id)
                        
                );
            ''')

            print("ClaimTags Table created successfully")

    def insert_claim_tag(self, tag_id, claim_id):
        print("tag_id,-------------------------- claim_id", tag_id, claim_id)
        c, conn = create_connection()

        createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        with conn:
            c.execute(
                '''INSERT INTO ClaimTags (createdAt, updatedAt, tag_id, claim_id) VALUES (%s, %s, %s, %s);
                ''', (createdAt, updatedAt, int(tag_id), int(claim_id))
            )

            conn.commit()
            print("Last Row Id", c.lastrowid)
            return c.lastrowid


class RepliesLinkingClaimsReReplies:
    def __init__(self):
        self.create_table()

    def create_table(self):
        """
            create table RepliesLinkingClaimsReReplies, 
        """
        c, conn = create_connection()

        # conn = create_connection(db_name)
        #conn.text_factory = bytes

        with conn:
            #             c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            #             c.execute('''DROP TABLE IF EXISTS Replies;''')
            #             c.execute('''ALTER TABLE Replies
            # DROP FOREIGN KEY from_user;''')
            #             c.execute('''ALTER TABLE Replies
            # DROP FOREIGN KEY claim_id;''')

            #             c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

            # c.execute('''DROP TABLE IF EXISTS Replies;''')
            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'RepliesLinkingClaimsReReplies') ''')

            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

            c.execute('''CREATE TABLE RepliesLinkingClaimsReReplies (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    claim_id INTEGER NOT NULL,
                    reply_id INTEGER,
                    rereply_id INTEGER,

                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                    

                    FOREIGN KEY (claim_id) REFERENCES Claims (id),
                    FOREIGN KEY (reply_id) REFERENCES Replies (id) on update SET NULL on delete SET NULL,
                    FOREIGN KEY (rereply_id) REFERENCES ReReplies (id) on update SET NULL on delete SET NULL
                );
            ''')

            print("Replies Table created successfully")

    def insert_claim_tag(self, reply_id, claim_id, rereply_id):

        print("tag_id,-------------------------- claim_id",
              reply_id, claim_id, rereply_id)

        c, conn = create_connection()

        createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        with conn:
            c.execute(
                '''INSERT INTO ClaimTags (createdAt, updatedAt, reply_id, claim_id, rereply_id) VALUES (%s, %s, %s, %s, %s);
                ''', (createdAt, updatedAt, reply_id, claim_id, rereply_id)
            )

            conn.commit()
            print("Last Row Id", c.lastrowid)
            return c.lastrowid

    def get_repliesLinking_claims_reReplies(self, claim_id):
        c, conn = create_connection()

        with conn:
            c.execute(
                ''' SELECT C.id AS claim_id, R.reply_text AS reply_text, R.type AS reply_type, R.from_user AS reply_authored_by, R.id AS reply_id
                    FROM Claims C 
                    LEFT JOIN RepliesLinkingClaimsReReplies RLCR ON C.id = RLCR.claim_id
                    LEFT JOIN Replies R ON RLCR.reply_id = R.id
                    JOIN ReReplies RR ON RLCR.reply_id = RR.id;
                ''', (claim_id,))

            desc = c.description
            myresult = c.fetchall()
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in myresult]
            print(data)
            return data


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
            #             c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            #             c.execute('''DROP TABLE IF EXISTS Replies;''')
            #             c.execute('''ALTER TABLE Replies
            # DROP FOREIGN KEY from_user;''')
            #             c.execute('''ALTER TABLE Replies
            # DROP FOREIGN KEY claim_id;''')

            #             c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

            # c.execute('''DROP TABLE IF EXISTS Replies;''')
            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'Replies') ''')

            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

            c.execute('''CREATE TABLE Replies (

                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    claim_id INTEGER NOT NULL,
                    from_user INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                    
                    type ENUM('CLARIFICATION', 'SUPPORTING ARGUMENT', 'COUNTERARGUMENT'),
                    reply_text TEXT NOT NULL,
                    FOREIGN KEY (from_user) REFERENCES Users (id),                     
                    FOREIGN KEY (claim_id) REFERENCES Claims (id)
                );
            ''')

            print("Replies Table created successfully")

    def insert_replies(self, claim_id, from_user, type, reply_text):

        c, conn = create_connection()

        createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        with conn:
            c.execute(
                '''INSERT INTO Replies (createdAt, updatedAt, claim_id, from_user, type, reply_text) VALUES (%s, %s, %s, %s, %s, %s);
                ''', (createdAt, updatedAt, claim_id, from_user, type, reply_text)
            )

            conn.commit()
            print("Last Row Id", c.lastrowid)
        return c.lastrowid

    def get_replies_to_claim(self, claim_id):
        c, conn = create_connection()

        with conn:
            c.execute(
                ''' SELECT C.id AS claim_id, R.reply_text AS reply_text, R.type AS reply_type, R.from_user AS reply_authored_by, R.id AS reply_id
                    FROM Claims C LEFT JOIN Replies R ON C.id = R.claim_id
                    WHERE R.claim_id = %s;
                ''', (claim_id,))

            desc = c.description
            myresult = c.fetchall()
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in myresult]
            print(data)
            return data

            # myresult = c.fetchall()
            # print(myresult)
            # return myresult


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
            # c.execute('''SET FOREIGN_KEY_CHECKS = 0''')
            # c.execute('''DROP TABLE IF EXISTS ReReplies;''')
            # c.execute('''SET FOREIGN_KEY_CHECKS = 1;''')

            c.execute(
                ''' SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA ='DebateForumDB') AND (TABLE_NAME = 'ReReplies') ''')

            # if the count is 1, then table exists
            if c.fetchone()[0] > 0:
                #print('Table exists.')
                return True

            c.execute('''CREATE TABLE ReReplies (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    reply_id INTEGER NOT NULL,
                    from_user INTEGER NOT NULL,
                    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                    
                    type ENUM('EVIDENCE', 'SUPPORT', 'REBUTTAL'),
                    re_reply_text TEXT NOT NULL,
                    FOREIGN KEY (from_user) REFERENCES Users (id),                     
                    FOREIGN KEY (reply_id) REFERENCES Replies (id)
                );
            ''')
#
            print("ReReplies Table created successfully")

    def insert_re_replies(self, reply_id, from_user, type, re_reply_text):

        c, conn = create_connection()

        createdAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        updatedAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        with conn:
            c.execute(
                '''INSERT INTO ReReplies (createdAt, updatedAt, reply_id, from_user, type, re_reply_text) VALUES (%s, %s, %s, %s, %s, %s);
                ''', (createdAt, updatedAt, reply_id, from_user, type, re_reply_text)
            )

            conn.commit()
            print("Last Row Id", c.lastrowid)
        return c.lastrowid

    def get_rereplies_to_replay(self, reply_id):
        c, conn = create_connection()

        with conn:
            c.execute(
                ''' SELECT R.id AS reply_id, Rr.re_reply_text AS re_reply_text, Rr.type AS re_reply_type, Rr.from_user AS re_reply_authored_by, Rr.id AS re_reply_id
                    FROM Replies R LEFT JOIN ReReplies Rr ON R.id = Rr.reply_id
                    WHERE Rr.reply_id = %s;
                ''', (reply_id,))

            desc = c.description
            myresult = c.fetchall()
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in myresult]
            print(data)
            return data
