from flask_table import Table, Col, LinkCol, BoolNaCol
from CowBook.Util.MoneyColumn import MoneyCol


class SoldTable(Table):
	table_id = "HerdTable"
	name = LinkCol("Name", 'cow', url_kwargs=dict(cowId='id'), attr='name')
	earTag = Col("Ear Tag #")
	dob = Col("Date of Birth")
	sex = Col("Sex")
	is_heifer = BoolNaCol("Heifer")
	owner = Col("Owner")
	markings = Col("Markings")
	weight = Col("Weight")
	perPound = MoneyCol("Per Pound")
	total = MoneyCol("Total")
