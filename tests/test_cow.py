from datetime import datetime
from CowBook.Models.Cow import CowModel


def test_cow():
	cow = CowModel.Cow("Daisy", "45", datetime(2019, 1, 1), "cow", False, "Luke", "Yellow", None)
	assert cow.name == "Daisy"
	assert cow.earTag == "45"
	assert cow.dob.day == 1
	assert cow.sex == "cow"
	assert cow.owner == "Luke"
	assert cow.markings == "Yellow"

	cow2 = CowModel.Cow(None, "45", datetime(2019, 1, 1), "cow", False, "Luke", "Yellow", None)
	assert cow2.name == "45"


if __name__ == '__main__':
	test_cow()
