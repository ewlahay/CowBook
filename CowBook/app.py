from sqlalchemy.exc import IntegrityError

from flask_json import FlaskJSON
import flask_security.core as core
from flask_nav.elements import Navbar, View, Subgroup, Separator, Link
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore, Security
from CowBook.Models.Cow.CowModel import Cow
from CowBook.Models.User import User, Role
from CowBook.init import app, nav, db
from CowBook import routes
from CowBook import api


# Navigation bar
@nav.navigation()
def navbar():
	navy = Navbar(
		'CowBook',
		View('Home', 'index'),
		Subgroup('Herd',
		         View("All", 'herd', type='all'),
		         View("Active", 'herd', type='active'),
		         View("Sold", 'herd', type='sold'),
		         Separator(),
		         View("Dead", 'herd', type='dead')
		         ),
		Subgroup('Treatments',
		         View('All', 'treatments', type='all'),
		         View('Medical', 'treatments', type='medical'),
		         View('Weights', 'treatments', type='weight'),
		         View("Breeding Records", 'treatments', type='breeding'),
		         View("Pregnancy Checks", 'treatments', type='pregnancyCheck')
		         ),
		View("Due Dates", 'view_due_date'),
	)
	if core.current_user.is_authenticated:
		navy.items.append(View("Add Cow", 'add_cow'))
		navy.items.append(View("User", "user"))
		navy.items.append(Link("Logout", "/logout"))
	else:
		navy.items.append(Link("Login", "/login"))
	return navy


nav.init_app(app)
json = FlaskJSON()
userDatastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, userDatastore)
mail = Mail(app)
json.init_app(app)
db.create_all()


@app.before_first_request
def create_user():
	# init_db()
	userDatastore.create_user(email=app.config["EMAIL"], password=app.config["PASSWORD"])
	try:
		db.session.commit()
	except IntegrityError:
		db.session.rollback()


@json.encoder
def custom_encoder(o):
	if isinstance(o, Cow):
		return o.__json__()


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
