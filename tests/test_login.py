from tests.helpers import login, logout


def test_login_logout(client):
	"""Make sure login and logout works."""
	rv = login(client, "test", "test")
	assert b'Logout' in rv.data

	rv = logout(client)
	assert b'Login' in rv.data

	rv = login(client, "testr", "test")
	assert b'Specified user does not exist' in rv.data

	rv = login(client, "test", "testx")
	assert b'Invalid password' in rv.data
