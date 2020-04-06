from CowBook.Models.Cow.CowModel import get_by_id
from tests.helpers import add_cow


def add_note(client, note=None, cow=1):
	if note is None:
		note = {"date": "2020-04-06", "text": "I hope this works"}
	client.post("/herd/{}/addNote".format(cow), data=note, follow_redirects=True)


def test_add_note(client):
	add_cow(client)
	add_note(client)
	cow = get_by_id(1)
	note = cow.notes[0]
	assert "I hope this works" == note.text
	assert "2020-04-06" == note.date.strftime("%Y-%m-%d")
