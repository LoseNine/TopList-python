from Config import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

base=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__,template_folder=base+'\\templates')
app.config.from_object(config.Config)

db=SQLAlchemy(app)