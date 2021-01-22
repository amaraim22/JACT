import os
import urllib.request
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import csv

app = Flask(__name__)

@app.route('/')
def return_home():
    return render_template("index.html")

@app.route('/about')
def return_about():
    return render_template("about.html")

@app.route('/index')
def return_index():
    return render_template("index.html")

def return_users():
    with open('data/users.csv', mode='r') as file:
        data = csv.DictReader(file, delimiter=',')
        user = []      
        for row in data:
            user.append({
                "fname": row["firstName"],
                "lname": row["lastName"],
                "bio": row["bio"],
                "imgFile": row["imgFile"]
                })
    return user

@app.route('/portfolio')
def return_form():
    users = []
    users = return_users()
    return render_template("portfolio.html", users=users) 

app.config["IMAGE_UPLOADS"] = '/Users/chantelngoh/Desktop/SBU/Github/JACT/static/images'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            print("Image saved")
            return redirect(request.url)

    return render_template("portfolio.html")

@app.route('/newUser', methods=["GET", "POST"])
def new_form():
    if request.method == "GET":
        return redirect(url_for('newUser'))
    elif request.method == "POST":
        userdata = dict(request.form)
        fname = userdata["fname"]
        lname = userdata["lname"]
        bio = userdata["bio"]
        lines = list()
        isTaken = False
        users = []

        with open('data/users.csv', mode='r') as readFile:
            reader = csv.DictReader(readFile, delimiter=',')
            for row in reader:
                lines.append(row)
                for r in range(len(lines)):
                    if fname == lines[r]["firstName"] and lname == lines[r]["lastName"]:
                        isTaken = True

        if( len(fname) < 1 or len(lname) < 1 or len(bio) < 1 ):
            users = return_users()
            return render_template("portfolio.html", users=users, status='Please resubmit with valid information.')  

        elif( isTaken == True ):
            users = return_users()
            return render_template("portfolio.html", users=users, info='This name is already taken.')   

        else:
            if request.files:
                image = request.files["image"]
                if image.filename == "":
                    users = return_users()
                    return render_template("portfolio.html", users=users, image_status='Please submit an image.') 
                if not allowed_image(image.filename):
                    users = return_users()
                    return render_template("portfolio.html", users=users, image_status='That image extension is not allowed.') 
                else:
                    filename = secure_filename(image.filename)
                    ext = filename.rsplit(".", 1)[1]
                    new_filename = fname + "-" + lname + "." + ext
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], new_filename))

                with open('data/users.csv', mode='a', newline='') as file:
                    data = csv.writer(file)
                    data.writerow([fname, lname, bio,new_filename]) 
                users = []
                users = return_users()
                return render_template("portfolio.html", users=users)       

@app.route('/portfolio', methods=["GET", "POST"])
def delete_form():
    if request.method == "GET":
        return render_template("portfolio.html") 
    elif request.method == "POST":
        userdata = dict(request.form)
        fullname = userdata["delete-btn"]    
        fname = fullname.rsplit("-", 1)[0]
        lname = fullname.rsplit("-", 1)[1]
        lines = list()
        with open('data/users.csv', mode='r') as readFile:
            reader = csv.DictReader(readFile, delimiter=',')
            for row in reader:
                lines.append(row)
                for r in range(len(lines)):
                    if fname == lines[r]["firstName"] and lname == lines[r]["lastName"]:
                        lines.remove(row)
                        arrImages = os.listdir(app.config["IMAGE_UPLOADS"])
                        for img in arrImages:
                            filename = img.rsplit(".", 1)[0]
                            if filename == fullname:
                                os.remove(app.config["IMAGE_UPLOADS"] + '/' + img)

        with open('data/users.csv', mode='w') as writeFile:
            writer = csv.writer(writeFile)  
            writer.writerow(["firstName", "lastName", "bio", "imgFile"])  
            for r in range(len(lines)):
                firstName = lines[r]["firstName"]
                lastName = lines[r]["lastName"]
                bio = lines[r]["bio"]   
                imgFile = lines[r]["imgFile"]  
                writer.writerow([firstName, lastName, bio, imgFile])
        users = []
        users = return_users()      
        return render_template("portfolio.html", users=users)

@app.route('/open', methods=["GET", "POST"])
def open_form():
    if request.method == "GET":
        return render_template("portfolio.html") 
    elif request.method == "POST":
        userdata = dict(request.form)
        fullname = userdata["open-btn"]    
        fname = fullname.rsplit("-", 1)[0]
        lname = fullname.rsplit("-", 1)[1]   
        lines = list()
        with open('data/users.csv', mode='r') as readFile:
            reader = csv.DictReader(readFile, delimiter=',')
            for row in reader:
                lines.append(row)
                for r in range(len(lines)):
                    if fname != lines[r]["firstName"] and lname != lines[r]["lastName"]:
                        lines.remove(row)
            return render_template("user-page.html", thisUser=lines)

if __name__ == '__main__':
   app.run(debug = True)