from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key ='!@#@!#ASDASFAER!@$ASD#!#@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/dbwebfilm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 5
db = SQLAlchemy(app=app)