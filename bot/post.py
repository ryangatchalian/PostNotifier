import mysql.connector
from mysql.connector import Error
from reddit import *
from settings import *

def create_server_connection(host_name: str, user_name: str, user_password: str):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        # print("MySQL server connection successful")
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
        # print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, database: str):
    cursor = connection.cursor()
    try:
        create_database_query = 'CREATE DATABASE IF NOT EXISTS ' + database
        cursor.execute(create_database_query)
        # print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query: str):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        # print("Query successful")
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
        insert_row = "INSERT IGNORE INTO " + website + " (title, url, created) VALUES (%s, %s, %s)"
        cursor.execute(insert_row, (data[0], data[1], data[2]))
        connection.commit()
        # print("stored")
        return True
    except Error as err:
        print(f"Error: '{err}'")
        return False


def latest_posts(connection, table_name: str, start: int, stop: int):
    diff = stop - start
    if diff > 0:
        data_query = f"SELECT * FROM {table_name} ORDER BY _id DESC LIMIT {diff}"
        output = pull_data(connection, data_query)
        return output
    else:
        return


if __name__ == '__main__':
    serverconn = create_server_connection('localhost', 'root', settings.MYSQL_PASS)
    create_database(serverconn, 'postnotifier')
    db = create_db_connection('localhost', 'root', settings.MYSQL_PASS, 'postnotifier')
    create_table_query = 'CREATE TABLE IF NOT EXISTS ' + settings.REDDIT + settings.TABLE_SETTINGS
    # print(create_table_query)
    execute_query(db, create_table_query)
    # print(pull_data(db, 'SELECT _id FROM reddit WHERE _id>4'))
    test = reddit.reddit_scrape()
    # print(test)
    get_last_row_id = "SELECT _id FROM " + settings.REDDIT + " ORDER BY _id DESC LIMIT 1;"
    latest_id = pull_data(db, get_last_row_id)[0][0]
    print(latest_id)
    # for row in test:
    #     store_post(db, settings.REDDIT, row)

    db.close()
