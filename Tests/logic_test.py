import os
import subprocess
import sys
import pytest

from App.AddWeeklySchedule import add_weekly_schedule_for_employee

sys.path.append(os.getcwd())
from App.Employee import Employee
from App.RoomOrder import RoomOrder
from Database.ManageDB import *


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
    schedule_file.write("'24/07/17 12', 3, 170")
    # checking the validity of the id of the employee.
    assert add_weekly_schedule_for_employee("000", schedule_file) is "Employee doesn't exist in the system"
    # checking the permissions of the employee and the permissions of the room.
    assert add_weekly_schedule_for_employee("789", schedule_file) is "You don't have the right access permission"
