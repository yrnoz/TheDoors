import os
import subprocess

from App.Employee import Employee
from App.RoomOrder import RoomOrder
from Database.AddToDB import *

if __name__ == "__main__":
	p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
	Rooms.drop()
	Employees.drop()
	read_employees_details("employees_test.csv")
	read_rooms_details("rooms_test.csv")
	room = Rooms.find()[0]
	employee = Employee(777, "John", "Engineer", 2)
	add_employee(employee)
	assert check_id_of_employee(777) is True
	print("Finished Testing")
	# assign_employees_to_room_one_hour('24/07/17 12', room, 10)
	# assign_employees_to_room_to_X_hours('24/07/17 12', 10, 3)
	# assign_employees_to_room_to_X_hours('24/07/17 12', 70, 10)

	item1 = RoomOrder('24/07/17 12', 3, 170)
	item2 = RoomOrder('24/07/17 12', 3, 100)
	RoomOrderItems = []
	RoomOrderItems.append(item1)
	RoomOrderItems.append(item2)
	add_weekly_schedule(123, RoomOrderItems)

	item21 = RoomOrder('24/07/17 12', 3, 100)
	RoomOrderItems2 = []
	RoomOrderItems2.append(item21)
	add_weekly_schedule(456, RoomOrderItems2)
	p.terminate()
