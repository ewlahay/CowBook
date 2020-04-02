from CowBook.Models.Cow.CowModel import get_by_id
from CowBook.Forms.Cow.CowForm import CowForm
from CowBook.app import db


class EditCowForm(CowForm):
	"""Used for editing a saved cow object, specifically for use with PUT requests"""

	def __init__(self, cowId):
		super().__init__()
		self.cowId = cowId

	def save(self):
		cow = get_by_id(self.cowId)
		# If statements are used instead of iterating over form.data since photo and carrier are edge cases that would be hard to handle otherwise
		if cow:
			if self.name.data:
				cow.name = self.name.data
			if self.earTag.data:
				cow.earTag = self.earTag.data
			if self.dob.data:
				cow.dob = self.dob.data
			if self.sex.data:
				cow.sex = self.sex.data
			if self.carrier.data:
				cow.carrier = bool(self.carrier.data)
			if self.owner.data:
				cow.owner = self.owner.data
			if self.markings.data:
				cow.markings = self.markings.data

		else:
			raise Exception("Cow not found!")
		filename = self.save_photo()
		if filename is not None:
			cow.photo = filename
		db.session.add(cow)
		db.session.commit()
		return cow

	def setup(self):
		cow = get_by_id(self.cowId)
		attributes = vars(cow)
		for attr in attributes:
			#print(attr)
			try:
				self[attr].data = cow.__getattribute__(attr)
			except KeyError:
				#print(attr)
				pass
