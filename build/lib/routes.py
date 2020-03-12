from flask import render_template, request, redirect, url_for
import flask_table
from flask_table import Col, LinkCol, BoolCol, DateCol
from __init__ import app
from Models import Cow, Treatment


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/herd')
def herd():
	herdTable = Cow.CowTable(Cow.get_all())
	return render_template("Herd.html", table=herdTable)


@app.route('/herd/add', methods=["GET", "POST"])
def add_cow():
	form = Forms.CowForm()
	if form.validate_on_submit():
		newCow = form.save()
		return redirect(url_for('herd'))
	return render_template("/Cow/AddCow.html", form=form)


@app.route('/herd/<cowId>')
def cow(cowId):
	tempCow = Cow.get_by_id(cowId)
	calves = Cow.CowTable(Cow.get_calves(tempCow))
	weights = Treatment.WeightTable(Treatment.get_weights(tempCow))
	events = Treatment.EventTable(Treatment.get_events(tempCow))
	treats = Treatment.TreatmentTable(Treatment.get_treatments(tempCow))
	pregnancyChecks = Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks(tempCow))
	return render_template("/Cow/Cow.html", cow=tempCow, calves=calves, weights=weights, events=events,
	                       treatments=treats, pregnancyCheck=pregnancyChecks)


@app.route('/herd/<cowId>/treatment', methods=["GET", "POST"])
def treatment(cowId):
	tempCow = Cow.get_by_id(cowId)
	eventForm = Treatment.EventForm()
	treatmentForm = Treatment.TreatmentForm()
	weightForm = Treatment.WeightForm()
	pregnancyCheckForm = Treatment.PregnancyCheckForm()
	form = Treatment.Form()
	if tempCow is not None:
		'''if treatmentForm.validate_on_submit():
			treatmentForm.save(cowId)
		elif weightForm.validate_on_submit():
			weightForm.save(cowId)
		elif pregnancyCheckForm.validate_on_submit():
			pregnancyCheckForm.save(cowId)
		elif eventForm.validate_on_submit():
			eventForm.save(cowId)'''
		if form.formType.data == "Event":
			item = eventForm
		elif form.formType.data == "Treatment":
			item = treatmentForm
		elif form.formType.data == "Weight":
			item = weightForm
		elif form.formType.data == "Pregnancy Check":
			item = pregnancyCheckForm
		else:
			item = form
		if item.validate_on_submit():
			item.save(cowId)
		else:
			if request.method == 'POST':
				form.validate()
			print(item.errors)
			return render_template("/Cow/AddTreatment.html", cow=tempCow, form=form, event=eventForm,
			                       treatment=treatmentForm, weight=weightForm, pregnancyCheck=pregnancyCheckForm)
		return redirect(url_for('herd'))
	else:
		return render_template("/Error/404.html")


def event(cowId):
	pass


@app.route('/herd/treatments')
def treatments():
	treatType = request.args.get("type")
	events = []
	TableClass = flask_table.create_table('Events')
	columns = [("parent", LinkCol("Cow", "cow", url_kwargs=dict(cowId='parent'))), ("date", DateCol("Date")), ("type", Col("Type")), ("notes", Col("Notes"))]
	medical = [("lotNo", Col("Lot #")), ("expiration", DateCol("Expiration")), ("withdrawal", Col("Withdrawal (Days)")), ("dosage", Col("Dosage")), ("unit", Col("unit"))]
	weight = [("weight", Col("Weight"))]
	pregnancyCheck = [("pregnant", BoolCol("Pregnant"))]
	tables = []
	if treatType == "all":
		tables.append(Treatment.EventTable(Treatment.get_events()))
		tables.append(Treatment.TreatmentTable(Treatment.get_treatments()))
		tables.append(Treatment.WeightTable(Treatment.get_weights()))
		tables.append(Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks()))
	elif treatType == "medical":
		tables.append(Treatment.TreatmentTable(Treatment.get_treatments()))
	elif treatType == "weight":
		tables.append(Treatment.WeightTable(Treatment.get_weights()))
	elif treatType == "pregnancyCheck":
		tables.append(Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks()))
	return render_template("Treatments.html", tables=tables)
