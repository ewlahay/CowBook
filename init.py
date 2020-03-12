import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_nav import Nav
from flask_sqlalchemy import SQLAlchemy
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.secret_key = "mooo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
nav = Nav()
