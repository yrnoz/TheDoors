from datetime import datetime, timedelta
from app.models import *
from mongoengine import Q
from pymongo import MongoClient
# from app import Rooms_table

import logging

logging.basicConfig(filename='myapp.log', level=logging.INFO)
# client = MongoClient()  # making the connection with the DB
# db = client['test-database']  # create a new DB
# Rooms = db["Rooms"]  # create new table that called Rooms
# Employees = db["Employees"]  # create new table that called Employees
from app.models import User, Room

NO_EMPLOYEE_ERROR = -1
MAX_PERMISSION = 100

Employees = User

Rooms = Room


##################################################################################

# import and export from files functions

def import_employees_from_file(input_file):
    """
    The function gets a CSV file with details about employees in the
    factory and adds them to the DB
    input: CSV file
    output: side effect  - the details added to the DB
    """
    global Employees
    man_permission = get_permission_of_manager()
    with open(input_file) as details:  # open the file
        for line in filter(lambda x: x.strip(), details.readlines()):
            if line.find('#') != -1:
                continue
            id, name, role, permission, password = line[:-1].split(",")  # get the parameters we need from the line
            if (int(permission) < 0) or (int(permission) <= man_permission and role != "Manager"):
                continue
            user = User(id=id,
                        username=name,
                        password=password,
                        role=role, access_permission=permission,
                        )
            user.save()
            # print("{} num of users {}".format(name, User.objects.count()))
            # employee = {"id": id, "name": name, "role": role, "permission": int(permission), "password": password,
            #             "friends": [],
            #             "schedule": {}}
            # Employees.insert(employee)  # add employee's details to the DB


def export_employees_to_file(output_file):
    """
        exports employee collection in csv format
        :param output_file: the name of file employees' collection will be exported to
    """
    global Employees
    with open(output_file, 'w') as output:
        output.write("# User_id ,Username ,Role ,Access permission ,Password #\n")
        for employee in Employees.objects():
            output.write(str(employee.user_id) + "," + employee.username + "," + employee.role + ","
                         + str(employee.access_permission) + "," + employee.password + "\n")

            # if not employee["friends"]:
            #     output.write(str(employee["id"]) + "," + employee["name"] + "," + employee["role"] + ","
            #                  + str(employee["permission"]) + "," + employee["password"] + "\n")
            # else:
            #     output.write(str(employee["id"]) + "," + employee["name"] + "," + employee["role"] + ","
            #                  + str(employee["permission"]) + "," + employee["password"] + "," + ",".join(
            #         employee["friends"]) + "\n")


def export_rooms_to_file(output_file):
    """
    exports room collection in csv format
    :param output_file: the name of file rooms' collection will be exported to
    """
    global Rooms
    with open(output_file, 'w') as output:
        output.write("# Room_id ,maxCapacity ,Access permission, Floor #\n")
        for room in Rooms.objects():
            output.write(str(room.room_id) + "," + str(room.maxCapacity) + "," + str(room.access_permission) + ","
                         + str(room.floor) + "\n")


def import_room_details_from_file(input_file):
    """
    The function gets a CSV file with details about rooms in the
    factory and adds them to the DB
    input: CSV file
    output: side effect  - the details added to the DB
    """
    global Rooms
    with open(input_file) as details:  # open the file
        for line in filter(lambda x: x.translate(None, '\n'), details.readlines()):
            if line.find('#') != -1:
                continue
            id, capacity, permission, floor = line.split(",")  # get the parameters we need from the line
            if int(capacity) <= 0 or int(permission) < 0:
                continue
            room = Room(room_id=id,
                        floor=floor,
                        maxCapacity=capacity,
                        access_permission=permission)
            room.save()
            # print("room id {} floor {}".format(room.room_id, room.floor))
            # room = {"id": id, "capacity": int(capacity), "permission": int(permission), "floor": int(floor),
            #         "schedule": {}}
            # Rooms.insert_one(room)  # add employee's details to the DB


#######################################################################################


