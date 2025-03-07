from flask import Flask, render_template, request, redirect, url_for

from crud import createUpdateDelete
from crud import read

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')
