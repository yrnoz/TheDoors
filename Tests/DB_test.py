import os
import subprocess
import sys

sys.path.append(os.getcwd())
from App.Employee import Employee
from App.RoomOrder import RoomOrder
from Database.ManageDB import *


def test_DB():
	p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
	Rooms.drop()
	Employees.drop()
	print os.getcwd()
	read_employees_details("Tests\\employees_test.csv")
	read_rooms_details("Tests\\rooms_test.csv")
	# room = Rooms.find()[0]
	employee = Employee(777, "John", "Engineer", 2)
	add_employee(employee)
	assert check_id_of_employee(777) is True
	# assign_employees_to_room_one_hour('24/07/17 12', room, 10)
	# assign_employees_to_room_to_X_hours('24/07/17 12', 10, 3)
	# assign_employees_to_room_to_X_hours('24/07/17 12', 70, 10)
	item1 = RoomOrder('24/07/17 12', 3, 170)
	item2 = RoomOrder('24/07/17 12', 3, 100)
	RoomOrderItems = [item1, item2]
	add_weekly_schedule(123, RoomOrderItems)

	item21 = RoomOrder('24/07/17 12', 3, 100)
	RoomOrderItems2 = [item21]
	add_weekly_schedule(456, RoomOrderItems2)
	p.terminate()