# format of input_file: date, duration_time, max_percent_capacity, num_employees, str_id_employee
# max_percent_capacity is double between 0 to 100. Value of 100 means that you accept maximus capacity in the room
def add_weekly_schedule(id, input_file):
    logging.info('Started add weekly')
    if not check_id_of_employee(id):
        logging.info('Employee does not exist in the system')
        return False
    employee_permission = find_employee(id).access_permission
    logging.info('YOUR permission %d' % int(employee_permission))
    # employee = find_employee(id)
    # employee_permission = get_access_permission_of_employee_by_id(id)
    with open(input_file) as schedule:
        for line in schedule.readlines():
            count = line.count(',')
            split_line = line.split(',')
            date = split_line[0]
            num_hours = split_line[1]
            guests_ids = None
            if count >= 2:
                guests_ids = split_line[2:]
            guests_len = 0 if not guests_ids else len(guests_ids)
            logging.info('before get valid rooms')
            valid_rooms = get_valid_rooms(employee_permission, date, int(num_hours), 1 + guests_len)
            logging.info('after get valid rooms')
            if not valid_rooms:
                logging.info('Could not schedule your request')
                return False
            else:
                for _id in valid_rooms:
                    logging.info('valid_room id = %s' % _id)
            date_aux = parse_string_time_to_datetime(date)
            logging.info('After date aux')
            add_weekly_schedule_employee(id, valid_rooms[0], date_aux)
            if guests_ids:
                for _id in guests_ids:
                    add_weekly_schedule_employee(_id, valid_rooms[0],
                                                 date_aux)  # TODO: need a better heuristic to choose room (e.g. least busy, etc)
            add_weekly_schedule_room(valid_rooms[0])
    return True
    # anouncments_list = assign_employees_to_room_to_X_hours(date, num_employees, int(duration_hours), employee, id_employee_list, max_capacity)
    # anouncments_string = ""
    # for announce in anouncments_list:
    #    anouncments_string += announce
    # print anouncments_string
    # return anouncments_string


def get_valid_rooms(orderer_permission, date, num_hours=1, num_employees=1):
    logging.info("in get_valid_rooms %s" % date)
    valid_rooms_ids = []
    date_time = parse_string_time_to_datetime(date)
    logging.info("in get_valid_rooms before loop")
    for room in Rooms.objects(Q(maxCapacity__gte=num_employees) & Q(access_permission__lte=orderer_permission)):
        logging.info("in get_valid_rooms loop")
        sched = filter(lambda s: s.date == date_time,
                       room.schedules)  # TODO: will need to take into account num of hours
        if not sched:
            valid_rooms_ids.append(room.room_id)
        elif sched[0].occupancy + num_employees <= room.maxCapacity:
            valid_rooms_ids.append(room.room_id)
    return valid_rooms_ids

    # roomsSchedules = Rooms.objects(Q(access_permission__lte=orderer_permission))
    # Rooms.objects((Q(access_permission__lte=orderer_permission) & Q(maxCapacity__gte=(o)))


########## ELYASAG: PROBLEMATIC CODE########################
def add_weekly_schedule_employee(employee_id, room_id, date, time=1):
    assert check_id_of_employee(employee_id)
    logging.info('in add weekly schedule for employee %s' % employee_id)
    sched = Schedule(room_id=room_id, date=date, time=time)
    logging.info('in add weekly schedule for employee %s after sched initialization' % employee_id)
    updated = None
    # updated = Employees.objects(Q(user_id=employee_id) & Q(schedules__date=date)).update_one(set__schedules__S=sched)
    logging.info('in add weekly schedule for employee %s after updating schedule' % employee_id)
    if not updated:
        logging.info('in add weekly schedule for employee %s new schedule' % employee_id)
        Employees.objects(Q(user_id=employee_id)).update_one(schedules=[sched])  # ELYASAF: MORE SPECIFICALLY THIS
        logging.info('in add weekly schedule for employee %s new schedule finish' % employee_id)


