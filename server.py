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
def return_portfolio():
    return render_template("portfolio.html")