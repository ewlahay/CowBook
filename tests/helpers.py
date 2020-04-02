from flask.testing import FlaskClient


def login(client: FlaskClient, username, password):
	data = dict(email=username, password=password, submit="Login", next="")
	return client.post('/login', query_string=data, data=data, follow_redirects=True)


def logout(client):
	return client.get('/logout', follow_redirects=True)