def add_weekly_schedule_room(room_id, date, employees_ids, time=1):
    assert Rooms.objects(room_id=room_id)
    old_sched = Rooms.objects(Q(schedules__date=date) & Q(room_id=room_id)).schedules
    new_sched = None
    if old_sched:
        new_sched = Schedule(room_id=room_id, date=date, occupancy=len(employees_ids + old_sched[0].employees_id),
                             employees_ids=old_sched[0].employees_id + employees_ids, time=time)
    else:
        new_sched = Schedule(room_id=room_id, date=date, occupancy=len(employees_ids), employees_id=employees_ids,
                             time=time)
    Rooms.objects(Q(schedules__date=date) & Q(room_id=room_id)).update_one(pull__schedules__date=date)
    Rooms.objects(Q(schedules__date=date) & Q(room_id=room_id)).update_one(push__schedules=new_sched)


def assign_employees_to_room_one_hour(date_time, room, num_employees, employee, id_employee_list, max_capacity,
                                      anouncments_list):
    """
    this function gets date time in format "D/M/Y Hour", the room from the DB to assign employees,
    and number of employees to assign, if possible - they would be assigned to the room.
    :param employee:
    :param date_time: date time in format "D/M/Y Hour"
    :param room: the room from the DB to assign employees
    :param num_employees: number of employees to assign
    :return:  False - in case the employees can not be assigned to the room
              True - in case the employees were assigned to the room
    """
    global Rooms
    global Employees
    capacity = room.maxCapacity
    schedule = room.schedule
    schedule_employee = employee.schedule

    if not check_ligal_permission(employee, room, id_employee_list):
        return
    try:
        datetime.strptime(date_time, "%d/%m/%y %H")  # check the date_time format is correct
    except ValueError:
        return False
    if not (date_time in schedule):
        if num_employees > capacity or (date_time in schedule_employee):
            return False
        schedule[date_time] = (num_employees, None)
        schedule_employee[date_time] = (num_employees, room["id"])
        update_schedule_employees(date_time, room, id_employee_list, num_employees)
        anouncments_list.append(
            "Dear {}! The room that was chosen for you is: {}. For the time: {}. ".format(employee['name'], room['id'],
                                                                                          date_time))
    else:
        free_capacity_room = capacity - schedule[date_time][0]
        capacity_edited = (free_capacity_room * int(max_capacity)) / 100
        if schedule[date_time][0] + num_employees > capacity_edited | (date_time in schedule_employee):
            return False
        schedule[date_time] = (schedule[date_time][0] + num_employees, None)
        schedule_employee[date_time] = (num_employees, room["id"])
        update_schedule_employees(date_time, room, id_employee_list, num_employees)
        anouncments_list.append(
            "Dear {}! The room that was chosen for you is: {}. For the time: {}. ".format(employee['name'], room['id'],
                                                                                          date_time))
    Rooms.replace_one({'_id': room['_id']}, room)
    Employees.replace_one({'_id': employee['_id']}, employee)

    return True


def assign_employee_to_room(date_time, employee, num_hours, num_employees, guests_ids):
    pass


def parse_string_time_to_datetime(date_str, time_delta=0):
    return datetime.strptime(date_str, "%d/%m/%y %H") + timedelta(hours=time_delta)


def parse_datetime_to_string(date_time, time_delta=0):
    return datetime.strftime(date_time + timedelta(hours=time_delta), "%d/%m/%y %H")


