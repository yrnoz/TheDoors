import os
import subprocess

from App.AddWeeklySchedule import add_weekly_schedule_for_employee
from Database.ManageDB import *


def delete_content(pfile):
    pfile.seek(0)
    pfile.truncate()


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
    assert add_weekly_schedule_for_employee("000", schedule_file) is "Employee doesn't exist in the system"

    # checking the permissions of the employee and the permissions of the room.
    assert add_weekly_schedule_for_employee("234", schedule_file) is "You don't have the right access permission"

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
    assert add_weekly_schedule_for_employee("234", schedule_file) is "There is no room matching to the permission - 1"

    delete_content(schedule_file)
    schedule_file.write("'24/07/17 12', 2, 2")

    # checking scheduling room successfuly.
    assert add_weekly_schedule_for_employee("234", schedule_file) is "taub 4"

    p.terminate()


if __name__ == '__main__':
    test_add_weekly_schedule()
