import sqlite3

conn=sqlite3.connect("MyDatabase.db")

#sql ="CREATE TABLE hirerform(id INTEGER PRIMARY KEY AUTOINCREMENT,Candidatename TEXT,CompanyName TEXT,EmployeeRole TEXT,CandidateMail TEXT,CandidateNumber TEXT)"

#sql="CREATE TABLE register (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,number TEXT,email TEXT,password TEXT)"
#cursor=conn.cursor()
#cursor.execute(sql)

#dict={"name":"sugan","pass":"5454"}
#print(dict["name"])

dict={"name":"hjkhjk","pass":"ggj"}

name=dict["name"]
pas=dict['pass']

if(name!="" and pas!=""):
    print('yes')


import http.client

conn = http.client.HTTPSConnection("linkedin-jobs-scraper-api.p.rapidapi.com")

payload = "{\r\n    \"title\": \"Software Engineer\",\r\n    \"location\": \"Berlin\",\r\n    \"rows\": 100\r\n}"

headers = {
    'content-type': "application/json",
    'X-RapidAPI-Key': "ce76502e3emsh89637eacd6deeccp1cec75jsnc1111b873470",
    'X-RapidAPI-Host': "linkedin-jobs-scraper-api.p.rapidapi.com"
}

conn.request("POST", "/jobs", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))