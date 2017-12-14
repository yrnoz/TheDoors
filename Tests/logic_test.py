import os
import subprocess
import pytest

from App.AddWeeklySchedule import add_weekly_schedule_for_employee
from App.Room import Room
from App.RoomReccomendations import initialize_employee_from_dict, initialize_room_from_dict, \
    reccomendationToEmployeeByRoom, emptyRooms
from Database.ManageDB import *
from App.Employee import *

import random, string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture(autouse=True)
def p():
    mongo = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    yield mongo
    mongo.terminate()


def delete_content(pfile):
    pfile.seek(0)
    pfile.truncate()


def ltest_add_weekly_schedule_succeed():
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2\n")
    employees.write("498,Elyasaf,Engineer,2\n")
    # entering a room with permission 1.
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")

    # import_employees_from_file("employees.csv")
    # import_room_details_from_file(rooms.name)
    # schedule_file = open("schedule_file.csv", "w+")

    schedule_file.write("24/07/17 12, 2, 35 \n")  # need to succeed
    schedule_file.seek(0)

    assert add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep) \
           == "Dear Koby! The room that was chosen for you is: taub 4. For the time: 24/07/17 12. " \
              "Dear Koby! The room that was chosen for you is: taub 4. For the time: 24/07/17 13. "


def test_add_weekly_schedule_some_hours_fails():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    # employees = open("employees.csv", "w+")
    # rooms = open("rooms.csv", "w+")

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    # entering two employees with permissions 2.
    employees.write("234,Koby,Engineer,2\n")
    employees.write("498,Elyasaf,Engineer,2\n")
    # entering a room with permission 1.
    rooms.write("taub 4,40,1,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")

    # import_employees_from_file("employees.csv")
    # import_room_details_from_file(rooms.name)
    # schedule_file = open("schedule_file.csv", "w+")

    schedule_file.write("24/07/17 12, 2, 170 \n")
    schedule_file.seek(0)

    assert add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep) == \
           "Dear Koby! There is no free room the 24/07/17 12 ! Sorry." \
           "Dear Koby! There is no free room the 24/07/17 13 ! Sorry."


# @pytest.mark.skip(reason="not working as of now, remove this when you're working on it")
def test_add_weekly_schedule():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    # employees = open("employees.csv", "w+")
    # rooms = open("rooms.csv", "w+")
    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    # entering two employees with permissions 2.
    employees.write("234,Koby,Engineer,2\n")
    employees.write("498,Elyasaf,Engineer,2\n")
    # entering a room with permission 1.
    rooms.write("taub 4,40,1,1\n")
    employees.seek(0)
    rooms.seek(0)
    # import_employees_from_file("employees.csv")
    # import_room_details_from_file(rooms.name)
    # schedule_file = open("schedule_file.csv", "w+")
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")

    schedule_file.write("24/07/17 12, 1, 17 \n")
    schedule_file.seek(0)
    # checking the validity of the id of the employee.
    assert add_weekly_schedule_for_employee("000",
                                            "Tests%sschedule_file.csv" % os.sep) == "Employee doesn't exist in the system"

    # checking the permissions of the employee and the permissions of the room.
    assert add_weekly_schedule_for_employee("234",
                                            "Tests%sschedule_file.csv" % os.sep) == "Dear Koby! There is no free room the 24/07/17 12 ! Sorry."
    p.terminate()


#########################################################################################################


def print_friends():
    for employee in Employees.find():
        print "friends of {} id-{}:".format(employee["name"], employee["id"]) + str(employee["friends"])


@pytest.mark.skip(reason="not relevant for now")
def test_recommend_by_friends():
    # initial friends for every employee
    for employee in Employees.find():
        employee_obj = initialize_employee_from_dict(employee)
        for friend in Employees.find():
            if employee["id"] != friend["id"]:
                employee_obj.add_friends([int(friend["id"])])
        # print employee_obj.friends
    # initial schedule for every room
    for room in Rooms.find():
        room_obj = initialize_room_from_dict(room)
        room_obj.add_schedule()


