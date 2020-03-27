import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('CowBook.default_settings')
app.config.from_pyfile(os.environ['APP_CONFIG'])
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
nav = Nav()
