from datetime import datetime
from pymongo import MongoClient

client = MongoClient()  # making the connection with the DB
db = client['test-database']  # create a new DB
Rooms = db["Rooms"]  # create new table that called Rooms
Employees = db["Employees"]  # create new table that called Employees


# The function gets a CSV file with details about employees in the
# factory and adds them to the DB
# input: CSV file
# output: side effect  - the details added to the DB
def read_employees_details(inputfile):
    global Employees
    with open(inputfile) as details:  # open the file
        for line in details.readlines():
            id, name, role, permission = line[:-1].split(",")  # get the parameters we need from the line
            employee = {"id": int(id), "name": name, "role": role, "permission": int(permission), "friends": [],
                        "schedule": {}}
            Employees.insert(employee)  # add employee's details to the DB


# The function gets a CSV file with details about rooms in the
# factory and adds them to the DB
# input: CSV file
# output: side effect  - the details added to the DB
def read_rooms_details(inputfile):
    global Rooms
    with open(inputfile) as details:  # open the file
        for line in details.readlines():
            id, capacity, permission, floor = line[:-1].split(",")  # get the parameters we need from the line
            room = {"id": id, "capacity": int(capacity), "permission": int(permission), "floor": int(floor),
                    "schedule": {}}
            Rooms.insert(room)  # add employee's details to the DB


def get_access_permission_of_employee_by_id(id):
    global Employees
    employee = Employees.find_one({"id": int(id)})
    return int(employee["permission"])


# this function gets date time in format "D/M/Y Hour", the room from the DB to assign employees
# and number of employees to assign.
# output: False - in case the employees can not be assigned to the room
# True - in case the employees were assigned to the room
def assign_employees_to_room(date_time, room, num_employees):
    global Rooms
    capacity = room["capacity"]
    schedule = room["schedule"]
    try:
        datetime.strptime(date_time, "%d/%m/%y %H")  # check the date_time format is correct
    except ValueError:
        return False
    if not (date_time in schedule):
        if num_employees > capacity:
            return False
        schedule[date_time] = (num_employees, None)
    else:
        if schedule[date_time][0] + num_employees > capacity:
            return False
        schedule[date_time] = (schedule[date_time][0] + num_employees, None)
    Rooms.replace_one({'_id': room['_id']}, room)
    return True
