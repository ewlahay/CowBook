from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, func
import enum
from datetime import datetime

from sqlalchemy.orm import relationship

from CowBook.Models.Death import Death
from CowBook.Models.Sale import Sale
from CowBook.app import db


class Sex(enum.Enum):
	male = 2
	female = 1
	steer = 3


class Cow(db.Model):
	__tablename__ = "Cow"

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, unique=True)
	earTag = Column(Integer)
	dob = Column(Date, nullable=False)
	dam_id = Column(Integer, nullable=True)
	# dam = relationship("Cow", foreign_keys=[dam_id])

	sire_id = Column(Integer, nullable=True)
	# sire = relationship("Cow", foreign_keys=[sire_id])
	sex = Column(Enum("cow", "bull", "steer"), nullable=False)
	# calves = relationship("Cow", foreign_keys=[sire_id, dam_id])
	carrier = Column(Boolean)
	owner = Column(String, nullable=False)
	markings = Column(String)
	photo = Column(String)
	active = Column(Boolean)

	sale = relationship("Sale", uselist=False, back_populates="cow")
	death = relationship("Death", uselist=False, back_populates="cow")
	notes = relationship("Note", back_populates="cow")

	# treatments = relationship("Treatment", uselist=False, backref="cow")
	# events = relationship("Event", uselist=False, backref="cow")
	# weights = relationship("Weight", uselist=False, backref="cow")
	# pregnancychecks = relationship("PregnancyCheck", uselist=False, backref="cow")
	# breds = relationship("Bred", uselist=False, backref="cow")

	@property
	def is_heifer(self):
		calves = get_calves(self)
		if len(calves) == 0 and self.sex == "cow":
			return True
		return False

	@property
	def is_sold(self):
		sale = db.session.query(Sale).filter_by(parent=self.id).first()
		return sale is not None

	@property
	def is_dead(self):
		death = db.session.query(Death).filter_by(parent=self.id).first()
		return death is not None

	@property
	def status(self):
		if self.is_dead:
			return "dead"
		if self.is_sold:
			return "sold"
		return "{} years old".format(((datetime.now().date() - self.dob).days / 365).__round__(2))

	@property
	def age(self):
		return ((datetime.now().date() - self.dob).days / 365).__round__(2)

	@property
	def calves(self):
		return get_calves(self)

	@property
	def is_active(self):
		return self.active and not self.is_sold and not self.is_dead

	def set_dam_id(self, dam_id):
		if dam_id == self.id:
			raise ValueError("Can't set as own mother")
		self.check_age(dam_id)
		self.dam_id = dam_id

	def set_sire_id(self, sire_id):
		if sire_id == self.id:
			raise ValueError("Can't set as own father")
		self.check_age(sire_id)
		self.sire_id = sire_id

	def check_age(self, cow2Id):
		cow2 = get_by_id(cow2Id)
		if cow2 is not None:
			if cow2.dob > self.dob:
				raise ValueError("Parent can't be born after child")
		else:
			raise ValueError("Parent doesn't exist!")

	def __init__(self, name, earTag, dob: datetime, sex, carrier, owner, markings, photo, active=True):
		self.name = name or earTag  # Empty names default to earTag number
		self.earTag = earTag
		self.dob = dob  # datetime.strptime(dob, "%Y-%m-%d")
		self.sex = sex
		self.carrier = carrier
		self.owner = owner
		self.markings = markings
		self.photo = photo
		self.active = active

	# self.active = active

	def __str__(self):
		return "{} #{} {}".format(self.name, self.earTag, self.dob.strftime("%m/%d/%Y"))

	def __json__(self):
		value = {
			'id': self.id,
			'name': self.name,
			'earTag': self.earTag,
			'dob': self.dob.strftime("%m/%d/%Y"),
			'dam_id': self.dam_id,
			'sire_id': self.sire_id,
			'sex': self.sex,
			'carrier': self.carrier,
			'owner': self.owner,
			'markings': self.markings,
			'photo': self.photo,
			'isHeifer': self.is_heifer,
			'age': self.age
		}
		return value

	def save(self):
		"""Save the cow to the database"""
		db.session.add(self)
		db.session.commit()


def get_by_id(cowId):
	cow = db.session.query(Cow).filter_by(id=cowId).first()
	return cow


def get_calves(cow):
	calves = db.session.query(Cow).filter((Cow.dam_id == cow.id) | (Cow.sire_id == cow.id)).all()
	return calves


def get_all_dams():
	dams = db.session.query(Cow).filter(Cow.sex == "cow").all()
	return dams


def get_all_sires():
	return db.session.query(Cow).filter(Cow.sex == "bull").all()


def get_by_name(name: str) -> Cow:
	if name is None or len(name) == 0:
		return None
	name = "{}%".format(name.lower())
	# return db.session.query(Cow).filter(func.lower(Cow.name) == func.lower(name)).first()
	return db.session.query(Cow).filter(func.lower(Cow.name).like(name)).first()


def get_active():
	cows = db.session.query(Cow).filter(Cow.active == True).all()
	activeCows = [x for x in cows if x.is_active]
	return activeCows


def get_inactive() -> [Cow]:
	""" Returns a list of cows marked as inactive"""
	cows = db.session.query(Cow).filter(Cow.active == False).all()
	return cows


def get_all():
	cows = Cow.query.all()
	return cows
