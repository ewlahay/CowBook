import json
from datetime import date, timedelta, datetime

import pytz

from tests.helpers import login, add_cow
from CowBook.Models.Cow.CowModel import get_by_id


def add_event(client, event=None, cow=1):
	add_cow(client)
	if event is None:
		event = {"formType": "Bred", "date": "2020-10-19", "sire": "Big Mac", "notes": "Calving ease bull"}
	client.post("/herd/{}/addEvent".format(cow), data=event, follow_redirects=True)


def test_add_event(client):
	add_event(client)
	start = datetime(2020, 10, 19, tzinfo=pytz.UTC)
	end = start + timedelta(weeks=52)
	url = "api/herd/duedates?start=2020-10-19T00%3A00%3A00-05%3A00&end=2022-02-07T00%3A00%3A00-05%3A00"
	# print(url)
	rv = client.get(url)
	data = json.loads(rv.data)[0]
	assert data["end"] == (start + timedelta(days=287)).strftime("%Y-%m-%d")
	assert data["start"] == (start + timedelta(days=279)).strftime("%Y-%m-%d")
	assert data["title"] == "Dotty due to give birth"


def test_calendar(client):
	add_event(client)
	calender = client.get("api/calendar/dueDates.ics")
	assert b"Dotty due to give birth" in calender.data
