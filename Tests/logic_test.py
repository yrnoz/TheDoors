import os
import subprocess
import pytest

from App.AddWeeklySchedule import add_weekly_schedule_for_employee
from App.AddWeeklySchedule import delete_weekly_schedule
from App.Room import Room
from App.RoomReccomendations import initialize_employee_from_dict, \
    emptyRooms, recommend_by_friends
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



    # entering a room with permission 2, need to succeed.


def test_weekly_schedule1():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2, 1234\n")
    employees.write("498,Elyasaf,Engineer,2, 5678\n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    assert (add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
            == "Dear Koby! The room that was chosen for you is: taub 4. For the time: 24/07/17 12. ")
    p.terminate()


# entering a room with permission 2, but Koby is the director and has permission 3. need to fail.
def test_weekly_schedule2():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,3, 1234\n")
    employees.write("498,Elyasaf,Engineer,2 ,5678\n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)

    assert add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep) \
           == "Dear Koby! There is no free room the 24/07/17 12 ! Sorry."
    p.terminate()


# entering a room with permission 2, but one of the employees has permission 3. Need to fail (Maybe in the feutare we
# will change it. Now, we are going on the basic.
def test_weekly_schedule3():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2, 1234\n")
    employees.write("498,Elyasaf,Engineer,3, 5678\n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    assert (add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
            == "Dear Koby! There is no free room the 24/07/17 12 ! Sorry.")
    p.terminate()


# There is only one room with only not enoght place. need to fail
def test_weekly_schedule4():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2, 1234\n")
    employees.write("498,Elyasaf,Engineer,2, 5678\n")
    rooms.write("taub 4,1,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    assert (add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
            == "Dear Koby! There is no free room the 24/07/17 12 ! Sorry.")
    p.terminate()


# check some hours
def test_weekly_schedule5():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2, 1234\n")
    employees.write("498,Elyasaf,Engineer,2, 5678\n")
    rooms.write("taub 4,1,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 2, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    assert (add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
            == "Dear Koby! There is no free room the 24/07/17 12 ! Sorry." \
               "Dear Koby! There is no free room the 24/07/17 13 ! Sorry.")
    p.terminate()


# Chcek that the employee exist in the system. I'm not checking that the rest of the employees exist. I assume that
# everything is alright. Maybe we will check it to the next sprint.
def test_weekly_schedule6():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2, 1234\n")
    employees.write("498,Elyasaf,Engineer,2, 5678\n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    assert (add_weekly_schedule_for_employee("000", "Tests%sschedule_file.csv" % os.sep)
            == "Employee doesn't exist in the system")
    p.terminate()


#What happens if we do the schedular twice. NOT-PASSSING. Need to understand how to write this test properly
def test_weekly_schedule7():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2, 1234\n")
    employees.write("498,Elyasaf,Engineer,2, 5678\n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    assert (add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
            == "Dear Koby! The room that was chosen for you is: taub 4. For the time: 24/07/17 12. ")

    assert (add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
            == "Dear Koby! You have already ordered room for: 24/07/17 12 ! Sorry.")
    p.terminate()

@pytest.mark.skip
def test_weekly_schedule_delete():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()

    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")

    employees.write("234,Koby,Engineer,2, 1234\n")
    employees.write("498,Elyasaf,Engineer,2, 5678\n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    assert (add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
            == "Dear Koby! The room that was chosen for you is: taub 4. For the time: 24/07/17 12. ")

    schedule_file = open("Tests%sschedule_file_delete.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 1, 2, 498 234 \n")  # need to succeed
    schedule_file.seek(0)
    delete_weekly_schedule("234", "Tests%sschedule_file_delete.csv" % os.sep)
    p.terminate()


#########################################################################################################


def print_friends():
    for employee in Employees.find():
        print "friends of {} id-{}:".format(employee["name"], employee["id"]) + str(employee["friends"])


@pytest.mark.skip(reason="not relevant for now")
def test_reccomendationToEmployeeByRoom():
    pass


@pytest.mark.skip(reason="fix it")
def test_emptyRooms():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    employees = open("Tests%semployees.csv" % os.sep, "w+")
    rooms = open("Tests%srooms.csv" % os.sep, "w+")
    employees.write("234,Koby,Engineer,2,pass2\n")
    employees.write("498,Elyasaf,Engineer,2,pass1 \n")
    rooms.write("taub 4,40,2,1\n")
    employees.seek(0)
    rooms.seek(0)
    import_employees_from_file("Tests%semployees.csv" % os.sep)
    import_room_details_from_file(rooms.name)
    schedule_file = open("Tests%sschedule_file.csv" % os.sep, "w+")
    schedule_file.write("24/07/17 12, 2, 35 \n")
    schedule_file.seek(0)
    add_weekly_schedule_for_employee("234", "Tests%sschedule_file.csv" % os.sep)
    koby = Employee(234, 'Koby', 'Engineer', 2, "password")
    x = emptyRooms(koby, "24/07/17 12")
    assert emptyRooms(koby, "24/07/17 12") == {"taub 4": 5}


