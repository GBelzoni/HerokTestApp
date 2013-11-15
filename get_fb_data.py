import os
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('main.html') 

@app.route('/displayHello/')
def disply_html():
	return render_template('helloworld2.html') 




