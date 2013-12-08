import os
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
#Below is for debugging in flask server remove for gunicorn
app.config['DEBUG'] = True


@app.route('/main')
def home():
	return render_template('main.html') 

@app.route('/receive_simple/<data>')
def recv(data):
  f = open('temp.txt','w')
  f.write(data)
  f.close()
  return data

@app.route('/displayHello/')
def disply_html():
  return render_template('helloworld2.html') 


if __name__ == '__main__':
  app.run()