def assign_employees_to_room_to_X_hours(date_time, num_employees, num_hours, employee, id_employee_list, max_capacity):
    """
    :param employee:
    :param date_time:
    :param num_employees:
    :param num_hours:
    """

    # employee_permission = get_access_permission_of_employee_by_id(id)
    anouncments_list = []
    num_rooms = Rooms.objects.count()  # size of the DB of Rooms
    previous_room = Rooms.objects.first()
    for i in range(0, num_hours):
        updated_time_temp = (datetime.strptime(date_time, "%d/%m/%y %H") + timedelta(hours=i))
        updated_time = datetime.strftime(updated_time_temp, "%d/%m/%y %H")
        if check_employee_already_ordered(employee, updated_time):
            anouncments_list.append(
                "Dear {}! You have already ordered room for: {} ! Sorry.".format(employee['name'], updated_time))
            continue

        is_asigned_previous = assign_employees_to_room_one_hour(updated_time, previous_room, num_employees, employee,
                                                                id_employee_list, max_capacity,
                                                                anouncments_list)
        # print anouncments_list
        if not is_asigned_previous:
            for room in Rooms.objects:
                if num_rooms == 1:
                    anouncments_list.append(
                        "Dear {}! There is no free room the {} ! Sorry.".format(employee['name'], updated_time))
                    continue
                if room.room_id == previous_room.room_id:
                    continue
                is_asigned = assign_employees_to_room_one_hour(updated_time, room, num_employees, employee,
                                                               id_employee_list, max_capacity,
                                                               anouncments_list)
                if is_asigned:
                    previous_room = room
                    break
                if not is_asigned:
                    anouncments_list.append(
                        "Dear {}! There is no free room the {} ! Sorry.".format(employee['name'], updated_time))
            print anouncments_list
            return anouncments_list
            #         for j in range(0, num_rooms):
            #             room = Rooms.objects[j]
            #             if num_rooms == 1:
            #                 anouncments_list.append(
            #                     "Dear {}! There is no free room the {} ! Sorry.".format(employee['name'], updated_time))
            #                 continue
            #
            #             if room['id'] == previous_room['id']:
            #                 continue
            #             is_asigned = assign_employees_to_room_one_hour(updated_time, room, num_employees, employee,
            #                                                            id_employee_list, max_capacity,
            #                                                            anouncments_list)
            #             if is_asigned:
            #                 previous_room = room
            #                 break
            #             if not is_asigned:
            #                 anouncments_list.append(
            #                     "Dear {}! There is no free room the {} ! Sorry.".format(employee['name'], updated_time))
            # print anouncments_list
            # return anouncments_list


# def add_weekly_schedule(employee_id, schedule_file=None):
#     import logging
#     logging.basicConfig(filename='myapp.log', level=logging.INFO)
#     logging.info('Started')
#     if schedule_file is None:
#         schedule_file = []
#         logging.info('room order is none')
#     global Employees
#     global Rooms
#     employee = find_employee(employee_id)
#     logging.info('found employee %s' % employee_id)
#     # logging.info('file path: %s' % room_order_items)
#     for item in schedule_file:
#         date_time = item.date_time
#         num_employees = item.num_employees
#         num_hours = item.num_hours
#         assign_employees_to_room_to_X_hours(date_time, num_employees, num_hours, employee)


# the function check if there is a employee which have already ordered room for the same date_time
def check_employee_already_ordered(employee, date_time):
    schedule_employee = employee["schedule"]
    if date_time in schedule_employee:  # there is an order
        name = employee['name']
        print
        "Dear {}! You have already ordered room for this time.".format(name)
        return True
    return False


def delete_assign_employees_from_room(date_time, num_employees, num_hours, employee, id_employee_list):
    global Employees
    global Rooms
    for i in range(0, num_hours):
        updated_time_temp = (datetime.strptime(date_time, "%d/%m/%y %H") + timedelta(hours=i))
        updated_time = datetime.strftime(updated_time_temp, "%d/%m/%y %H")
        if not check_room_ordered_by_employee(employee, updated_time):
            print "error delete"
            continue
        room = get_room_ordered_by_employee(employee, updated_time)
        schedule = room["schedule"]
        schedule[date_time] = (schedule[date_time][0] - num_employees, None)
        schedule_employee = employee["schedule"]
        del schedule_employee[date_time]
        Rooms.replace_one({'_id': room['_id']}, room)

        for id in id_employee_list:
            employee_friend = find_employee(id)
            schedule_employee = employee_friend["schedule"]
            del schedule_employee[date_time]
            Employees.replace_one({'_id': employee_friend['_id']}, employee_friend)


def check_room_ordered_by_employee(employee, updated_time):
    schedule_employee = employee["schedule"]
    if id in schedule_employee:
        return False
    return True


def get_room_ordered_by_employee(employee, updated_time):
    room = None
    schedule_employee = employee["schedule"]
    # if id in schedule_employee:
    id_room = schedule_employee[updated_time][1]
    room = find_room(id_room)
    return room


#######################################################################################

# aux functions for the DB

