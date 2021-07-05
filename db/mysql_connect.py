from logging import error
import mysql.connector
from flaskext.mysql import MySQL
from config import credentials

databaseSet = "DebateForumDB3"
mysql_credentials = credentials.db_credentials

def create_mysql_db(db_credential):
    try:
        [host, user, password, database] = db_credential
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            auth_plugin='mysql_native_password'
        )
        my_cursor = mydb.cursor()
        my_cursor.execute("CREATE DATABASE DebateForumDB3")
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
        conn = mysql.connector.connect(host=host,user=user,password=passd,database=databaseSet)
        c = conn.cursor()
        return c, conn
    except error as er:
        print(er)

    return None


class UserAuthSqliteDb:
    def __init__(self, db_credential):
        self.create_db()
        self.db_credential = db_credential

    def recipient_exists(self, to_add):
        conn = create_connection(self.db_credential)
        #conn.text_factory = bytes

        # with self.conn:
        #     cursor = conn.execute("SELECT user_id FROM users WHERE username = ?", to_add)
        #     result = cursor.fetchone()
        #     if result:
        #         return True
        #     else:
        #         return False     
