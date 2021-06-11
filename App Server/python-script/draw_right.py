#!/usr/bin/env python3
import os
import mysql.connector as mariadb
f = open("/home/layim/code/topology.dot", "w")
dbConfig = {
    'host': '10.80.9.1',
    'user': 'remote',
    'password': 'C1sc0123',
    'database' : 'TLPR_test',
}
conn = mariadb.connect(**dbConfig)
cursor = conn.cursor()
sql_select_Query = "select * from tempCDP where rec=1"
cursor.execute(sql_select_Query)
records = cursor.fetchall()
print("Total number of link in the topology is: ", cursor.rowcount)
f.write ("digraph topology {\n");
for row in records:
        f.write(f'   "%s" -> "%s" [arrowhead=none];\n' % (row[0], row[2]))
sql_select_Query = "select distinct A from tempCDP"
cursor.execute(sql_select_Query)
records = cursor.fetchall()
for row in records:
        f.write(f'   "%s" [shape=rect label="%s" width=3]\n' % (row[0], row[0]))

f.write ("}\n")
f.close()
os.system('/usr/bin/dot -Tjpeg /home/layim/code/topology.dot -o /var/www/html/app/jpg/topology3.jpg')
