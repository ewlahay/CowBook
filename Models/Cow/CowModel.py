from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Boolean, Enum
import json
import enum
from datetime import datetime
from init import db


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

	# events = relationship("Event")
	@property
	def is_heifer(self):
		calves = get_calves(self)
		if len(calves) == 0 and self.sex == "cow":
			return True
		return False

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

	def __init__(self, name, earTag, dob, sex, carrier, owner, markings, photo):
		self.name = name
		self.earTag = earTag
		self.dob = dob  # datetime.strptime(dob, "%Y-%m-%d")
		self.sex = sex
		self.carrier = carrier
		self.owner = owner
		self.markings = markings
		self.photo = photo

	def __str__(self):
		return "{} #{} {}".format(self.name, self.earTag, self.dob.strftime("%d/%m/%y"))

	def __json__(self):
		value = {
			'id': self.id,
			'name': self.name,
			'earTag': self.earTag,
			'dob': self.dob.strftime("%Y-%m-%d"),
			'dam_id': self.dam_id,
			'sire_id': self.sire_id,
			'sex': self.sex,
			'carrier': self.carrier,
			'owner': self.owner,
			'markings': self.markings,
			'photo': self.photo,
			'isHeifer': self.is_heifer
		}
		return value


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


def get_all():
	cows = Cow.query.all()
	return cows
