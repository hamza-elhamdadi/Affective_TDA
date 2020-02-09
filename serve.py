import os, fnmatch

from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

def error(err):
    print(err)

@app.route('/')
def hello():
    return 'hello, World!'
@app.route('/goodbye')
def goodbye():
    return 'goodbye, World!'