def add_employee(employee):
    """
    Adds a given employee into the db.
    Useful for on-the-fly addition of employees into the DB when the system is already up-and-running (i.e. after
    the DB initialization phase)
    :param employee: the employee object to be added into the DB.
    """
    global Employees
    employee_json = {"id": employee.id, "name": employee.name, "role": employee.role,
                     "permission": int(employee.access_permission), "password": employee.password,
                     "friends": employee.friends,
                     "schedule": {}}
    Employees.insert(employee_json)


def remove_employee(id):
    global Employees
    if not Employees.delete_one({"id": id}).deleted_count:
        print 'No such employee'


def update_employee(id, name, role, permission, password, friends, schedules):
    global Employees
    if not Employees.update_one({'id': id},
                                {'$set': {'name': name, 'role': role, 'permission': permission, 'password': password,
                                          'friends': friends, "schedule": schedules}}).matched_count:
        print "No such employee"


def add_room(room):
    """
    Adds a new room into the db.
    Useful for on-the-fly addition of rooms into the DB when the system is already up-and-running (i.e. after
    the DB initialization phase)
    :param room: room to be added into the DB
    """
    global Rooms
    room_json = {"id": room.id, "capacity": int(room.maxCapacity), "permission": int(room.access_permission),
                 "floor": int(room.floor), "schedule": {}}
    Rooms.insert(room_json)


def remove_room(id):
    global Rooms
    if not Rooms.delete_one({"id": id}).deleted_count:
        print
        'No such room'


def update_room(id, floor, max_capacity, access_permission, schedule):
    global Rooms
    if not Rooms.update_one({'id': id},
                            {'$set': {'floor': floor, 'capacity': max_capacity,
                                      'access_permission': access_permission, "schedule": schedule}}).matched_count:
        print
        'No such room'


def get_access_permission_of_employee_by_id(id):
    global Employees
    if not (check_id_of_employee(id)):
        return NO_EMPLOYEE_ERROR
    employee = find_employee(id)

    return int(employee.permission)


# input: id output: password of this employee
def get_password_of_employee_by_id(id):
    global Employees
    employee = Employees.find_one({"id": str(id)})
    return str(employee["password"])


# input: id output: True - if there is employee with this id False other wise
def check_id_of_employee(id):
    global Employees
    employee = Employees.objects.get(user_id=str(id))
    if employee is None:
        return False
    return True


# input: id output: True - if there is employee with this id False other wise
def check_id_str_of_employee(id):
    global Employees
    employee = Employees.find_one({"id": id})
    if employee is None:
        return False
    return True


# input: id, password output: True if the password match the employee False otherwise
def check_password_of_employee(username, password):
    global Employees
    for employee in Employees.objects(username=str(username)):
        if employee.password == password:
            if employee.access_permission == MAX_PERMISSION:
                return {'user_type': "MANAGER", 'user_id': employee.id}
            return {'user_type': "USER", 'user_id': employee.id}
    return {'user_type': "NOT_EXIST"}


# input: id output: the employee with this id
def find_employee(id):
    if check_id_of_employee(id):
        return Employees.objects.get(user_id=str(id))
    return None


def check_ligal_permission(employee, room, id_employee_list):
    max_permission = get_minimum_permission_in_factory()  # I assume it is the max
    for id in id_employee_list:
        permission_employee = int(find_employee(id)["permission"])
        if permission_employee > max_permission:
            max_permission = permission_employee
    employee_permission = int(employee["permission"])
    max_permission_all = max(employee_permission, max_permission)
    room_permission = room["permission"]
    if max_permission_all <= room_permission:
        return True
    return False


def check_room_id(id):
    global Rooms
    return Rooms.objects.get(room_id=str(id)) is not None


# input: id output: the room with this id
def find_room(id):
    global Rooms
    return Rooms.objects(room_id=str(id))


def get_average_friends_in_factory():
    '''
        A function that calculate the average friends per employee
        :return: the average friends per employee
    '''
    num_employees = Employees.find().count()
    if num_employees is 0:
        return -1
    employees = []
    for employee in Employees.find():
        employees.append(employee)
    num_friends = reduce(lambda x, y: x + y, map(lambda x: len(x["friends"]), employees))
    return int(num_friends / num_employees)


