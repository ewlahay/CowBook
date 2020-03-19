from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Boolean, and_, func, desc
from sqlalchemy.ext.declarative import declared_attr
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, IntegerField, BooleanField, DateField, FloatField, SelectField
from wtforms_alchemy import model_form_factory
from flask_table import Table, Col, LinkCol, BoolCol
from datetime import datetime, timedelta

from Models.Cow import CowModel
from init import db

MIN_GESTATION = 279

ModelForm = model_form_factory(FlaskForm)


class Base(object):
	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

	id = Column(Integer, primary_key=True, autoincrement=True)
	date = Column(Date, nullable=False)
	type = Column(String)

	@declared_attr
	def parent(self):  # The cow that the event belongs to/is linked to in the database.
		return Column(Integer, ForeignKey('Cow.id'))

	notes = Column(String)

	def __init__(self, date, type, parent, notes):
		self.date = date
		self.type = type
		self.parent = parent
		self.notes = notes


class Event(Base, db.Model):
	# everything is inherited
	pass


class EventForm(ModelForm):
	class Meta:
		model = Event

	submit = SubmitField()

	def save(self, parent):
		event = Event(self.date.data, self.type.data, parent, self.notes.data)
		db.session.add(event)
		db.session.commit()
		return event


class EventTable(Table):
	table_id = "Events"

	@property
	def parent(self):
		if self.show_parent is True:
			return LinkCol("Cow", 'cow', url_kwargs=dict(cowId='parent'), attr='parent')
		else:
			return None

	date = Col("Date")
	type = Col("Type")
	notes = Col("Notes")

	def __init__(self, items, classes=None, thead_classes=None, sort_by=None, sort_reverse=False, no_items=None,
	             table_id=None, border=None, html_attrs=None, show_parent=True):
		super().__init__(items, classes, thead_classes, sort_by, sort_reverse, no_items, table_id, border, html_attrs)
		self.show_parent = show_parent

	@parent.setter
	def parent(self, value):
		self._parent = value


class Treatment(Base, db.Model):
	lotNo = Column(String)
	expiration = Column(Date)
	withdrawal = Column(Integer)
	dosage = Column(Integer)
	unit = Column(String)

	def __init__(self, date, type, parent, notes, lotNo, expiration, withdrawal, dosage, unit):
		super().__init__(date, type, parent, notes)
		self.lotNo = lotNo
		self.expiration = expiration
		self.withdrawal = withdrawal
		self.dosage = dosage
		self.unit = unit


class TreatmentForm(ModelForm):
	''''lotNo = StringField("Lot #")
	expiration = DateField("Expiration")
	withdrawal = IntegerField("Withdrawal (Days)")
	dosage = IntegerField("Dosage")
	unit = StringField("Unit")'''

	class Meta:
		model = Treatment

	def save(self, parent):
		treatment = Treatment(self.date.data, self.type.data, parent, self.notes.data, self.lotNo.data,
		                      self.expiration.data, self.withdrawal.data, self.dosage.data, self.unit.data)
		db.session.add(treatment)
		db.session.commit()
		return treatment


class TreatmentTable(EventTable):
	table_id = "Treatments"
	lotNo = Col("Lot #")
	expiration = Col("Expiration")
	withdrawal = Col("Withdrawal time (Days)")
	dosage = Col("Dose")
	unit = Col("Unit")


class Weight(Base, db.Model):
	weight = Column(Float)

	def __init__(self, date, type, parent, notes, weight):
		super().__init__(date, type, parent, notes)
		self.weight = weight

	def to_string(self):
		return "weight: {} date: {} parent: {}".format(self.weight, self.date, self.parent)


class WeightForm(ModelForm):
	class Meta:
		model = Weight

	# weight = FloatField("Weight")

	def save(self, parent):
		weight = Weight(self.date.data, self.type.data, parent, self.notes.data, self.weight.data)
		db.session.add(weight)
		db.session.commit()
		return weight


