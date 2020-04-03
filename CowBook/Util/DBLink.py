from flask import url_for
from flask_table import Col
from CowBook.Models.Cow.CowModel import get_by_name, get_by_id


class CowNameLinkCol(Col):
	def td_format(self, content):
		cow = get_by_name(content)
		if cow is not None:
			url = url_for("app.cow", cowId=cow.id)
			return '<a href="{}">{}</a>'.format(url, content)
		return content


class CowIdLinkCol(Col):
	def td_format(self, content):
		cow = get_by_id(content)
		if cow is not None:
			url = url_for("app.cow", cowId=cow.id)
			return '<a href="{}">{}</a>'.format(url, cow.name)
		return content
