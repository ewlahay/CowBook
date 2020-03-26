from flask_json import FlaskJSON
from flask_nav.elements import Navbar, View, Subgroup, Separator

from CowBook.Models.Cow.CowModel import Cow
from CowBook.init import app, nav, db
from CowBook import routes
from CowBook import api

# Navigation bar
@nav.navigation()
def navbar():
	return Navbar(
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
		View("Add Cow", 'add_cow')
	)


nav.init_app(app)
json = FlaskJSON()


@json.encoder
def custom_encoder(o):
	if isinstance(o, Cow):
		return o.__json__()


if __name__ == '__main__':
	json.init_app(app)
	db.create_all()
	app.run(debug=True, host='0.0.0.0')