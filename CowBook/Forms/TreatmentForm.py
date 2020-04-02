from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from CowBook.app import db

ModelForm = model_form_factory(FlaskForm)
from CowBook.Models.Treatment import Treatment


class TreatmentForm(ModelForm):
	''''lotNo = StringField("Lot #")
	expiration = DateField("Expiration")
	withdrawal = IntegerField("Withdrawal (Days)")
	dosage = IntegerField("Dosage")
	unit = StringField("Unit")'''

	class Meta:
		model = Treatment

	def save(self, parent):
		treatment = Treatment(self.date.data, self.type.data, parent, self.notes.data, self.lotNo.data,
		                      self.expiration.data, self.withdrawal.data, self.dosage.data, self.unit.data)
		db.session.add(treatment)
		db.session.commit()
		return treatment
