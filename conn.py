import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="bank"
)
cursor = mydb.cursor()
