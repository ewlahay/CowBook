from flask import url_for
from flask_table import Col
from CowBook.Models.Cow.CowModel import get_by_name


class CowNameLinkCol(Col):
	def td_format(self, content):
		cow = get_by_name(content)
		if cow is not None:
			url = url_for("app.cow", cowId=cow.id)
			return '<a href="{}">{}</a>'.format(url, content)
		return content
