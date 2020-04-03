from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_sqlalchemy import SQLAlchemy
import flask_security.core as core
from flask_nav.elements import Navbar, View, Subgroup, Separator, Link
from flask_mail import Mail
from flask_security import Security

db = SQLAlchemy()
bootstrap = Bootstrap()
nav = Nav()


# Navigation bar
@nav.navigation()
def navbar():
	navy = Navbar(
		'CowBook',
		View('Home', 'app.index'),
		Subgroup('Herd',
		         View("All", 'app.herd', type='all'),
		         View("Active", 'app.herd', type='active'),
		         View("Sold", 'app.herd', type='sold'),
		         Separator(),
		         View("Dead", 'app.herd', type='dead')
		         ),
		Subgroup('Treatments',
		         View('All', 'app.treatments', type='all'),
		         View('Medical', 'app.treatments', type='medical'),
		         View('Weights', 'app.treatments', type='weight'),
		         View("Breeding Records", 'app.treatments', type='breeding'),
		         View("Pregnancy Checks", 'app.treatments', type='pregnancyCheck')
		         ),
		View("Due Dates", 'app.view_due_date'),
	)
	if core.current_user.is_authenticated:
		navy.items.append(View("Add Cow", 'app.add_cow'))
		navy.items.append(View("User", "app.user"))
		navy.items.append(Link("Logout", "/logout"))
	else:
		navy.items.append(Link("Login", "/login"))
	return navy


security = Security()
mail = Mail()

if __name__ == '__main__':
	from CowBook.init import create_app

	app = create_app()
	app.run(debug=True, host='0.0.0.0')
