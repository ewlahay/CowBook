from flask import flash
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from CowBook.app import db

ModelForm = model_form_factory(FlaskForm)
from CowBook.Models.Sale import Sale, get_by_parent_id


class SaleForm(ModelForm):
	class Meta:
		model = Sale

	def save(self, parent):
		if get_by_parent_id(parent) is None:
			sold = Sale(parent, self.date.data, self.weight.data, self.perPound.data, self.total.data)
			db.session.add(sold)
			db.session.commit()
			print("Cow sold!")
			return sold
		else:
			flash("Cow has already been sold!")
