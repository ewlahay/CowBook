from flask import url_for
from flask_table import Col
from CowBook.Models.Cow.CowModel import get_by_name, get_by_id
template = '''<div class="tooltip">{link}
			<div class="card">
			        <img id="image" src="{img}">
			        <div class="textContainer">
			            <h3 id="name">{name}</h3>
			            <p id="dob">{dob}</p>
			            <p id="tag">{tag}</p>
			            <p id="sex">{sex}</p>
			            <p id="owner">{owner}</p>
			        </div>
			    </div>
			</div>'''  # Not used here


class CowNameLinkCol(Col):
	def td_format(self, content):
		cow = get_by_name(content)
		if cow is not None:
			return format_card(cow)
		# url = url_for("app.cow", cowId=cow.id)
		# return '<a href="{}">{}</a>'.format(url, content)
		return content


class CowIdLinkCol(Col):
	def td_format(self, content):
		cow = get_by_id(content)
		if cow is not None:
			return format_card(cow)
		# url = url_for("app.cow", cowId=cow.id)
		# return '<a href="{}">{}</a>'.format(url, cow.name)
		return content


def format_card(cow):
	url = url_for("app.cow", cowId=cow.id)
	link = '<a href="{}" onmouseover="renderCard(this)">{}</a>'.format(url, cow.name)
	return link
