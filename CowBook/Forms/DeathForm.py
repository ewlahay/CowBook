from flask import flash
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from CowBook.init import db

ModelForm = model_form_factory(FlaskForm)
from CowBook.Models.Death import Death, get_by_parent_id


class DeathForm(ModelForm):
	class Meta:
		model = Death

	def save(self, parent):
		if get_by_parent_id(parent) is None:
			sold = Death(parent, self.date.data, self.cause.data)
			db.session.add(sold)
			db.session.commit()
			return sold
		else:
			flash("Cow has already died!")
