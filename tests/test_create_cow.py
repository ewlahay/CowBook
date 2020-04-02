import json
import os
import tempfile
import unittest

from tests.helpers import login


def test_empty_db(client):
	"""Start with a blank database."""
	rv = client.get('/api/herd?filter=all')
	print(rv.data)
	assert b'[]' in rv.data


def test_add_cow(client):
	login(client, "test", "test")
	cow = {"name": "Dotty", "dob": "2012-10-19", "earTag": 45, "sex": "cow", "owner": "Molly",
	       "markings": "Greyish yellow"}
	client.post("/herd/add", data=cow, follow_redirects=True)

	rv = client.get('/api/herd?filter=all')

	data = json.loads(rv.data)[0]
	assert data["name"] == "Dotty"
	assert data["isHeifer"] is True
	assert data["earTag"] == 45
	assert data["dob"] == "2012-10-19"
	assert data["sex"] == "cow"
	assert data["carrier"] is False
	assert data["owner"] == "Molly"

	cow["name"] = "Ditzy"
	cow["earTag"] = 13
	cow["carrier"] = True
	client.post("/herd/add", data=cow, follow_redirects=True)
	rv = client.get('/api/herd?filter=all')
	data = json.loads(rv.data)[1]
	assert data["name"] == "Ditzy"
	assert data["isHeifer"] is True
	assert data["earTag"] == 13
	assert data["dob"] == "2012-10-19"
	assert data["sex"] == "cow"
	assert data["carrier"] is True
	assert data["owner"] == "Molly"


if __name__ == '__main__':
	unittest.main()
