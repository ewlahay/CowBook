from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from CowBook.init import db

ModelForm = model_form_factory(FlaskForm)
from CowBook.Models.Treatment import Weight


class WeightForm(ModelForm):
	class Meta:
		model = Weight

	# weight = FloatField("Weight")

	def save(self, parent):
		weight = Weight(self.date.data, self.type.data, parent, self.notes.data, self.weight.data)
		db.session.add(weight)
		db.session.commit()
		return weight
