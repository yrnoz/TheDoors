import os
import subprocess

from App.Employee import Employee
from Database.ManageDB import *


def initialize_from_dict(dict_employee):
    employee = Employee(dict_employee["id"], dict_employee["name"], dict_employee["role"], dict_employee["permission"])
    employee.friends = list(dict_employee["friends"])
    employee.schedule = dict(dict_employee["schedule"])
    return employee


def recommend_by_friends(employee):
    """return list of rooms 'res' that highly recommended for employee """
    rec_room = employee.recommendation_by_friends()
    res = []
    for room in rec_room:
        room_tmp = Rooms.find({"id": room[0]})
        if room.current_occupancy <= room_tmp.capcity:
            res.append(room[0])
    return res


def reccomendationToEmployeeByRoom(date_time, occupancy):
    reccomendedList = []
    for room in Rooms.find():
        if occupancy <= room.maxCapacity - room.schedule[date_time].occupancy:
            reccomendedList.append(room)
    return reccomendedList


# input: time requested to check num of empty places in each room.
# output: a dictionary that for each room include the number of empty seats in that room in the given time.
def emptyRooms(time):
    emptyPlaceInRooms = {}
    for room in Rooms.find():
        emptyPlaceInRooms.update(room.id, room.maxCapacity - room.schedule[time].occupancy)
    return emptyPlaceInRooms


def room_with_my_friends(friends):
    """this fun get list of friends which the user want to be with (in the same room) and return the room that
    the biggest sub group in it"""
    rooms = {}
    for friend in friends:
        location = friend.get_location()
        if location is not None:
            count = rooms.get(location, default=0) + 1
            rooms += (location, count)
    sorted_rooms = sorted(rooms, key=lambda x: x[1])
    return sorted_rooms[-1]


def print_friends():
    for employee in Employees.find():
        print "friends of {}:".format(employee["name"]) + str(employee["friends"])


def test_recommend_by_friends():
    for employee in Employees.find():
        employee_obj = initialize_from_dict(employee)
        for friend in Employees.find():
            if employee is not friend:
                employee_obj.add_friends(list(friend["id"]))
        print employee_obj.friends
        add_friends_to_employee(employee, employee_obj.friends)
    print_friends()


def test_reccomendationToEmployeeByRoom():
    pass


def test_emptyRooms():
    pass


def test_room_with_my_friends():
    pass


def print_employees_db():
    for employee in Employees.find():
        print "id: " + str(employee["id"]) + " name: " + employee["name"] + " role: " + \
              employee["role"] + " permossion: " + str(employee["permission"]) + "\n"


def print_rooms_db():
    for room in Rooms.find():
        print "id: " + room["id"] + " capacity: " + str(room["capacity"]) + " permossion: " + str(room["permission"])
        + " floor: " + str(room["floor"]) + "\n"


if __name__ == "__main__":
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    Rooms.drop()
    Employees.drop()
    import_employees_from_file("employees_test.csv")
    import_room_details_from_file("rooms_test.csv")
    print_rooms_db()
    print_employees_db()
    test_recommend_by_friends()
    test_reccomendationToEmployeeByRoom()
    test_emptyRooms()
    test_room_with_my_friends()
