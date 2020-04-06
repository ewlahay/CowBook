import json

from flask.testing import FlaskClient


def login(client: FlaskClient, username, password):
	data = dict(email=username, password=password, submit="Login", next="")
	return client.post('/login', query_string=data, data=data, follow_redirects=True)


def logout(client):
	return client.get('/logout', follow_redirects=True)


def add_cow(client, cow=None):
	login(client, "test", "test")
	if cow is None:
		cow = {"name": "Dotty", "dob": "2012-10-19", "earTag": 45, "sex": "cow", "owner": "Molly",
		       "markings": "Greyish yellow"}
	client.post("/herd/add", data=cow, follow_redirects=True)
	rv = client.get('/api/herd?filter=all')

	data = json.loads(rv.data)[0]
	assert data["name"] == "Dotty"
	assert data["isHeifer"] is True
	assert data["earTag"] == 45
	assert data["dob"] == "10/19/2012"
	assert data["sex"] == "cow"
	assert data["carrier"] is False
	assert data["owner"] == "Molly"
