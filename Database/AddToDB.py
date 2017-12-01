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
def read_employees_details(input_file):
    global Employees
    with open(input_file) as details:  # open the file
        for line in details.readlines():
            id, name, role, permission = line[:-1].split(",")  # get the parameters we need from the line
            employee = {"id": int(id), "name": name, "role": role, "permission": int(permission), "friends": [],
                        "schedule": {}}
            Employees.insert(employee)  # add employee's details to the DB


def add_employee(employee):
    """
    Adds a given employee into the db.
    Useful for on-the-fly addition of employees into the DB when the system is already up-and-running (i.e. after
    the DB initialization phase)
    :param employee: the employee object to be added into the DB.
    """
    global Employees
    employee_json = {"id": int(employee.id), "name": employee.name, "role": employee.role,
                     "permission": int(employee.access_permission), "friends": employee.friends,
                     "schedule": {}}
    Employees.insert(employee_json)


def add_room(room):
    """
    Adds a new room into the db.
    Useful for on-the-fly addition of rooms into the DB when the system is already up-and-running (i.e. after
    the DB initialization phase)
    :param room: room to be added into the DB
    """
    global Rooms
    room_json = {"id": room.id, "capacity": int(room.maxCapacity), "permission": int(room.access_permission),
                 "floor": int(room.floor),
                 "schedule": {}}
    Rooms.insert(room_json)


# The function gets a CSV file with details about rooms in the
# factory and adds them to the DB
# input: CSV file
# output: side effect  - the details added to the DB
def read_rooms_details(input_file):
    global Rooms
    with open(input_file) as details:  # open the file
        for line in details.readlines():
            id, capacity, permission, floor = line[:-1].split(",")  # get the parameters we need from the line
            room = {"id": id, "capacity": int(capacity), "permission": int(permission), "floor": int(floor),
                    "schedule": {}}
            Rooms.insert(room)  # add employee's details to the DB


def get_access_permission_of_employee_by_id(id):
    global Employees
    employee = Employees.find_one({"id": int(id)})
    return int(employee["permission"])


def check_id_of_employee(id):
    global Employees
    employee = Employees.find_one({"id": int(id)})
    if employee is None:
        return False
    return True

def find_worker(id):
    if check_id_of_employee(id):
        return Employees.find_one({"id": int(id)})



def assign_employees_to_room_one_hour(date_time, room, num_employees):
    """
    this function gets date time in format "D/M/Y Hour", the room from the DB to assign employees,
    and number of employees to assign, if possible - they would be assigned to the room.
    :param date_time: date time in format "D/M/Y Hour"
    :param room: the room from the DB to assign employees
    :param num_employees: number of employees to assign
    :return:  False - in case the employees can not be assigned to the room
              True - in case the employees were assigned to the room
    """
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


# iterate on the range of hours. prefer to look at the previous room
def assign_employees_to_room_to_X_hours(date_time, num_employees, num_hours):
    """

    :param date_time:
    :param num_employees:
    :param num_hours:
    """
    previous_room = Rooms.find()[0]
    for i in range(0, num_hours):
        is_asigned_previous = assign_employees_to_room_one_hour(date_time, previous_room, num_employees)
        if not is_asigned_previous:
            for j in range(0, 11):  # TODO: find a better way to iterate over the DB
                room = Rooms.find()[j]
                is_asigned = assign_employees_to_room_one_hour(date_time, room, num_employees)
                if is_asigned:
                    previous_room = room
                    break
            if not is_asigned:
                print "There is no free room the %(i)d hour! Sorry." % {"i": i + 1}