def get_minimum_permission_in_factory():
    '''
    A function that returns the minimum permission of an employee in the factory
    :return: the minimum permission.
    '''
    if Employees.find().count() == 0:
        return -1
    permissions = []
    for employee in Employees.find():
        permissions.append(int(employee["permission"]))
    return max(permissions)


def get_permission_of_manager():
    '''
    A function that returns the permission of the manager in the factory
    :return: the permission of the manager.
    '''
    if Employees.objects().count() == 0:
        return -1
    permissions = []
    for employee in Employees.objects(role="Manager"):
        permissions.append(employee.access_permission)
    if not permissions:
        return -1
    return min(permissions)


####################### NEEDS TO BE UPDATED, DOESN'T WORK ANYMORE! ################################

def add_a_friend_for_employee(employee_id, friend_id):
    """
    adds a friend to employees' friend list (and vice versa)
    :param employee_id: id of employee
    :param friend_id: id of employees' friend
    :return: side effect: employee and his friends are now in each others' friends' list
    """
    employee = find_employee(employee_id)
    friend = find_employee(friend_id)
    if employee is None or friend is None:
        return
    add_friend_aux(employee, friend_id)
    add_friend_aux(friend, employee_id)


def add_friend_aux(employee, friend_id):
    """
    An auxiliary function for the above, it does the actual changes to the DB (wrote it to avoiding code duplication)
    :param employee: the employee who adds the friend
    :param friend_id: the id of the friend
    """
    employee_friends = employee["friends"]
    employee_friends.append(friend_id)
    Employees.update_one({'id': employee["id"]},
                         {'$set': {
                             'friends': employee_friends}})


def delete_a_friend_from_employee(employee_id, friend_id):
    """
    deletes a friend from employee's list
    :param employee_id: the employee that wants to delete a friend
    :param friend_id: the id of the friend to be deleted
    :return: side effect, given employee and friend won't be friends any longer
    """
    employee = find_employee(employee_id)
    friend = find_employee(friend_id)
    if employee is None or friend is None:
        return
    delete_a_friend_aux(employee, friend_id)
    delete_a_friend_aux(friend, employee_id)


def delete_a_friend_aux(employee, friend_id):
    """
    An auxiliary function for the above, it does the actual changes to the DB (wrote it to avoiding code duplication)
    :param employee: employee that wants to remove given id from his list
    :param friend_id: id of the friend to be removed
    """
    employee_friends = employee["friends"]
    employee_friends.remove(friend_id)
    Employees.update_one({'id': employee["id"]},
                         {'$set': {
                             'friends': employee_friends}}).matched_count


def set_location_of_employee(employee_id, room_id, room_floor):
    """
    Updates employee's location in the DB when he enters into a room
    :param employee_id: id of employee entering a room
    :param room_id: id of the room the employee's entering into
    :param room_floor: the floor of the id
    :return: side effect: employee is marked as being in the room in the DB
    """
    # TODO: room floor might be redundant, need to reconsider it
    if not (check_id_of_employee(employee_id) or find_room(room_id)):
        return
    global Employees
    global Rooms
    Employees.update_one({'id': employee_id},
                         {'$set': {'current_room': {'room_id': room_id, 'room_floor': room_floor}}})


def handle_employee_exiting_a_room(employee_id):
    """
    handles employee exiting a room by unsetting the location field in the DB
    :param employee_id: id of employee that exits a room
    """
    if not check_id_of_employee(employee_id):
        return
    Employees.update_one({'id': employee_id},
                         {'$unset': {'current_room': {}}})


def check_if_theres_an_employee_friend_in_room(employee_id, room_id):
    """
    Checks if there's a friend of given employee in the specified room
    :param employee_id: employee whose friends list we're querying for presence in the room
    :param room_id: room where we look for friends in
    :return: True - if there's a friend in specified room, False - otherwise
    """
    if not (check_id_of_employee(employee_id) or find_room(room_id)):
        return False
    friends_list = find_employee(employee_id)["friends"]
    for friend_id in friends_list:
        friend = Employees.find_one({"$and": [{"id": friend_id},
                                              {"current_room": {"$exists": True}},
                                              {"current_room.room_id": room_id}]})
        if friend is not None:
            return True
    return False
    # friends_in_room = friends_list.filter()

####################################################################################################