class WeightTable(EventTable):
	table_id = "Weights"
	weight = Col("Weight")


class PregnancyCheck(Base, db.Model):
	pregnant = Column(Boolean)

	def __init__(self, date, type, parent, notes, pregnant):
		super().__init__(date, type, parent, notes)
		self.pregnant = pregnant


class PregnancyCheckForm(ModelForm):
	# pregnant = BooleanField("Pregnant")
	class Meta:
		model = PregnancyCheck

	def save(self, parent):
		pregnancyCheck = PregnancyCheck(self.date.data, self.type.data, parent, self.notes.data, self.pregnant.data)
		db.session.add(pregnancyCheck)
		db.session.commit()
		return pregnancyCheck


class PregnancyCheckTable(EventTable):
	table_id = "PregnancyChecks"
	pregnant = BoolCol("Pregnant")


class Bred(Base, db.Model):
	sire = Column(String)

	def __init__(self, date, type, parent, notes, sire):
		super().__init__(date, type, parent, notes)
		self.sire = sire


class BredForm(ModelForm):
	class Meta:
		model = Bred

	def save(self, parent):
		bred = Bred(self.date.data, self.type.data, parent, self.notes.data, self.sire.data)
		db.session.add(bred)
		db.session.commit()
		return Bred


class BredTable(EventTable):
	table_id = "breedingHistory"
	sire = Col("Sire")


class Form(FlaskForm):
	formType = SelectField("Type")
	date = DateField("Date", render_kw={"value": datetime.now().date().isoformat(), "type": "date"})
	type = StringField("Type")
	notes = StringField("Notes")

	lotNo = StringField("Lot #")
	expiration = DateField("Expiration", render_kw={"type": "date"})
	withdrawal = IntegerField("Withdrawal (Days)", )
	dosage = IntegerField("Dosage")
	unit = StringField("Unit")

	weight = FloatField("Weight")

	pregnant = BooleanField("Pregnant")
	sire = StringField("Sire")
	submit = SubmitField("Save")


def get_weights(cow=None):
	if cow is None:
		return db.session.query(Weight)
	return db.session.query(Weight).filter_by(parent=cow.id)


def get_events(cow=None):
	if cow is None:
		return db.session.query(Event).all()
	return db.session.query(Event).filter_by(parent=cow.id)


def get_treatments(cow=None):
	if cow is None:
		return db.session.query(Treatment).all()
	return db.session.query(Treatment).filter_by(parent=cow.id)


def get_pregnancy_checks(cow=None):
	if cow is None:
		return db.session.query(PregnancyCheck).all()
	return db.session.query(PregnancyCheck).filter_by(parent=cow.id)


def get_all_events():
	events = get_events()
	events.extend(get_weights())
	events.extend(get_treatments())
	events.extend(get_pregnancy_checks())
	return events


def get_breedings(tempCow=None):
	if tempCow is None:
		return db.session.query(Bred).all()
	return db.session.query(Bred).filter_by(parent=tempCow.id)


def get_due_dates(start, end):

	dates = db.session.query(Bred).filter(
		and_(
			func.date(Bred.date) >= start - timedelta(days=288), func.date(Bred.date) <= end - timedelta(days=MIN_GESTATION)
		)
	)
	#dates = db.session.query(Bred).filter(Bred.date.between(start, end)).all()
	dueDates = []
	for date in dates:
		tempCow = CowModel.get_by_id(date.parent)
		dueDates.append(
			{
				'title': tempCow.name,
				'allDay': True,
				'url': '/herd/{}'.format(date.parent),
				'start': date.date + timedelta(days=MIN_GESTATION),
				'end': date.date + timedelta(days=287)
			}
		)
	return dueDates


def get_next_due_date():
	first = db.session.query(Bred).order_by(desc(Bred.date)).first()
	return first.date + timedelta(MIN_GESTATION)