@pytest.mark.skip(reason="not relevant for now")
def test_room_with_my_friends():
    pass


def print_employees_db():
    for employee in Employees.find():
        print "id: " + str(employee["id"]) + " name: " + employee["name"] + " role: " + \
              employee["role"] + " permossion: " + str(employee["permission"]) + "password: " + str(
            employee["password"]) + "\n"


def print_rooms_db():
    for room in Rooms.find():
        print "id: " + room["id"] + " capacity: " + str(room["capacity"]) + " permossion: " + str(
            room["permission"]) + " floor: " + str(room["floor"]) + "\n"


# def test_roomRecommendation_two_rooms():
#     Rooms.drop()
#     Employees.drop()
#     import_employees_from_file("Tests%semployees_test.csv" % os.sep)
#     # import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
#     koby = Employee(234, 'Koby', 'Engineer', 2)
#     with open("Tests%srooms_test2.csv" % os.sep, 'w') as test:
#         test.write("taub 1,40,3,1\n")
#     import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
#     #recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
#     assert len(recommended) == 1
#     assert recommended[0] == "taub 1"
#     recommended = reccomendationToEmployeeByRoom(koby)
#     assert len(recommended) == 1
#     assert recommended[0] == "taub 1"
#     Rooms.drop()
#     with open("Tests%srooms_test2.csv" % os.sep, 'a') as test:
#         test.write("taub 2,30,3,1")
#     import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
#     recommended = reccomendationToEmployeeByRoom(koby, "03/02/19 11")
#     assert len(recommended) == 2
#     Rooms.drop()
#     Employees.drop()


# def test_roomRecommendation_no_permission():
#     Rooms.drop()
#     Employees.drop()
#     import_employees_from_file("Tests%semployees_test.csv" % os.sep)
#     # import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
#     koby = Employee(234, 'Koby', 'Engineer', 2)
#     with open("Tests%srooms_test2.csv" % os.sep, 'w') as test:
#         test.write("taub 1,40,1,1")
#     import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
#     recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
#     assert len(recommended) == 0
#     Rooms.drop()
#     with open("Tests%srooms_test2.csv" % os.sep, 'w') as test:
#         test.write("taub 2,30,3,1")
#     import_room_details_from_file("Tests%srooms_test2.csv" % os.sep)
#     recommended = reccomendationToEmployeeByRoom(koby, "03/02/19 11")
#     assert len(recommended) == 1
#     Rooms.drop()
#     Employees.drop()


# def test_roomRecommendation_no_place_in_rooms():
#     Rooms.drop()
#     Employees.drop()
#     import_employees_from_file("Tests%semployees_test.csv" % os.sep)
#     # import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
#     koby = Employee(234, 'Koby', 'Engineer', 2)
#     room1 = Room("taub 1", 0, 0, 3)
#     room2 = Room("taub 2", 0, 0, 3)
#     room3 = Room("taub 3", 0, 30, 4)
#     add_room(room1)
#     recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
#     assert len(recommended) == 0
#     add_room(room2)
#     recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
#     assert len(recommended) == 0
#     add_room(room3)
#     recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
#     assert len(recommended) == 1
#     assert recommended == [room3.id]
#     Rooms.drop()
#     Employees.drop()


# def test_roomRecommendation_many_rooms():
#     Rooms.drop()
#     Employees.drop()
#     import_employees_from_file("Tests%semployees_test.csv" % os.sep)
#     import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
#     koby = Employee(234, 'Koby', 'Engineer', 1)
#     recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
#     assert len(recommended) == 11
#     Rooms.drop()
#     for i in range(500):
#         room = Room(randomword(7), 0, 30, 2)
#         add_room(room)
#     recommended = reccomendationToEmployeeByRoom(koby, "24/12/17 14")
#     assert len(recommended) == 500
#     Rooms.drop()
#     Employees.drop()


def create_friend_relationship():
    for employee in Employee.find():
        employee = initialize_employee_from_dict(employee)
        employee.add_schedules({datetime.now().strftime("%d/%m/%y %H"), (0, "taub 4")})
        for friend in Employee.find({'permission': employee.access_permission}):
            friend = initialize_employee_from_dict(employee)
            if employee.id != friend.id:
                employee.add_friends(list(friend.id))


@pytest.mark.skip(reason="not relevant for now")
def test_recommend_by_friends():
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("Tests%sfriends_test.csv" % os.sep)
    import_room_details_from_file("Tests%srooms_test.csv" % os.sep)
    create_friend_relationship()
    for employee in Employee.find():
        employee = initialize_employee_from_dict(employee)
        res = recommend_by_friends(employee)
        assert res == ["taub 4"]


if __name__ == '__main__':
    test_weekly_schedule7()
