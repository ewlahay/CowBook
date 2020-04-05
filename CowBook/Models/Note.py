from flask_table import Table, Col
from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from CowBook.app import db


class Note(db.Model):
	_tablename_ = "note"

	id = Column(Integer, primary_key=True, autoincrement=True)
	parent = Column(Integer, ForeignKey('Cow.id'))
	cow = relationship("Cow")
	date = Column(Date, nullable=False)
	text = Column(String, nullable=False)

	def __init__(self, parent, date, text):
		self.parent = parent
		self.date = date
		self.text = text


class NoteTable(Table):
	table_id = "NoteTable"
	date = Col("Date")
	text = Col("Text")
