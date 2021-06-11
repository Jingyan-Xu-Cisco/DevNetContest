#!/usr/bin/env python3
import sys
import mysql.connector as mariadb
dbConfig = {
    'host': '10.80.9.1',
    'user': 'remote',
    'password': 'C1sc0123',
    'database' : 'TLPR_test',
}
conn = mariadb.connect(**dbConfig)
cursor = conn.cursor()
#
# Initialize temp CDP table
#
cursor.execute("delete from tempCDP limit 100")
conn.commit()

#
# Get the last update timestamp
#
Left    = 1
Center  = 2
Right   = 3
I_want  = Left
i = 1

cursor.execute("select distinct time from CDP_table order by time desc limit 3")
# data = str(f"%s" % 
timestamp = cursor.fetchall()
for row in timestamp:
   if I_want == i:
      data = str(f"%s" % row)
      print (data)
   i = i + 1;
#
# Retrieve the CDP records with the timestamp equal to last update
#
statement = "select * from CDP_table where time = " + '"' + data + '"'
cursor.execute(statement)
records = cursor.fetchall()
print("Total number of CDP record rows is: ", cursor.rowcount)

#
# Perform deduplication of CDP records and write them to a new table, tempCDP
#
for row in records:
        statement = str(f'insert ignore into tempCDP (A, A_int, B, B_int, rec) value ("%s", "%s", "%s", "%s", 1)' % (row[0], row[2], row[3], row[4]))
        cursor.execute(statement)
        conn.commit()
        print (statement)
        statement = str(f'insert ignore into tempCDP (A, A_int, B, B_int, rec) value ("%s", "%s", "%s", "%s", 2)' % (row[3], row[4], row[0], row[2]))
        cursor.execute(statement)
        conn.commit()
        print (statement)