@pytest.mark.skip(reason="not relevant for now")
def test_reccomendationToEmployeeByRoom():
    pass


def test_emptyRooms():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")
    employees.write("234,Koby,Engineer,2\n")
    employees.write("498,Elyasaf,Engineer,2\n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 2, 35 \n")
    schedule_file.seek(0)
    add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
    koby = Employee(234, 'Koby', 'Engineer', 2)
    x=emptyRooms(koby, "24/07/17 12")
    assert emptyRooms(koby, "24/07/17 12") == {"taub 4" : 5}

@pytest.mark.skip(reason="not relevant for now")
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


def test_roomRecommendation_two_rooms():
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("Tests%semployees_test.csv" % os.sep)
    # import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
    koby = Employee(234, 'Koby', 'Engineer', 2)
    with open("Tests%srooms_test2.csv" % os.sep, 'w') as test:
        test.write("taub 1,40,3,1\n")
    import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
    recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
    assert len(recommended) == 1
    assert recommended[0] == "taub 1"
    recommended = reccomendationToEmployeeByRoom(koby)
    assert len(recommended) == 1
    assert recommended[0] == "taub 1"
    Rooms.drop()
    with open("Tests%srooms_test2.csv" % os.sep, 'a') as test:
        test.write("taub 2,30,3,1")
    import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
    recommended = reccomendationToEmployeeByRoom(koby, "03/02/19 11")
    assert len(recommended) == 2
    Rooms.drop()
    Employees.drop()


def test_roomRecommendation_no_permission():
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("Tests%semployees_test.csv" % os.sep)
    # import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
    koby = Employee(234, 'Koby', 'Engineer', 2)
    with open("Tests%srooms_test2.csv" % os.sep, 'w') as test:
        test.write("taub 1,40,1,1")
    import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
    recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
    assert len(recommended) == 0
    Rooms.drop()
    with open("Tests%srooms_test2.csv" % os.sep, 'w') as test:
        test.write("taub 2,30,3,1")
    import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
    recommended = reccomendationToEmployeeByRoom(koby, "03/02/19 11")
    assert len(recommended) == 1
    Rooms.drop()
    Employees.drop()


def test_roomRecommendation_no_place_in_rooms():
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("Tests%semployees_test.csv" % os.sep)
    # import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
    koby = Employee(234, 'Koby', 'Engineer', 2)
    room1 = Room("taub 1", 0, 0, 3)
    room2 = Room("taub 2", 0, 0, 3)
    room3 = Room("taub 3", 0, 30, 4)
    add_room(room1)
    recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
    assert len(recommended) == 0
    add_room(room2)
    recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
    assert len(recommended) == 0
    add_room(room3)
    recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
    assert len(recommended) == 1
    assert recommended == [room3.id]
    Rooms.drop()
    Employees.drop()


def test_roomRecommendation_many_rooms():
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("Tests%semployees_test.csv" % os.sep)
    import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
    koby = Employee(234, 'Koby', 'Engineer', 1)
    recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
    assert len(recommended) == 11
    Rooms.drop()
    for i in range(500):
        room = Room(randomword(7), 0, 30, 2)
        add_room(room)
    recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
    assert len(recommended) == 500
    Rooms.drop()
    Employees.drop()


def test_recommend_by_friends():
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("Tests%semployees_test.csv" % os.sep)
    import_room_details_from_file("Tests%srooms_test.csv" % os.sep)


if __name__ == '__main__':
    test_add_weekly_schedule()
    test_add_weekly_schedule_succeed()
    test_add_weekly_schedule_some_hours_fails()
    test_roomRecommendation_two_rooms()
    test_roomRecommendation_no_permission()
    test_roomRecommendation_no_place_in_rooms()
    test_roomRecommendation_many_rooms()
