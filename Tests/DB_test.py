import os
import subprocess

import pytest

from App.Employee import Employee
from App.Room import Room
from App.RoomOrder import RoomOrder
from Database.ManageDB import *


@pytest.fixture(autouse=True)
def p():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    yield p
    p.terminate()


def get_ids_from_file(file_name):
    list_ids = []
    with open(file_name) as details:
        for line in filter(lambda x: x.strip(), details.readlines()):
            list_ids.append(line.split(',')[0])
    return list_ids


def test_import_employees_succeeds():
    file_name = "Tests%semployees_test.csv" % os.sep
    employee_ids = get_ids_from_file(file_name)
    Employees.drop()
    Rooms.drop()
    import_employees_from_file(file_name)
    assert Employees.count() == 11
    for id in employee_ids:
        assert Employees.find_one({"id": id}) is not None
    Employees.drop()


def test_import_rooms_succeeds():
    file_name = "Tests%srooms_test.csv" % os.sep
    room_ids = get_ids_from_file(file_name)
    Rooms.drop()
    import_room_details_from_file(file_name)
    assert Rooms.count() == 11
    for id in room_ids:
        assert Rooms.find_one({"id": id}) is not None
    Rooms.drop()


def test_export_employees_without_change_shouldnt_change():
    file_name = "Tests%semployees_test.csv" % os.sep
    Employees.drop()
    Rooms.drop()
    import_employees_from_file(file_name)
    output_file = "Tests%soutput_test.csv" % os.sep
    export_employees_to_file(output_file)
    with open(output_file, 'r') as output, open(file_name, 'r') as _input:
        file_in = filter(lambda x: x.strip(), _input.readlines())
        file_out = output.readlines()
    for line, line2 in zip(file_out, file_in):
        assert line2 in file_out
        assert line in file_in
    Employees.drop()
    os.remove(output_file)


def test_export_employees_with_removal_should_decrease():
    file_name = "Tests%semployees_test.csv" % os.sep
    # p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Employees.drop()
    import_employees_from_file(file_name)
    remove_employee("965")
    output_file = "Tests%soutput_test.csv" % os.sep
    assert check_id_of_employee("965") is False
    export_employees_to_file(output_file)
    with open(output_file, 'r') as output, open(file_name, 'r') as _input:
        file_in = filter(lambda x: x.strip(), _input.readlines())
        file_out = output.readlines()
    for line in file_out:
        assert line in file_in
    # p.terminate()
    Employees.drop()
    os.remove(output_file)


def test_export_employees_with_addition_should_increase():
    file_name = "Tests%semployees_test.csv" % os.sep
    # p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Employees.drop()
    import_employees_from_file(file_name)
    add_employee(Employee("900", "Johnny", "Engineer", 1, "password"))
    output_file = "Tests%soutput_test.csv" % os.sep
    assert check_id_of_employee("900") is True
    export_employees_to_file(output_file)
    with open(output_file, 'r') as output, open(file_name, 'r') as _input:
        file_in = filter(lambda x: x.strip(), _input.readlines())
        file_out = output.readlines()
    for line in file_in:
        assert line in file_out
    # p.terminate()
    Employees.drop()
    os.remove(output_file)


def test_export_rooms_without_change_shouldnt_change():
    file_name = "Tests%srooms_test.csv" % os.sep
    Rooms.drop()
    import_room_details_from_file(file_name)
    output_file = "Tests%soutput_test.csv" % os.sep
    export_rooms_to_file(output_file)
    with open(output_file, 'r') as output, open(file_name, 'r') as _input:
        file_in = filter(lambda x: x.strip(), _input.readlines())
        file_out = output.readlines()
    for line, line2 in zip(file_out, file_in):
        assert line2 in file_out
        assert line in file_in
    Rooms.drop()
    os.remove(output_file)


def test_export_rooms_with_removal_should_decrease():
    file_name = "Tests%srooms_test.csv" % os.sep
    Rooms.drop()
    import_room_details_from_file(file_name)
    output_file = "Tests%soutput_test.csv" % os.sep
    remove_room("taub 7")
    export_rooms_to_file(output_file)
    with open(output_file, 'r') as output, open(file_name, 'r') as _input:
        file_in = filter(lambda x: x.strip(), _input.readlines())
        file_out = output.readlines()
    for line in file_out:
        assert line in file_in
    Rooms.drop()
    os.remove(output_file)


def test_export_rooms_with_addition_should_increase():
    file_name = "Tests%srooms_test.csv" % os.sep
    Rooms.drop()
    import_room_details_from_file(file_name)
    output_file = "Tests%soutput_test.csv" % os.sep
    add_room(Room(id="taub 10", floor=5, max_capacity=100, access_permission=3))
    export_rooms_to_file(output_file)
    with open(output_file, 'r') as output, open(file_name, 'r') as _input:
        file_in = filter(lambda x: x.strip(), _input.readlines())
        file_out = output.readlines()
    for line in file_in:
        assert line in file_out
    Rooms.drop()
    os.remove(output_file)


def test_add_friend():
    file_name = "Tests%semployees_test.csv" % os.sep
    # p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Employees.drop()
    import_employees_from_file(file_name)
    add_a_friend_for_employee("498", "123")
    assert "123" in find_employee("498")["friends"]
    assert "498" in find_employee("123")["friends"]
    output_file = "Tests%soutput_test.csv" % os.sep
    export_employees_to_file(output_file)
    Employees.drop()
    os.remove(output_file)


def test_remove_friend():
    file_name = "Tests%semployees_test.csv" % os.sep
    # p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Employees.drop()
    import_employees_from_file(file_name)
    add_a_friend_for_employee("498", "123")
    assert "123" in find_employee("498")["friends"]
    assert "498" in find_employee("123")["friends"]
    delete_a_friend_from_employee("123", "498")
    assert "123" not in find_employee("498")["friends"]
    assert "498" not in find_employee("123")["friends"]
    output_file = "Tests%soutput_test.csv" % os.sep
    export_employees_to_file(output_file)
    Employees.drop()
    os.remove(output_file)


def test_check_password_of_employee():
    file_name = "Tests%semployees_test.csv" % os.sep
    # p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Employees.drop()
    import_employees_from_file(file_name)
    assert check_password_of_employee("123", "1234") is True
    assert check_password_of_employee("0123", "1235") is True
    assert check_password_of_employee("134", "1239") is True
    assert check_password_of_employee("742", "1221") is True
    assert check_password_of_employee("965", "1222") is True
    assert check_password_of_employee("840", "1323") is True
    Employees.drop()


def test_get_password_of_employee_by_id():
    file_name = "Tests%semployees_test.csv" % os.sep
    # p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Employees.drop()
    import_employees_from_file(file_name)
    assert get_password_of_employee_by_id("123") == "1234"
    assert get_password_of_employee_by_id("0123") == "1235"
    assert get_password_of_employee_by_id("134") == "1239"
    assert get_password_of_employee_by_id("742")== "1221"
    assert get_password_of_employee_by_id("965") == "1222"
    assert get_password_of_employee_by_id("840") == "1323"
    Employees.drop()


@pytest.mark.skip(reason=0)
def test_db():
    # p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
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
    # print employee
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
    Rooms.drop()
    Employees.drop()
    # p.terminate()
