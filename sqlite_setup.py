import sqlite3
import json

conn=sqlite3.connect("MyDatabase.db")

print("Success")
#sql="INSERT INTO DATA (username,pass) VALUES (?, ?)"

sql="SELECT * FROM DATA where username=?"
val="sugan"

cursor=conn.cursor()

cursor.execute(sql,(val,))

# Get column names from the cursor description
columns = [column[0] for column in cursor.description]

# Fetch all results as a list of dictionaries
result_as_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]

print(result_as_dict)

for i in result_as_dict:
    print(i['PASS'])

#p=cursor.fetchall()

# for v in p:
#     #g=json.dumps(v)
#     print(v)
#     print(v['pass'])

print("inserted successfully")

#conn.execute("CREATE TABLE USER(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,pass TEXT)")

#sql="CREATE TABLE DATA (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,pass TEXT)"

#cursor.execute(sql)

print("next")

conn.close()

list=[6876]


# if not result_as_dict:
#     print(" empty")
# else:
#     print("available")
#     while 
#         print(i['pass'])
