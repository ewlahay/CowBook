# Flask-Admin views
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import current_user
from flask import url_for, redirect, request, abort


class BaseView(ModelView):
	form_base_class = SecureForm
	can_create = False

	def is_accessible(self):
		return current_user.is_active and current_user.is_authenticated

	def _handle_view(self, name, **kwargs):
		"""
		Override builtin _handle_view in order to redirect users when a view is not accessible.
		"""
		if not self.is_accessible():
			if current_user.is_authenticated:
				# permission denied
				abort(403)
			else:
				# login
				return redirect(url_for('security.login', next=request.url))


class UserView(BaseView):
	can_create = True
	column_exclude_list = ['password', 'username', 'confirmed_at']
	form_create_rules = ('email', 'password')
	can_edit = False


class TreatmentView(BaseView):
	form_ajax_refs = {
		'cow': {
			'fields': ['name', ],
			'page_size': 10
		}
	}


class CowView(BaseView):
	can_edit = False
