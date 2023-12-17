from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask,request,render_template,flash,url_for,redirect;

import sqlite3

import json

import http

print("Connected Successfully !")

app = Flask(__name__)

app.secret_key = 'Done ehhh'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/registerrec",methods = ['POST', 'GET'])
def registerrec():
    msg=''
    if request.method == 'POST':

        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        password = request.form['password']

        if(name!="" and number!="" and email!="" and password!=""):
      
              sql = "SELECT * FROM register WHERE email =? "
              conn=sqlite3.connect("MyDatabase.db")
              cursor=conn.cursor()
              cursor.execute(sql,(email,))
              columns = [column[0] for column in cursor.description]
              # Fetch all results as a list of dictionaries
              list = [dict(zip(columns, row)) for row in cursor.fetchall()]
              print(list)
              conn.commit()
              conn.close()
              print(list) 
              print(type(list))
              print("--------------------------------")
              if len(list)>0:
                 return render_template('login.html', msg="You are already registered with this email id , please login using your details")
              else:
        
                  insert_sql = "INSERT INTO register (name,number,email,password)  VALUES (?,?,?,?)"

                  conn=sqlite3.connect("MyDatabase.db")
                  data=(name,number,email,password)
                  cursor=conn.cursor()
                  cursor.execute(insert_sql,data)
                  conn.commit()
                  conn.close()
                  print("==============================================")
                  return render_template('login.html', msg="Registered successfuly..login to continue")
        else:
            return render_template('register.html',usrname=name,usrpass=password,usrnumber=number,usremail=email,smsg = 'please fill the all columns ')
    
    else:
        return render_template('register.html',msg="")

#Login

@app.route("/loginrec", methods =['POST','GET'])
def loginrec():
    print(request.method)
    print(request.form)
    smsg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        if( email!="" and password!=""):
            print("#######################")
            print(email)
            print(password)
            print("################################")
            sql = "SELECT * FROM register WHERE email = ?"
            
            conn=sqlite3.connect("MyDatabase.db")
            cursor=conn.cursor()
            cursor.execute(sql,(email,))
            # Get column names from the cursor description
            columns = [column[0] for column in cursor.description]
            list = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.commit()
            conn.close()
            print("*********************************")
            print(type(list))
            print(list)
            print("******************************")
            if len(list)>0:
                dic=list[0]
                res1 = dic['email']
                res2 = dic['password']
                res3 = dic['name']
                res4 = dic['number']

                if(res1 == email and res2 == password):
                        session['email'] = res1
                        session['pass'] = res2
                        session['name'] = res3
                        session['number'] = res4
                        return render_template('profile.html')
                else:
                    return render_template('login.html', smsg ='Incorrect username / password !',mail=email,passwd=password)
            else:
                return render_template('register.html', smsg = 'Not yet registered')
        else:   
            print("============================================================")
            return render_template('login.html', smsg ='Please fill all the details!',mail=email,passwd=password)

    else:
        if 'email' in session and 'pass' in session:
            return render_template('profile.html')
        else:
            return render_template('login.html')
            
#contac

@app.route("/jobsrec",methods = ['POST', 'GET'])
def jobsrec():
    jmsg=''

    if request.method == 'POST':
    
        CandidateName = request.form['CandidateName']
        CompanyName = request.form['CompanyName']
        EmployeeRole = request.form['EmployeeRole']
        CandidateMail = request.form['CandidateMail']
        CandidateNumber = request.form['CandidateNumber']
        
        if(CandidateMail!="" and CandidateName!=""):
        
           insert_sql = "INSERT INTO hirerform (CandidateName,CompanyName,EmployeeRole,CandidateMail,CandidateNumber) VALUES (?,?,?,?,?)"
           tuple=(CandidateName,CompanyName,EmployeeRole,CandidateMail,CandidateNumber)
           conn=sqlite3.connect("MyDatabase.db")
           cursor=conn.cursor()
           cursor.execute(insert_sql,tuple)
           conn.commit()
           conn.close()    
           return render_template('jobs.html', msg="Registered successful!! and We will contact you soon")
    
        else:
            return render_template('jobs.html',role=EmployeeRole,name=CandidateName,email=CandidateMail,cname=CompanyName,nummber=CandidateNumber ,smsg="Please enter the email and name ")
  
    else:
        return render_template('jobs.html', jmsg="")


@app.route('/profile')
def profile():
    if 'email'  in session and 'pass' in session:
         return render_template("profile.html")
    else:
        return render_template("login.html")


@app.route('/exploreJobs', methods = ['GET', 'POST'])
def exploreJobs():

    if 'email' in session and 'pass' in session:
  
        conn = http.client.HTTPSConnection("linkedin-jobs-scraper-api.p.rapidapi.com")

        payload = "{\r\n    \"title\": \"Software Engineer\",\r\n    \"location\": \"Berlin\",\r\n    \"rows\": 100\r\n}"

        headers = {
        'content-type': "application/json",
        'X-RapidAPI-Key': "f844d89005msh1e3f82ddc9fd4d9p12657djsnc1a3cf230946",
        'X-RapidAPI-Host': "linkedin-jobs-scraper-api.p.rapidapi.com"
         }

        conn.request("POST", "/jobs", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data=data.decode("utf-8")
        job = json.loads(data)
        print("=============================================================")
        #print(job)
        print(type(job))
	    #json_data = json.loads(job)
        return render_template('exploreJobs.html', jobs =job)
    
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('email', None)
   session.pop('pass', None)
   session.pop('name', None)
   session.pop('number', None)
   # Redirect to login page
   return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

