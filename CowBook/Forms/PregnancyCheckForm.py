from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from CowBook.app import db

ModelForm = model_form_factory(FlaskForm)
from CowBook.Models.Treatment import PregnancyCheck


class PregnancyCheckForm(ModelForm):
	# pregnant = BooleanField("Pregnant")
	class Meta:
		model = PregnancyCheck

	def save(self, parent):
		pregnancyCheck = PregnancyCheck(self.date.data, self.type.data, parent, self.notes.data, self.pregnant.data)
		db.session.add(pregnancyCheck)
		db.session.commit()
		return pregnancyCheck
