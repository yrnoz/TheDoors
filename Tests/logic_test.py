import os
import subprocess

import pytest

from App.AddWeeklySchedule import add_weekly_schedule_for_employee
from App.RoomReccomendations import initialize_employee_from_dict, initialize_room_from_dict
from Database.ManageDB import *


def delete_content(pfile):
    pfile.seek(0)
    pfile.truncate()


@pytest.mark.skip(reason="not working as of now, remove this when you're working on it")
def test_add_weekly_schedule():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    employees = open("employees.csv", "w+")
    rooms = open("rooms.csv", "w+")
    # entering two employees with permissions 2.
    employees.write("234,Koby,Engineer,2")
    employees.write("498,Elyasaf,Engineer,2")
    # entering a room with permission 1.
    rooms.write("taub 4,40,1,1")
    import_employees_from_file(employees.name)
    import_room_details_from_file(rooms.name)
    schedule_file = open("schedule_file.csv", "w+")
    schedule_file.write("'24/07/17 12', 1, 170")

    # checking the validity of the id of the employee.
    assert add_weekly_schedule_for_employee("000", schedule_file) == "Employee doesn't exist in the system"

    # checking the permissions of the employee and the permissions of the room.
    assert add_weekly_schedule_for_employee("234", schedule_file) == "You don't have the right access permission"

    Rooms.drop()
    Employees.drop()
    delete_content(employees)
    delete_content(rooms)
    # entering two employees with permissions 2.
    employees.write("234,Koby,Engineer,1")
    employees.write("498,Elyasaf,Engineer,1")
    # entering a room with permission 1.
    rooms.write("taub 4,40,1,2")
    import_employees_from_file(employees.name)
    import_room_details_from_file(rooms.name)

    # checking the permissions of the existence of rooms with the demanded permission.
    assert add_weekly_schedule_for_employee("234", schedule_file) == "There is no room matching to the permission - 1"

    delete_content(schedule_file)
    schedule_file.write("'24/07/17 12', 2, 2")

    # checking scheduling room successfuly.
    assert add_weekly_schedule_for_employee("234", schedule_file) == "taub 4"

    p.terminate()

#########################################################################################################


def print_friends():
    for employee in Employees.find():
        print "friends of {} id-{}:".format(employee["name"], employee["id"]) + str(employee["friends"])


def test_recommend_by_friends():
    # initial friends for every employee
    for employee in Employees.find():
        employee_obj = initialize_employee_from_dict(employee)
        for friend in Employees.find():
            if employee["id"] != friend["id"]:
                employee_obj.add_friends([int(friend["id"])])
        print employee_obj.friends
    # initial schedule for every room
    for room in Rooms.find():
        room_obj = initialize_room_from_dict(room)
        room_obj.add_schedule()


def test_reccomendationToEmployeeByRoom():
    pass


def test_emptyRooms():
    pass


def test_room_with_my_friends():
    pass


def print_employees_db():
    for employee in Employees.find():
        print "id: " + str(employee["id"]) + " name: " + employee["name"] + " role: " + \
              employee["role"] + " permossion: " + str(employee["permission"]) + "\n"


def print_rooms_db():
    for room in Rooms.find():
        print "id: " + room["id"] + " capacity: " + str(room["capacity"]) + " permossion: " + str(
            room["permission"]) + " floor: " + str(room["floor"]) + "\n"


def test_roomRecommendation():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("employees_test.csv")
    import_room_details_from_file("rooms_test.csv")
    print_rooms_db()
    print_employees_db()
    test_recommend_by_friends()
    test_reccomendationToEmployeeByRoom()
    test_emptyRooms()
    test_room_with_my_friends()


if __name__ == '__main__':
   test_add_weekly_schedule()
#test_roomRecommendation()
