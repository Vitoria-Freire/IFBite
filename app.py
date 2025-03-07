from flask import Flask, render_template, request, redirect, url_for

from crud import createUpdateDelete
from crud import read

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')