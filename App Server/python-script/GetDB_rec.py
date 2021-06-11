import sys
import mysql.connector as mariadb
from netmiko import ConnectHandler
dbConfig = {
    'host': '10.80.9.1',
    'user': 'remote',
    'password': 'C1sc0123',
    'database' : 'exampledb',
}
conn = mariadb.connect(**dbConfig)
cursor = conn.cursor()
sql_select_Query = "select * from example"
cursor.execute(sql_select_Query)
records = cursor.fetchall()
print("Total number of rows in Device is: ", cursor.rowcount)
print("\nPrinting record from example table")
for row in records:
        print("Fristname = ", row[0])
        print("Lastname = ", row[1])
