import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="toko_cendrawasih"
)

def get_cursor(dictionary=True):
    return db.cursor(dictionary=dictionary)
