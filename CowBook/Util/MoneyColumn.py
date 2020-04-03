from flask_table import Col


class MoneyCol(Col):
	"""Adds a dollar sign in front of column values"""

	def td_format(self, content: float):
		return "${:.2f}".format(content)
