import pytest

from CowBook.app import db
from CowBook.init import create_app


class Config:
	pass


@pytest.fixture
def client():
	config = Config()
	config.SQLALCHEMY_DATABASE_URI = 'sqlite://'
	config.TESTING = True
	config.EMAIL = "test"
	config.PASSWORD = "test"
	config.LOGIN_DISABLED = True
	config.WTF_CSRF_ENABLED = False
	config.SECURITY_PASSWORD_SALT = "moo"
	app = create_app(config)
	with app.test_client() as client:
		with app.app_context():
			db.create_all()
		yield client
