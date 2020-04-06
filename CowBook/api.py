import os
from datetime import datetime, timedelta

from flask import request, send_file, Blueprint
from flask_json import as_json
from flask_security import login_required

from CowBook.Models.Cow.CowModel import get_all_dams, get_all_sires, get_all, get_active, get_by_id
from CowBook.Models.Death import get_dead
from CowBook.Models.Sale import get_sold
from CowBook.Models import Treatment
import dateutil.parser
from ics import Calendar, Event

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/dams')
@as_json
def get_dams():
	return get_all_dams()


@api.route('/sires')
@as_json
def get_sires():
	return get_all_sires()


@api.route('/herd')
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


@api.route("/herd/<cowId>")
@as_json
def get_cow(cowId):
	return get_by_id(cowId)


@api.route('/herd/duedates')
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


@api.route('/calendar/dueDates.ics')
@login_required
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
	file = open(os.path.dirname(__file__) + "/static/calendar.ics", mode="w")
	file.writelines(calender)
	file.close()
	return send_file(os.path.dirname(__file__) + "/static/calendar.ics", mimetype="text/calendar")

# TODO Implement calendar feed
