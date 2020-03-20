from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms_alchemy import model_form_factory

from init import db

ModelForm = model_form_factory(FlaskForm)
from Models.Treatment import Event


class EventForm(ModelForm):
	class Meta:
		model = Event

	submit = SubmitField()

	def save(self, parent):
		event = Event(self.date.data, self.type.data, parent, self.notes.data)
		db.session.add(event)
		db.session.commit()
		return event
