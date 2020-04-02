from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from CowBook.app import db


class Death(db.Model):
	_tablename_ = "death"

	id = Column(Integer, primary_key=True, autoincrement=True)
	parent = Column(Integer, ForeignKey('Cow.id'))
	cow = relationship("Cow")
	date = Column(Date, nullable=False)
	cause = Column(String, nullable=False)

	def __init__(self, parent, date, cause):
		self.parent = parent
		self.date = date
		self.cause = cause


def get_by_parent_id(parent):
	return db.session.query(Death).filter_by(parent=parent).first()


def get_dead(combine=True):
	if combine:
		return [union(x.cow, x) for x in Death.query.all()]
	else:
		return [x.cow for x in Death.query.all()]


def union(cow, death):
	"""Combines a cow and a death object"""
	return {
		"id": cow.id,
		"name": cow.name,
		"earTag": cow.earTag,
		"dob": cow.dob,
		"sex": cow.sex,
		"is_heifer": cow.is_heifer,
		"owner": cow.owner,
		"markings": cow.markings,
		"date": death.date,
		"cause": death.cause
	}
