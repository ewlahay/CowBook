from flask_json import FlaskJSON
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator

from Models.Cow.CowModel import Cow
from init import app, nav, db
import routes


# Navigation bar
@nav.navigation()
def navbar():
	return Navbar(
		'CowBook',
		View('Home', 'index'),
		View('Herd', "herd"),
		Subgroup('Treatments',
		         View('All', 'treatments', type='all'),
		         View('Medical', 'treatments', type='medical'),
		         View('Weights', 'treatments', type='weight'),
		         View("Pregnancy Checks", 'treatments', type='pregnancyCheck')
		         ),
		View("Due Dates", 'view_due_date'),
		View("Add Cow", 'add_cow')
	)


nav.init_app(app)
json = FlaskJSON()


@json.encoder
def custom_encoder(o):
	if isinstance(o, Cow):
		return o.__json__()


if __name__ == '__main__':
	# database.init_db()
	json.init_app(app)
	db.create_all()
	app.run(debug=True, host='0.0.0.0')
