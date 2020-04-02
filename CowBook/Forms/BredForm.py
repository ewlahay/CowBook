from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from CowBook.app import db

ModelForm = model_form_factory(FlaskForm)
from CowBook.Models.Treatment import Bred


class BredForm(ModelForm):
	class Meta:
		model = Bred

	def save(self, parent):
		bred = Bred(self.date.data, self.type.data, parent, self.notes.data, self.sire.data)
		db.session.add(bred)
		db.session.commit()
		return Bred
