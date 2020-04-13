from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_security import login_required, current_user

from CowBook.Forms.NoteForm import NoteForm
from CowBook.Forms.BredForm import BredForm
from CowBook.Forms.Cow.EditParentForm import EditParentForm
from CowBook.Forms.DeathForm import DeathForm
from CowBook.Forms.EditTreatmentForm import EditTreatmentForm
from CowBook.Forms.EventForm import EventForm
from CowBook.Forms.PregnancyCheckForm import PregnancyCheckForm
from CowBook.Forms.SaleForm import SaleForm
from CowBook.Forms.TreatmentForm import TreatmentForm
from CowBook.Forms.WeightForm import WeightForm
from CowBook.Models.Cow.CowModel import get_by_id, get_calves, get_all, get_active
from CowBook.Forms.Cow.CowForm import CowForm
from CowBook.Models.Cow.CowTable import CowTable
from CowBook.Forms.Cow.EditCowForm import EditCowForm
from CowBook.Models.Death import get_dead
from CowBook.Models.DeathTable import DeathTable
from CowBook.Models.Note import NoteTable
from CowBook.Models.Sale import get_sold
from CowBook.Models.SoldTable import SoldTable
from CowBook.Models import Treatment

app = Blueprint('app', __name__, url_prefix='/')


@app.context_processor
def inject_user():
	return dict(user=current_user)


@app.route('/')
def index():
	return render_template("index.html")


@app.route("/user")
@login_required
def user():
	return render_template("security/User.html")


@app.route('/herd')
def herd():
	tableType = request.args.get("type")
	# data =
	types = {
		"all": get_all,
		"active": get_active,
		"sold": get_sold,
		"dead": get_dead,
	}
	try:
		data = types[tableType]
	except KeyError:
		return render_template("Herd.html", table=CowTable(get_all()))

	if data is not None:
		data = data()
	if tableType == "sold":
		herdTable = SoldTable(data)
	elif tableType == "dead":
		herdTable = DeathTable(data)
	else:
		herdTable = CowTable(data)
	return render_template("Herd.html", table=herdTable, type=tableType)


@app.route('/herd/add', methods=["GET", "POST"])
@login_required
def add_cow():
	form = CowForm()
	if form.validate_on_submit():
		tempCow = form.save()
		return redirect(url_for('app.cow', cowId=tempCow.id))
	return render_template("/Cow/AddCow.html", form=form)


@app.route('/herd/duedates')
def view_due_date():
	defaultDate = Treatment.get_next_due_date() or datetime.now()
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
	treats = Treatment.TreatmentTable(Treatment.get_treatments(tempCow))
	pregnancyChecks = Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks(tempCow))
	breedings = Treatment.BredTable(Treatment.get_breedings(tempCow))
	notes = NoteTable(tempCow.notes)

	return render_template("/Cow/Cow.html", cow=tempCow, calves=calves, weights=weights, events=events,
	                       treatments=treats, pregnancyCheck=pregnancyChecks, notes=notes, breedings=breedings, dam=dam,
	                       sire=sire)


@app.route('/herd/<cowId>/stats')
def stats(cowId):
	tempCow = get_by_id(cowId)
	if tempCow is None:
		return render_template('/Error/404.html', content="Cow {} not found".format(cowId))
	return render_template('/Cow/Dashboard.html', cow=tempCow)


def handle_add_event_form(tempCow=None):
	"""Creates and validates a multi use form"""
	# Single form with every possible field
	form = Treatment.Form()
	# Set choices for form type on frontend
	form.formType.choices = [("Event", "Event"), ("Treatment", "Treatment"), ("Weight", "Weight"), ("Sale", "Sale"),
	                         ("Death", "Death")]
	if tempCow is None or tempCow.sex == "cow":
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
	return item


@app.route('/herd/<cowId>/addEvent', methods=["GET", "POST"])
@login_required
def treatment(cowId):
	tempCow = get_by_id(cowId)
	if tempCow is not None:
		item = handle_add_event_form(tempCow)
		if item.validate_on_submit():
			item.save(cowId)
		else:
			if request.method == 'POST':
				item.validate()
			return render_template("/Cow/AddTreatment.html", cow=tempCow, form=item)
		return redirect(url_for('app.cow', cowId=cowId))
	else:
		return render_template("/Error/404.html")


