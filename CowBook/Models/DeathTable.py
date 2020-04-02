from flask_table import Table, Col, LinkCol, BoolNaCol


class DeathTable(Table):
	table_id = "HerdTable"
	name = LinkCol("Name", 'app.cow', url_kwargs=dict(cowId='id'), attr='name')
	earTag = Col("Ear Tag #")
	dob = Col("Date of Birth")
	sex = Col("Sex")
	is_heifer = BoolNaCol("Heifer")
	owner = Col("Owner")
	markings = Col("Markings")
	date = Col("Date of Death")
	cause = Col("Cause of Death")
