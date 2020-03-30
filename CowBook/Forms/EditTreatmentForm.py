from wtforms import SubmitField
from CowBook.Forms.TreatmentForm import TreatmentForm
from CowBook.Models.Treatment import get_treatment
from CowBook.init import db


class EditTreatmentForm(TreatmentForm):
	submit = SubmitField()

	def __init__(self, treatmentId):
		super().__init__()
		self.treatmentId = treatmentId

	def save(self, parent):
		treatment = get_treatment(self.treatmentId)
		# If statements are used instead of iterating over form.data since photo and carrier are edge cases that would be hard to handle otherwise
		if treatment:
			attributes = vars(self)
			for attr in attributes:
				try:
					if self[attr].data:
						setattr(treatment, attr, self[attr].data)
				except KeyError:
					pass

		else:
			raise Exception("Treatment not found!")
		db.session.add(treatment)
		db.session.commit()
		return treatment

	def setup(self):
		print(self.treatmentId)
		treatment = get_treatment(self.treatmentId)
		print(treatment)
		attributes = vars(treatment)
		for attr in attributes:
			print(attr)
			try:
				self[attr].data = treatment.__getattribute__(attr)
			except KeyError:
				pass