@app.route('/herd/<cowId>/addNote', methods=["GET", "POST"])
@login_required
def add_note(cowId):
	tempCow = get_by_id(cowId)
	if tempCow is not None:
		form = NoteForm()

		if form.validate_on_submit():
			form.save(cowId)
		else:
			if request.method == 'POST':
				form.validate()
			return render_template("/Cow/AddNote.html", cow=tempCow, form=form)
		return redirect(url_for('app.cow', cowId=cowId))
	else:
		return render_template("/Error/404.html", content="Cow not found!")


@app.route('/herd/<cowId>/edit', methods=["GET", "POST"])
@login_required
def edit_cow(cowId):
	tempCow = get_by_id(cowId)
	if tempCow is None:
		return render_template('/Error/404.html', content="Cow {} not found".format(cowId))
	form = EditCowForm(cowId)
	if form.validate_on_submit():
		form.save()
		return redirect(url_for('app.cow', cowId=cowId))
	form.setup()
	return render_template("/Cow/Edit.html", cow=tempCow, form=form)


@app.route('/herd/<cowId>/edit/dam', methods=["GET", "POST"])
@login_required
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
		return redirect(url_for('app.cow', cowId=cowId))
	return render_template("/Cow/EditParent.html", cow=newCow, form=form)


@app.route('/herd/<cowId>/edit/sire', methods=["GET", "POST"])
@login_required
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
		return redirect(url_for('app.cow', cowId=cowId))
	return render_template("/Cow/EditParent.html", cow=newCow, form=form)


@app.route('/herd/treatments')
def treatments():
	treatType = request.args.get("type")
	tables = []
	if treatType == "medical":
		tables.append(Treatment.TreatmentTable(Treatment.get_treatments()))
	elif treatType == "weight":
		tables.append(Treatment.WeightTable(Treatment.get_weights()))
	elif treatType == "pregnancyCheck":
		tables.append(Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks()))
	elif treatType == "breeding":
		tables.append(Treatment.BredTable(Treatment.get_breedings()))
	else:
		treatType = "all"
		tables.append(Treatment.EventTable(Treatment.get_events()))
		tables.append(Treatment.TreatmentTable(Treatment.get_treatments()))
		tables.append(Treatment.WeightTable(Treatment.get_weights()))
		tables.append(Treatment.BredTable(Treatment.get_breedings()))
		tables.append(Treatment.PregnancyCheckTable(Treatment.get_pregnancy_checks()))
	return render_template("Treatments.html", tables=tables, treat=treatType)


@app.route('/herd/treatments/<treatId>/edit', methods=["GET", "POST"])
@login_required
def edit_treatment(treatId):
	treat = Treatment.get_treatment(treatId)
	if treat is None:
		return render_template('/Error/404.html', content="Treatment {} not found".format(treat))
	form = EditTreatmentForm(treatId)
	if form.validate_on_submit():
		try:
			form.save(None)
		except ValueError as e:
			flash(e)
			return render_template("/EditTreatment.html", form=form, treat=treat)
		return redirect(url_for('app.cow', cowId=treat.parent))
	form.setup()
	return render_template("/EditTreatment.html", form=form, treat=treat)


@app.route('/herd/treatments/customform', methods=['GET', 'POST'])
@login_required
def custom_form_treatment():
	form = handle_add_event_form()
	if request.method == 'POST':
		if form.validate():
			kwargs = request.form.copy()
			kwargs['csrf_token'] = None
			kwargs['submit'] = None
			for key, value in request.form.items():
				if value is None or value == "":
					del kwargs[key]
			return redirect(url_for('app.custom_form', **kwargs))
	return render_template("/Cow/AddTreatment.html", form=form)


@app.route('/herd/treatments/custom')
@login_required
def custom_form():
	formType = {
		"Event": EventForm,
		"Treatment": TreatmentForm,
		"Weight": WeightForm,
		"Pregnancy Check": PregnancyCheckForm,
		"Bred": BredForm,
		"Sale": SaleForm,
		"Death": DeathForm,
	}
	if len(request.args) > 0:
		args = request.args.copy()
		try:
			form = formType[args['formType']]()
			args['csrf_token'] = None
			date = args['date']
			date = datetime.strptime(date, "%Y-%m-%d")
			del args['date']
			form.date.data = date
			try:
				exp = args['expiration']
				exp = datetime.strptime(exp, "%Y-%m-%d")
				del args['expiration']
			except KeyError:
				pass
		except KeyError:
			return render_template('/Error/404.html', content="Invalid Parameters")

		if form is not None:
			for key, value in args.items():
				try:
					form[key].data = value
				except KeyError:
					pass
			return render_template("/CustomEventForm.html", form=form, formType=args['formType'])
	return render_template('/Error/404.html', content="Invalid form")
