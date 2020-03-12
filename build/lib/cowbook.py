from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator

from __init__ import app, nav, db
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
		View("Add Cow", 'add_cow')
	)


if __name__ == '__main__':
	# database.init_db()
	nav.init_app(app)
	db.create_all()
	app.run(debug=True)
