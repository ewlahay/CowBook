from flask import render_template, request, redirect, url_for, flash
from flask_json import as_json
import dateutil.parser

from Forms.BredForm import BredForm
from Forms.Cow.EditParentForm import EditParentForm
from Forms.DeathForm import DeathForm
from Forms.EventForm import EventForm
from Forms.PregnancyCheckForm import PregnancyCheckForm
from Forms.SaleForm import SaleForm
from Forms.TreatmentForm import TreatmentForm
from Forms.WeightForm import WeightForm
from Models.Cow.CowModel import get_by_id, get_calves, get_all, get_all_dams, get_all_sires, get_active
from Forms.Cow.CowForm import CowForm
from Models.Cow.CowTable import CowTable
from Forms.Cow.EditCowForm import EditCowForm
from Models.Death import get_dead
from Models.DeathTable import DeathTable
from Models.Sale import get_sold
from Models.SoldTable import SoldTable
from init import app
from Models import Treatment


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/herd')
def herd():
	tableType = request.args.get("type")
	# data =
	types = {
		"all": get_all,
		"active": get_active,
		"sold": get_sold,
		"dead": get_dead
	}
	data = types[tableType]
	if data is not None:
		data = data()
	if tableType == "sold":
		herdTable = SoldTable(data)
	elif tableType == "dead":
		herdTable = DeathTable(data)
	else:
		herdTable = CowTable(data)
	return render_template("Herd.html", table=herdTable)


@app.route('/herd/add', methods=["GET", "POST"])
def add_cow():
	form = CowForm()
	if form.validate_on_submit():
		form.save()
		return redirect(url_for('herd'))
	return render_template("/Cow/AddCow.html", form=form)


@app.route('/herd/duedates')
def view_due_date():
	defaultDate = Treatment.get_next_due_date()
	return render_template("/Cow/DueDates.html", defaultDate=defaultDate)


@app.route('/herd/<cowId>')
def cow(cowId):
	tempCow = get_by_id(cowId)
	if tempCow is None:
		return render_template('/Error/404.html', content="Cow {} not found".format(cowId))
	dam = get_by_id(tempCow.dam_id)
	sire = get_by_id(tempCow.sire_id)

	calves = CowTable(get_calves(tempCow))
	weights = Treatment.WeightTable(Treatment.get_weights(tempCow))
	events = Treatment.EventTable(Treatment.get_events(tempCow))
	# del events.parent
	treats = Treatment.TreatmentTable(Treatment.get_treatments(tempCow))
	# del treats.parent
	pregnancyChecks = Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks(tempCow))
	# del pregnancyChecks.parent
	breedings = Treatment.BredTable(Treatment.get_breedings(tempCow))
	# del breedings.parent
	return render_template("/Cow/Cow.html", cow=tempCow, calves=calves, weights=weights, events=events,
	                       treatments=treats, pregnancyCheck=pregnancyChecks, breedings=breedings, dam=dam, sire=sire)


@app.route('/herd/<cowId>/addEvent', methods=["GET", "POST"])
def treatment(cowId):
	tempCow = get_by_id(cowId)
	if tempCow is not None:
		# Single form with every possible field
		form = Treatment.Form()
		# Set choices for form type on frontend
		form.formType.choices = [("Event", "Event"), ("Treatment", "Treatment"), ("Weight", "Weight"), ("Sale", "Sale"), ("Death", "Death")]
		if tempCow.sex == "cow":
			form.formType.choices.append(("Pregnancy Check", "Pregnancy Check"))
			form.formType.choices.append(("Bred", "Bred"))
		form.formType.choices.sort(key=lambda x: x[0])
		formType = {
			"Event": EventForm,
			"Treatment": TreatmentForm,
			"Weight": WeightForm,
			"Pregnancy Check": PregnancyCheckForm,
			"Bred": BredForm,
			"Sale": SaleForm,
			"Death": DeathForm,
		}
		item = formType.get(form.formType.data)
		if item is None:
			item = form
		else:
			item = item()
		"""
		if form.formType.data == "Event":
			item = eventForm
		elif form.formType.data == "Treatment":
			item = treatmentForm
		elif form.formType.data == "Weight":
			item = weightForm
		elif form.formType.data == "Pregnancy Check":
			item = pregnancyCheckForm
		elif form.formType.data == "Bred":
			item = bredForm
		elif form.formType.data == "Sale":
			item = saleForm
		else:
			item = form
		"""
		if item.validate_on_submit():
			item.save(cowId)
		else:
			if request.method == 'POST':
				form.validate()
			return render_template("/Cow/AddTreatment.html", cow=tempCow, form=form)
		return redirect(url_for('cow', cowId=cowId))
	else:
		return render_template("/Error/404.html")


@app.route('/herd/<cowId>/edit', methods=["GET", "POST"])
def edit_cow(cowId):
	tempCow = get_by_id(cowId)
	if tempCow is None:
		return render_template('/Error/404.html', content="Cow {} not found".format(cowId))
	form = EditCowForm(cowId)
	if form.validate_on_submit():
		form.save()
		return redirect(url_for('cow', cowId=cowId))
	form.setup()
	return render_template("/Cow/Edit.html", cow=tempCow, form=form)


@app.route('/herd/<cowId>/edit/dam', methods=["GET", "POST"])
def edit_dam(cowId):
	newCow = get_by_id(cowId)
	if newCow is None:
		return render_template('/Error/404.html', content="Cow {} not found".format(cowId))
	form = EditParentForm(cowId, parent="dam")
	if form.validate_on_submit():
		try:
			form.save()
		except ValueError as e:
			flash(e)
			return render_template("/Cow/EditParent.html", cow=newCow, form=form)
		return redirect(url_for('cow', cowId=cowId))
	return render_template("/Cow/EditParent.html", cow=newCow, form=form)


@app.route('/herd/<cowId>/edit/sire', methods=["GET", "POST"])
def edit_sire(cowId):
	newCow = get_by_id(cowId)
	if newCow is None:
		return render_template('/Error/404.html', content="Cow {} not found".format(cowId))
	form = EditParentForm(cowId, parent="sire")
	if form.validate_on_submit():
		try:
			form.save()
		except ValueError as e:
			flash(e)
			return render_template("/Cow/EditParent.html", cow=newCow, form=form)
		return redirect(url_for('cow', cowId=cowId))
	return render_template("/Cow/EditParent.html", cow=newCow, form=form)


@app.route('/herd/<cowId>/sell', methods=["GET", "POST"])
def sell_cow(cowId):
	pass


@app.route('/herd/treatments')
def treatments():
	treatType = request.args.get("type")
	tables = []
	if treatType == "all":
		tables.append(Treatment.EventTable(Treatment.get_events()))
		tables.append(Treatment.TreatmentTable(Treatment.get_treatments()))
		tables.append(Treatment.WeightTable(Treatment.get_weights()))
		tables.append(Treatment.BredTable(Treatment.get_breedings()))
		tables.append(Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks()))
	elif treatType == "medical":
		tables.append(Treatment.TreatmentTable(Treatment.get_treatments()))
	elif treatType == "weight":
		tables.append(Treatment.WeightTable(Treatment.get_weights()))
	elif treatType == "pregnancyCheck":
		tables.append(Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks()))
	elif treatType == "breeding":
		tables.append(Treatment.BredTable(Treatment.get_breedings()))
	return render_template("Treatments.html", tables=tables)
