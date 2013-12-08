import os
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
#Below is for debugging in flask server remove for gunicorn
app.config['DEBUG'] = True


#Renders main page including logins and writing short and long tokens
#javascript file in static/fblogin.js
@app.route('/main')
def home():
	return render_template('main.html') 

#This handler receives GET request with <data> being the short term access token
@app.route('/receive_simple/<data>')
def recv(data):
  f = open('short_AT.txt','w')
  f.write(data)
  f.close()
  return data
 
#This handler call script which reads saved short access token, queries FB api for long access token
#Save long_AT in text file and returns token to display page 
@app.route('/get_long_AT')
def get_long_AT():
  
  from get_long_token import get_long_AT
  return get_long_AT() 

@app.route('/displayHello/')
def disply_html():
  return render_template('helloworld2.html') 


if __name__ == '__main__':
  app.run()

