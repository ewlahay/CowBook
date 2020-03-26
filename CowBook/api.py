from datetime import datetime, timedelta

from flask import request, send_file
from flask_json import as_json

from CowBook.Models.Cow.CowModel import get_all_dams, get_all_sires, get_all, get_active
from CowBook.Models.Death import get_dead
from CowBook.Models.Sale import get_sold
from CowBook.Models import Treatment
import dateutil.parser
from CowBook.init import app
from ics import Calendar, Event


@app.route('/api/dams')
@as_json
def get_dams():
	return get_all_dams()


@app.route('/api/sires')
@as_json
def get_sires():
	return get_all_sires()


@app.route('/api/herd')
@as_json
def get_herd():
	filter = request.args.get("filter")
	if filter == "active":
		return get_active()
	if filter == "all":
		return get_all()
	if filter == "dead":
		return get_dead()
	if filter == "sold":
		return get_sold(combine=False)

	return get_active()


@app.route('/api/herd/duedates')
@as_json
def get_due_dates():
	start = request.args.get("start")
	end = request.args.get("end")

	if start is not None and end is not None:
		startDate = dateutil.parser.isoparse(start)
		endDate = dateutil.parser.isoparse(end)
		dueDates = Treatment.get_due_dates(startDate, endDate)
		return dueDates
	return "error"


@app.route('/api/calendar/dueDates.ics')
def export_due_dates():
	calender = Calendar(creator="CowBook")
	dueDates = Treatment.get_due_dates(datetime.now().date(), datetime.now().date() + timedelta(
		weeks=104))  # get all due dates for next 2 years
	for dueDate in dueDates:
		event = Event()
		event.name = dueDate["title"]
		event.begin = dueDate["start"]
		event.end = dueDate["end"]
		calender.events.add(event)
	file = open("Data/Calendar.ics", mode="w")
	file.writelines(calender)
	file.close()
	return send_file("Data/Calendar.ics", mimetype="text/calendar")

# TODO Implement calendar feed
