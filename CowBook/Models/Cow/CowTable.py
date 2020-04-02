from flask_table import Table, Col, LinkCol, BoolNaCol


class CowTable(Table):
	table_id = "HerdTable"
	name = LinkCol("Name", 'app.cow', url_kwargs=dict(cowId='id'), attr='name')
	earTag = Col("Ear Tag #")
	dob = Col("Date of Birth")
	sex = Col("Sex")
	is_heifer = BoolNaCol("Heifer")
	# is_sold = BoolNaCol("Sold")
	carrier = Col("Carrier")
	owner = Col("Owner")
	markings = Col("Markings")
	addTreatment = LinkCol("Add Record", 'app.treatment', url_kwargs=dict(cowId='id'), text_fallback="Add")
	editCow = LinkCol("Edit Cow", 'app.edit_cow', url_kwargs=dict(cowId='id'), text_fallback="edit")
