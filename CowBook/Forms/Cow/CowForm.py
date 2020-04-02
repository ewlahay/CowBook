import os
import string

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import SubmitField, StringField
from wtforms_alchemy import model_form_factory
from PIL import Image
from CowBook.Models.Cow.CowModel import Cow
from CowBook.app import db
import random
from os import path
ModelForm = model_form_factory(FlaskForm)

IMAGE_SIZE = 600
IMAGE_FORMAT = ".jpeg"


def get_filename() -> str:
	"""Returns an unused filename for an image"""
	rand = get_random_string()
	while path.exists(rand + IMAGE_FORMAT):
		rand = get_random_string()
	return rand


def get_random_string() -> str:
	return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


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
			image = Image.open(self.photo.data)
			filename = get_filename()

			# exif = image.info['exif']
			image.save('Cowbook/static/Pictures/{}{}'.format(filename, IMAGE_FORMAT), IMAGE_FORMAT[1:])
			width, height = image.size

			if width > height:
				size = (IMAGE_SIZE, height / width * IMAGE_SIZE)
			else:
				size = (width / height, IMAGE_SIZE)
			image.thumbnail(size)

			image.save('Cowbook/static/Pictures/small/{}{}'.format(filename, IMAGE_FORMAT), IMAGE_FORMAT[1:])
			return filename + IMAGE_FORMAT
		return None

	def save(self):
		#print(self.photo.data)
		filename = self.save_photo()
		cow = Cow(self.name.data, self.earTag.data, self.dob.data, self.sex.data, bool(self.carrier.data),
		          self.owner.data, self.markings.data, filename)
		db.session.add(cow)
		db.session.commit()
		return cow
