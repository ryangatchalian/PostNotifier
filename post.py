import mysql.connector
from mysql.connector import Error
import settings


def create_server_connection(host_name: str, user_name: str, user_password: str):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL server connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_db_connection(host_name: str, user_name: str, user_password: str, db_name: str):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, database: str):
    cursor = connection.cursor()
    try:
        create_database_query = 'CREATE DATABASE IF NOT EXISTS ' + database
        cursor.execute(create_database_query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query: str):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def pull_data(connection, query: str):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        row = cursor.fetchall()
        if row is not None:
            return row
        else:
            return 'table is empty'
    except Error as err:
        print(f"Error: '{err}'")


def store_post(connection, website: str, data: tuple):
    cursor = connection.cursor(buffered=True)
    try:
        insert_row = 'INSERT INTO ' + website + ' (title, url, time) VALUES (%s, %s, %s)'
        cursor.execute(insert_row, (data[0], data[1], data[2]))
        connection.commit()
        print("stored")
        return True
    except Error as err:
        print(f"Error: '{err}'")
        return False


if __name__ == '__main__':
    serverconn = create_server_connection('localhost', 'root', settings.MYSQL_PASS)
    create_database(serverconn, 'postnotifier')
    db = create_db_connection('localhost', 'root', settings.MYSQL_PASS, 'postnotifier')
    create_table_query = 'CREATE TABLE IF NOT EXISTS ' + settings.REDDIT + settings.TABLE_SETTINGS
    execute_query(db, create_table_query)
    print(pull_data(db, 'SELECT * FROM reddit WHERE _id>4'))
    test = [('test title', 'test url', 'test time'), ('test 2a', 'test 2b', 'test 2c')]
    store_post(db, 'reddit', test[1])
    # dbcursor = db.cursor(buffered=True)
    # # dbcursor.execute("SELECT * FROM reddit")
    # # for i in range(dbcursor.rowcount):
    # #     row = dbcursor.fetchone()
    # #     print(row)
    db.close()
