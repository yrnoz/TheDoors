import os
import subprocess
import sys

from App.Employee import Employee
from App.Room import Room
from Database.ManageDB import *

sys.path.append(os.getcwd())


def enter_rooms_csv(filename):
    import_room_details_from_file(filename)


def enter_employees_csv(filename):
    import_employees_from_file(filename)


def add_employee_aux(employee_str):
    id, name, role, access_permission = employee_str.split()
    add_employee(Employee(int(id), name, role, int(access_permission)))


def add_room_aux(room_str):
    id, floor, max_capacity, access_permission = room_str.split()
    add_room(Room(id, int(floor), int(max_capacity), int(access_permission)))


def remove_employee_aux(id):
    remove_employee(int(id))


def update_employee_aux(employee_str):
    id, name, role, access_permission = employee_str.split()
    update_employee(int(id), name, role, int(access_permission))


def update_room_aux(room_str):
    id, floor, max_capacity, access_permission = room_str.split()
    update_room(id, int(floor), int(max_capacity), int(access_permission))


def enter_week_sched_cvs(filename):
    pass  # waiting for fundction to be written


def get_room_recommendation(cmd_str):
    """
    id, date_time = cmd_str.split(' ', 1)
    RoomReccomendations(Rooms, Employees).reccomendationToEmployeeByRoom(int(id), date_time)
    """
    pass


def help():
    print("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format('Currently, available commands are: ',
                                                                'enter_rooms_csv filename',
                                                                'enter_employees_csv filename',
                                                                'add_employee id name role access_permission',
                                                                'add_room id floor max_capacity access_permission',
                                                                'remove_employee id',
                                                                'remove_room id',
                                                                'update_employee id name role access_permission',
                                                                'update_room id floor max_capacity access_permission',
                                                                # 'enter_week_sched_cvs id filename',
                                                                # 'get_room_recommendation id DD/MM/YY HH',
                                                                'help', 'quit'))


if __name__ == "__main__":
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    print('Welcome to TheDoors, The Program for Solving the Door Permissions Problem!')
    help()

    cmd_dict = {'enter_rooms_csv': enter_rooms_csv,
                'enter_employees_csv': enter_employees_csv,
                'add_employee': add_employee_aux,
                'add_room': add_room_aux,
                'remove_employee': remove_employee_aux,
                'remove_room': remove_room,
                'update_employee': update_employee_aux,
                'update_room': update_room_aux,
                'enter_week_sched_cvs': enter_week_sched_cvs,
                'get_room_recommendation': get_room_recommendation}
    while True:
        cmd_args = raw_input('>>> ').split(' ', 1)
        if cmd_args == ['help']:
            help()
        elif cmd_args == ['quit']:
            print('Shutting down Program')
            p.terminate()
            break
        elif len(cmd_args) > 1 and cmd_args[0] in cmd_dict.keys():
            cmd, args = cmd_args
            try:
                cmd_dict[cmd](args)
            except (ValueError, TypeError) as e:
                print('Error! Invalid input, try again')
        else:
            print('Command does not exist, please try again.')
