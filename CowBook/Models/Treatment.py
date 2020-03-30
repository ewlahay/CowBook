from datetime import datetime, timedelta
from typing import Union

from flask_table import Table, Col, LinkCol, BoolCol
from flask_wtf import FlaskForm
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean, and_, func, desc
from sqlalchemy.ext.declarative import declared_attr
from wtforms.fields import SubmitField, StringField, IntegerField, BooleanField, DateField, FloatField, SelectField
from wtforms_alchemy import model_form_factory

from CowBook.Models.Cow import CowModel
from CowBook.Util.DBLink import CowNameLinkCol
from CowBook.init import db

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


class EventTable(Table):
	table_id = "Events"
	title = table_id
	"""
	@property
	def parent(self):
		print("Getting parent!")
		if self.show_parent is True:
			return LinkCol("Cow", 'cow', url_kwargs=dict(cowId='parent'), attr='parent')
		else:
			return None
	"""
	parent = LinkCol("Cow", 'cow', url_kwargs=dict(cowId='parent'), attr='parent')
	date = Col("Date")
	type = Col("Type")
	notes = Col("Notes")

	def __init__(self, items, classes=None, thead_classes=None, sort_by=None, sort_reverse=False, no_items=None,
	             table_id=None, border=None, html_attrs=None, show_parent=True):
		self.show_parent = show_parent
		super().__init__(items, classes, thead_classes, sort_by, sort_reverse, no_items, table_id, border, html_attrs)


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


class TreatmentTable(EventTable):
	table_id = "Treatments"
	title = "Medical"
	lotNo = Col("Lot #")
	expiration = Col("Expiration")
	withdrawal = Col("Withdrawal time (Days)")
	dosage = Col("Dose")
	unit = Col("Unit")
	edit = LinkCol("Edit", "edit_treatment", url_kwargs=dict(treatId='id'), text_fallback="edit")


class Weight(Base, db.Model):
	weight = Column(Float)

	def __init__(self, date, type, parent, notes, weight):
		super().__init__(date, type, parent, notes)
		self.weight = weight

	def to_string(self):
		return "weight: {} date: {} parent: {}".format(self.weight, self.date, self.parent)


class WeightTable(EventTable):
	table_id = "Weights"
	title = table_id
	weight = Col("Weight")


class PregnancyCheck(Base, db.Model):
	pregnant = Column(Boolean)

	def __init__(self, date, type, parent, notes, pregnant):
		super().__init__(date, type, parent, notes)
		self.pregnant = pregnant


class PregnancyCheckTable(EventTable):
	table_id = "PregnancyChecks"
	title = "Pregnancy Checks"
	pregnant = BoolCol("Pregnant")


class Bred(Base, db.Model):
	sire = Column(String)

	def __init__(self, date, type, parent, notes, sire):
		super().__init__(date, type, parent, notes)
		self.sire = sire


class BredTable(EventTable):
	table_id = "breedingHistory"
	title = "Breeding History"
	sire = CowNameLinkCol("Sire")


class Form(FlaskForm):
	formType = SelectField("Type")
	date = DateField("Date", render_kw={"value": datetime.now().date().isoformat(), "type": "date"})
	type = StringField("Type")

	lotNo = StringField("Lot #")
	expiration = DateField("Expiration", render_kw={"type": "date"})
	withdrawal = IntegerField("Withdrawal (Days)", )
	dosage = IntegerField("Dosage")
	unit = StringField("Unit")

	weight = FloatField("Weight")
	perPound = FloatField("Per Pound")
	total = FloatField("Total")

	pregnant = BooleanField("Pregnant")
	sire = StringField("Sire")

	notes = StringField("Notes")

	cause = StringField("Cause of Death")

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


def get_treatment(id) -> Treatment:
	return db.session.query(Treatment).filter_by(id=id).first()


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
	"""Returns a list of due dates calculated as breeding date + 279 days and ending at breeding date + 287 days."""
	dates = db.session.query(Bred).filter(
		and_(
			func.date(Bred.date) >= start - timedelta(days=288), func.date(Bred.date) <= end - timedelta(days=MIN_GESTATION)
		)
	)
	dueDates = []
	for date in dates:
		tempCow = CowModel.get_by_id(date.parent)
		dueDates.append(
			{
				'title': "{} due to give birth".format(tempCow.name),
				'allDay': True,
				'url': '/herd/{}'.format(date.parent),
				'start': date.date + timedelta(days=MIN_GESTATION),
				'end': date.date + timedelta(days=287)
			}
		)
	return dueDates


def get_next_due_date() -> Union[datetime, None]:
	now = datetime.now() - timedelta(288)
	first = db.session.query(Bred).order_by(desc(Bred.date)).filter(func.date(Bred.date) >= now).first()
	if first is None:
		return None
	return first.date + timedelta(MIN_GESTATION)
