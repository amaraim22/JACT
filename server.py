import os
#import magic
import urllib.request
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import csv

app = Flask(__name__)
UPLOAD_FOLDER = "/Users/chantelngoh/Desktop/SBU/Github/JACT/templates/upload.html"
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/open/<uname>')
def return_open(uname):
    return "Hello" + uname

@app.route('/portfolio')
def return_portfolio():
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
      
# @app.route('/delete')
# def delete_user():
#     with open('data/users.csv') as file:
#         data = csv.reader(file, delimiter=',')
#         first_line = True
#         users = []
#         for row in data:
#             if 

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

@app.route('/upload')
def upload_form():
    return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == '__main__':
   app.run(debug = True)
    
