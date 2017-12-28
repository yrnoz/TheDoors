from Database.ManageDB import *
import random


SimRooms = db["Rooms"]  # create new table that called SimRooms just for the Simulation

#SimEmployees contains: id, permission, schedule, friends
SimEmployees = db["Employees"]  # create new table that called SimEmployees just for the Simulation


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
            output.write(str(employee["id"]) + "," + str(employee["permission"]) + "\n")







