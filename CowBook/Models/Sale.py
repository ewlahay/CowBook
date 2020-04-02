from sqlalchemy import Column, Integer, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

from CowBook.app import db


class Sale(db.Model):
	_tablename_ = "sale"

	id = Column(Integer, primary_key=True, autoincrement=True)
	parent = Column(Integer, ForeignKey('Cow.id'))
	cow = relationship("Cow")
	date = Column(Date, nullable=False)
	weight = Column(Float, nullable=False)
	perPound = Column(Float, nullable=False)
	total = Column(Float, nullable=False)

	def __init__(self, parent, date, weight, perPound, total):
		self.parent = parent
		self.date = date
		self.weight = weight
		self.perPound = perPound
		self.total = total


def get_by_parent_id(parent):
	return db.session.query(Sale).filter_by(parent=parent).first()


def get_sold(combine=True):
	if combine:
		return [union(x.cow, x) for x in Sale.query.all()]
	else:
		return [x.cow for x in Sale.query.all()]


def union(cow, sale):
	"""Combines a cow and a sale object"""
	return {
		"id": cow.id,
		"name": cow.name,
		"earTag": cow.earTag,
		"dob": cow.dob,
		"sex": cow.sex,
		"is_heifer": cow.is_heifer,
		"owner": cow.owner,
		"markings": cow.markings,
		"weight": sale.weight,
		"perPound": sale.perPound,
		"total": sale.total
	}
