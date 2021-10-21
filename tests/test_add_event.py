import json
from datetime import date, timedelta, datetime

import pytz

from tests.helpers import login, add_cow
from CowBook.Models.Cow.CowModel import get_by_id


def add_event(client, event=None, cow=1, bredDate: datetime = datetime.now()):
	add_cow(client)
	if event is None:
		dateStr = bredDate.strftime("%Y-%m-%d")
		print(dateStr)
		event = {"formType": "Bred", "date": dateStr, "sire": "Big Mac", "notes": "Calving ease bull"}
	client.post("/herd/{}/addEvent".format(cow), data=event, follow_redirects=True)


def test_add_event(client):
	start = datetime(2020, 10, 19, tzinfo=pytz.UTC)
	add_event(client, bredDate=start)
	end = start + timedelta(weeks=52)
	url = "api/herd/duedates?start=2019-10-19T00%3A00%3A00-05%3A00&end=2022-02-07T00%3A00%3A00-05%3A00"
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
