from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from CowBook.app import db

ModelForm = model_form_factory(FlaskForm)
from CowBook.Models.Note import Note


class NoteForm(ModelForm):
	class Meta:
		model = Note

	def save(self, parent):
		note = Note(parent, self.date.data, self.text.data)
		db.session.add(note)
		db.session.commit()
		return note
