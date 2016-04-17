# Python web app.

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)

@app.route('/')
def main_view():
    return render_template('index.html')

@app.route('/temperatures')
def temperatures_view():
    return render_template('temperatures.html')
