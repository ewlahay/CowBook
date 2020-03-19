from flask import render_template, request, redirect, url_for, flash
from flask_json import as_json
import dateutil.parser
from Forms.Cow.EditParentForm import EditParentForm
from Models.Cow.CowModel import get_by_id, get_calves, get_all, get_all_dams, get_all_sires
from Forms.Cow.CowForm import CowForm
from Models.Cow.CowTable import CowTable
from Forms.Cow.EditCowForm import EditCowForm
from init import app
from Models import Treatment


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/herd')
def herd():
	herdTable = CowTable(get_all())
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
	weights = Treatment.WeightTable(Treatment.get_weights(tempCow), show_parent=False)
	events = Treatment.EventTable(Treatment.get_events(tempCow),show_parent=False)
	treats = Treatment.TreatmentTable(Treatment.get_treatments(tempCow),show_parent=False)
	pregnancyChecks = Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks(tempCow),show_parent=False)
	breedings = Treatment.BredTable(Treatment.get_breedings(tempCow),show_parent=False)
	return render_template("/Cow/Cow.html", cow=tempCow, calves=calves, weights=weights, events=events,
	                       treatments=treats, pregnancyCheck=pregnancyChecks, breedings=breedings, dam=dam, sire=sire)


@app.route('/herd/<cowId>/treatment', methods=["GET", "POST"])
def treatment(cowId):
	tempCow = get_by_id(cowId)
	eventForm = Treatment.EventForm()
	treatmentForm = Treatment.TreatmentForm()
	weightForm = Treatment.WeightForm()
	pregnancyCheckForm = Treatment.PregnancyCheckForm()
	bredForm = Treatment.BredForm()

	if tempCow is not None:
		form = Treatment.Form()
		# Set choices for form type on frontend
		form.formType.choices = [("Event", "Event"), ("Treatment", "Treatment"), ("Weight", "Weight")]
		if tempCow.sex == "cow":
			form.formType.choices.append(("Pregnancy Check", "Pregnancy Check"))
			form.formType.choices.append(("Bred", "Bred"))
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
		else:
			item = form
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


def event(cowId):
	pass


@app.route('/herd/treatments')
def treatments():
	treatType = request.args.get("type")
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


@app.route('/api/dams')
@as_json
def get_dams():
	return get_all_dams()


@app.route('/api/sires')
@as_json
def get_sires():
	return get_all_sires()


@app.route('/api/herd')
@as_json
def get_herd():
	return get_all()


@app.route('/api/herd/duedates')
@as_json
def get_due_dates():
	start = request.args.get("start")
	end = request.args.get("end")

	if start is not None and end is not None:
		startDate = dateutil.parser.isoparse(start)
		endDate = dateutil.parser.isoparse(end)
		dueDates = Treatment.get_due_dates(startDate, endDate)
		#print(startDate, endDate, dueDates)
		return dueDates
	return "error"
