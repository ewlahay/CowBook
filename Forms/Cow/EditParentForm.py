from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField

from Models.Cow.CowModel import get_by_id, Cow
from init import db


class EditParentForm(FlaskForm):
	id = IntegerField("Parent ID")
	submit = SubmitField()

	def __init__(self, cowId, parent="sire"):
		FlaskForm.__init__(self)
		self.cowId = cowId
		if parent not in ["dam", "sire"]:
			raise ValueError("Parent must be either dam or sire")
		self.parentType = parent

	def validate(self):
		super().validate()
		tempCow = get_by_id(self.id.data)
		if tempCow is not None:
			if self.parentType == "dam" and tempCow.sex == "cow":
				return True
			if self.parentType == "sire" and tempCow.sex == "bull":
				return True
		return False

	def save(self):
		tempCow = get_by_id(self.cowId)
		if tempCow is not None:
			if self.parentType == "dam":
				tempCow.set_dam_id(self.id.data)
			if self.parentType == "sire":
				tempCow.set_sire_id(self.id.data)
			db.session.add(tempCow)
			db.session.commit()
		return tempCow
