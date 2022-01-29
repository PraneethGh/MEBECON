
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote  
from sqlalchemy.engine import create_engine
app=Flask(__name__)

db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:praneeth@localhost:5432/disclasif"
from proj import routes