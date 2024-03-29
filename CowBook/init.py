import os
import warnings

from flask import Flask, render_template
from flask_admin import Admin
from flask_json import FlaskJSON
from flask_security import SQLAlchemyUserDatastore
from sqlalchemy.exc import IntegrityError
from CowBook.Models.Cow.CowModel import Cow
from CowBook.Models.Death import Death
from CowBook.Models.Note import Note
from CowBook.Models.Sale import Sale
from CowBook.Models.Treatment import Treatment, Event, Weight, PregnancyCheck, Bred
from CowBook.Models.User import User, Role
from CowBook.Views.Admin.Data import UserView, TreatmentView, CowView

json = FlaskJSON()


# basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config=None):
	app = Flask(__name__)
	app.config.from_object('CowBook.default_settings')
	if config is None:
		try:
			app.config.from_envvar('APP_CONFIG')
		except RuntimeError:
			print("Environmental variable APP_CONFIG not set!")
		except FileNotFoundError:
			print("Config file not found!")
	else:
		app.config.from_object(config)
	from CowBook.routes import app as routes
	from CowBook.api import api

	from CowBook.app import db, bootstrap, nav, security, mail
	db.init_app(app)
	bootstrap.init_app(app)
	nav.init_app(app)

	userDatastore = SQLAlchemyUserDatastore(db, User, Role)
	security.init_app(app, userDatastore)
	mail.init_app(app)
	json.init_app(app)
	db.create_all(app=app)
	admin = Admin(name='CowBook', app=app, template_mode='bootstrap3')
	with warnings.catch_warnings():
		warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
		admin.add_view(UserView(User, db.session))
	admin.add_view(CowView(Cow, db.session))
	admin.add_view(TreatmentView(Note, db.session))
	admin.add_view(TreatmentView(Treatment, db.session, category="Treatments"))
	admin.add_view(TreatmentView(Event, db.session, category="Treatments"))
	admin.add_view(TreatmentView(Weight, db.session, category="Treatments"))
	admin.add_view(TreatmentView(PregnancyCheck, db.session, category="Treatments"))
	admin.add_view(TreatmentView(Bred, db.session, category="Treatments"))
	admin.add_view(TreatmentView(Sale, db.session))
	admin.add_view(TreatmentView(Death, db.session))
	app.register_error_handler(404, page_not_found)
	app.register_blueprint(routes)
	app.register_blueprint(api)

	with app.app_context():
		create_user(app, db, userDatastore)
	return app


def create_user(app, db, userDatastore):
	# init_db()
	try:
		userDatastore.create_user(email=app.config["EMAIL"], password=app.config["PASSWORD"])
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
	except KeyError:
		pass


@json.encoder
def custom_encoder(o):
	if isinstance(o, (Cow, Treatment)):
		return o.__json__()


def page_not_found(e, message=None):
	return render_template('Error/404.html', content=message), 404
