import uuid
import logging
import os
from flask import Flask, request, render_template, redirect, url_for
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha
from pymongo import MongoClient


app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(), 'webwork')
    )

# Database Config
mongoClient = MongoClient('localhost', 27017)
mongo_db = mongoClient['myapp'] 

# Captcha Config
app.config["SECRET_KEY"] = str(uuid.uuid4()) 
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 8
app.config['CAPTCHA_WIDTH'] = 300
app.config['CAPTCHA_HEIGHT'] = 100

# Session Config
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = mongo_db  
app.config['SESSION_MONGODB_COLLECTION'] = 'sessions' 
app.config['SESSION_PERMANENT'] = False  
app.config['SESSION_COOKIE_NAME'] = 'my_session_cookie'

Session(app)
captcha = FlaskSessionCaptcha(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        if captcha.validate():
            return redirect(url_for('success'))
        else:
            return redirect(url_for('fail'))
    return render_template("mainForm.html")

@app.route('/successForm')
def success():
    return render_template("successForm.html")

@app.route('/failForm')
def fail():
    return render_template("failForm.html")

if __name__ == "__main__":
    app.debug = True
    logging.getLogger().setLevel("DEBUG")
    app.run()
