import os, fnmatch

from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

def error(err):
    print(err)

@app.route('/')
def return_index():
    return send_file('index.html')

@app.route('/hello')
def hello():
    return 'hello, World!'

@app.errorhandler(404)
def page_notfound(error):
    print('Error: ' + str(error))
    return 'This page does not exist', 404