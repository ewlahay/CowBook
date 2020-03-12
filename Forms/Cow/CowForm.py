from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from wtforms.fields import SubmitField, DateField, StringField
from wtforms_alchemy import model_form_factory

from Models.Cow.CowModel import Cow
from init import db
ModelForm = model_form_factory(FlaskForm)


class CowForm(ModelForm):
	submit = SubmitField()

	class Meta:
		model = Cow
		exclude = ['dam_id', 'sire_id', 'photo', 'name']

	name = StringField("name")
	photo = FileField("photo",
	                  validators=[FileAllowed(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'], "Images only!")])

	# dob = DateField('dob', format='%Y-%m-%d')
	def save_photo(self):
		if self.photo.data:
			filename = secure_filename(self.photo.data.filename)
			self.photo.data.save('static/Pictures/' + filename)
			print(filename)
			return filename
		return None

	def save(self):
		#print(self.photo.data)
		filename = self.save_photo()
		cow = Cow(self.name.data, self.earTag.data, self.dob.data, self.sex.data, bool(self.carrier.data),
		          self.owner.data, self.markings.data, filename)
		db.session.add(cow)
		db.session.commit()
		return cow
