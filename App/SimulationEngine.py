from Database.ManageDB import *
import random


SimRooms = db["Rooms"]  # create new table that called SimRooms just for the Simulation

#SimEmployees contains: id, permission, schedule, friends
SimEmployees = db["Employees"]  # create new table that called SimEmployees just for the Simulation

def simulation_import_room_details_from_file(input_file):
    """
    The function gets a CSV file with details about rooms in the
    factory and add them to the DB
    input: CSV file
    output: side effect  - the details added to the DB
    """
    global SimRooms
    with open(input_file) as details:  # open the file
        for line in filter(lambda x: x.strip(), details.readlines()):
            id, capacity, permission, floor = line[:-1].split(",")  # get the parameters we need from the line
            room = {"id": id, "capacity": int(capacity), "permission": int(permission), "floor": int(floor),
                    "schedule": {}}
            SimRooms.insert(room)  # add room's details to the DB

def simulation_export_rooms_to_file(output_file):
    """
    The function export to the manager a CSV file with all the rooms in the simulation factory
    :param output_file: file to write the rooms to.
    """
    global SimRooms
    with open(output_file, 'w') as output:
        for room in SimRooms.find():
            output.write(room["id"] + "," + str(room["capacity"]) + "," + str(room["permission"]) + ","
                         + str(room["floor"]) + "\n")


def simulation_add_random_employees(employees_number, min_permission):
    """
    The function add random employees to the simulation factory
    :param employees_number: number of employees in the simulation factory
    :param min_permission: min permission of employee.
    """
    global SimEmployees
    for i in range(0, employees_number):
        id = random.randint(0,employees_number*1000)
        while check_id_of_employee(id):
            id = random.randint(0, employees_number * 1000)
        permission = random.randint(1,min_permission)
        employee = {"id": int(id), "permission": int(permission), "friends": [], "schedule": {}}
        Employees.insert(employee)  # add employee's details to the DB


def simulation_export_employees_to_file(output_file):
    global SimEmployees
    with open(output_file, 'w') as output:
        for employee in SimEmployees.find():
            output.write(str(employee["id"]) + "," + str(employee["permission"]) + \
                         simulation_get_schedule_of_employee(employee["id"]) + "\n")

def simulation_get_schedule_of_employee(id):
    employee = find_employee(id)
    schedule = employee["schedule"]
    employee_schedule = ""
    for date_time, tuple in schedule.items():
        employee_schedule += date_time + ": " + tuple[1] + "; "
    return employee_schedule





