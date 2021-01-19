from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

@app.route('/')
def return_home():
    return render_template("index.html")

@app.route('/about')
def return_about():
    return render_template("about.html")

@app.route('/portfolio')
def return_users():
    with open('data/users.csv') as file:
        data = csv.reader(file, delimiter=',')
        first_line = True
        users = []
        for row in data:
            if not first_line:
                users.append({
                "fname": row[0],
                "lname": row[1],
                "bio": row[2]
                })
            else:
                first_line = False
        return render_template("portfolio.html", users=users)    

@app.route('/newUser', methods=["GET", "POST"])
def submit_form():
    if request.method == "GET":
        return redirect(url_for('newUser'))
    elif request.method == "POST":
        userdata = dict(request.form)
        fname = userdata["fname"]
        lname = userdata["lname"]
        bio = userdata["bio"]
        if( len(fname) < 1 or len(lname) < 1 or len(bio) < 1 ):
            return render_template("portfolio.html", status='Please resubmit with valid information.')
        else:
            with open('data/users.csv', mode='a', newline='') as file:
                data = csv.writer(file)
                data.writerow([fname, lname, bio])   
            return render_template("portfolio.html")   

@app.route('/newUser', methods=["GET", "POST"]) 
def delete_port():    
            