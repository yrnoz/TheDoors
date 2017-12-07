import os
import subprocess

from App.RoomOrder import RoomOrder
from Database.ManageDB import *


# @pytest.fixture(autouse=True)
# def setup_teardown_db():
#     p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
#
#     p.terminate()

def get_ids_from_file(file_name):
    list_ids = []
    with open(file_name) as details:
        for line in details.readlines():
            list_ids.append(line.split(',')[0])
    return list_ids


def test_import_employees_succeeds():
    file_name = "Tests%semployees_test.csv" % os.sep
    employee_ids = get_ids_from_file(file_name)
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Employees.drop()
    import_employees_from_file(file_name)
    assert Employees.count() == 11
    for id in employee_ids:
        assert Employees.find_one({"id": id}) is not None
    Employees.drop()
    p.terminate()


def test_import_rooms_succeeds():
    file_name = "Tests%srooms_test.csv" % os.sep
    room_ids = get_ids_from_file(file_name)
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    import_room_details_from_file(file_name)
    assert Rooms.count() == 11
    for id in room_ids:
        assert Rooms.find_one({"id": id}) is not None
    Rooms.drop()
    p.terminate()


# @pytest.mark.skip(reason="should be separated into different tests")
def test_db():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    # import_employees_from_file("Resources%semployees_test.csv" % (os.sep))
    # import_room_details_from_file("Resources%srooms_test.csv" % (os.sep))
    import_employees_from_file("Tests%semployees_test.csv" % os.sep)
    import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
    # room = Rooms.find()[0]
    # employee = Employee(777, "John", "Engineer", 2)
    # add_employee(employee)
    assert check_id_of_employee("123") is True
    # employee = find_employee(777)
    # print (employee)
    # assign_employees_to_room_one_hour('24/07/17 12', room, 10)
    # assign_employees_to_room_to_X_hours('24/07/17 12', 10, 3)
    # assign_employees_to_room_to_X_hours('24/07/17 12', 70, 10)
    item1 = RoomOrder('24/07/17 12', 3, 170)
    item2 = RoomOrder('24/07/17 12', 3, 100)
    RoomOrderItems = [item1, item2]
    add_weekly_schedule("123", RoomOrderItems)

    item21 = RoomOrder('24/07/17 12', 3, 100)
    RoomOrderItems2 = [item21]
    add_weekly_schedule("456", RoomOrderItems2)
    p.terminate()


if __name__ == "__main__":
    test_db()
