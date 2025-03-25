def get_db_cursor():
    from app import mysql
    return mysql.connection.cursor()
