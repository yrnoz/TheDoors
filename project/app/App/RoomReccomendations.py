import os
import subprocess

import datetime
from app.App.Employee import Employee
from app.App.Room import Room
from app.Database.ManageDB import *


def recommend_by_friends(employee, floor_constraint=None, capacity_constraint=1):
    """
    :param employee:
            capacity_constraint: a number between 0 and 1 which is the percentage of fullness of the room.
    :return:  list of rooms 'res' that highly recommended for employee
    """
    rec_room = employee.recommendation_by_friends()
    res = []
    for room in rec_room:
        room = initialize_room_from_dict(room)
        room_tmp = initialize_room_from_dict(Rooms.find({"id": room.id}))
        if room.current_occupancy <= capacity_constraint*room_tmp.get_capacity():
            if floor_constraint!=None and floor_constraint>=room.floor:
                res.append(room.id)
    return res


# input: time requested to check num of empty places in each room.
# output: a dictionary that for each room include the number of empty seats in that room in the given time.
def emptyRooms(employee, date_time=datetime.now().strftime("%d/%m/%y %H")):
    emptyPlaceInRooms = {}
    for room in Rooms.find({'permission': {'$gte': employee.access_permission}}):
        room = initialize_room_from_dict(room)
        emptyPlaceInRooms[room.id] = (room.maxCapacity - room.get_capacity(date_time))
    return emptyPlaceInRooms


def room_with_my_friends(friends):
    """this fun get list of friends which the user want to be with (in the same room) and return the room that
    the biggest sub group in it"""
    rooms = {}
    for friend in friends:
        location = friend.get_location()
        if location is not None:
            count = rooms.get(location, default=0) + 1
            rooms.update(location, count)
    sorted_rooms = sorted(rooms, key=lambda x: x[1])
    return sorted_rooms[-1]


def initialize_employee_from_dict(dict_employee):
    """

    :param dict_employee: dictionary of the values that needs to init employee
    :return: Employee object
    """
    employee = Employee(dict_employee["id"], dict_employee["name"], dict_employee["role"], dict_employee["permission"], dict_employee["password"])
    employee.friends = list(dict_employee["friends"])
    employee.schedule = dict(dict_employee["schedule"])
    return employee


def initialize_room_from_dict(dict_room):
    """

    :param dict_room: dictionary of the values that needs to init room
    :return: Room object
    """
    room = Room(dict_room["id"], dict_room["floor"], dict_room["capacity"], dict_room["permission"])
    room.schedule = dict(dict_room["schedule"])
    return room
