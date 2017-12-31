from datetime import datetime, timedelta
from pymongo import MongoClient

client = MongoClient()  # making the connection with the DB
db = client['test-database']  # create a new DB
Rooms = db["Rooms"]  # create new table that called Rooms
Employees = db["Employees"]  # create new table that called Employees


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
    with open(input_file) as details:  # open the file
        for line in filter(lambda x: x.strip(), details.readlines()):
            id, name, role, permission = line[:-1].split(",")  # get the parameters we need from the line
            employee = {"id": id, "name": name, "role": role, "permission": int(permission), "friends": [],
                        "schedule": {}}
            Employees.insert(employee)  # add employee's details to the DB


def export_employees_to_file(output_file):
    """
    exports employee collection in csv format
    :param output_file: the name of file employees' collection will be exported to
    """
    global Employees
    with open(output_file, 'w') as output:
        for employee in Employees.find():
            if not employee["friends"]:
                output.write(str(employee["id"]) + "," + employee["name"] + "," + employee["role"] + ","
                             + str(employee["permission"]) + "\n")
            else:
                output.write(str(employee["id"]) + "," + employee["name"] + "," + employee["role"] + ","
                             + str(employee["permission"]) + "," + ",".join(employee["friends"]) + "\n")


def export_rooms_to_file(output_file):
    """
    exports room collection in csv format
    :param output_file: the name of file rooms' collection will be exported to
    """
    global Rooms
    with open(output_file, 'w') as output:
        for room in Rooms.find():
            output.write(room["id"] + "," + str(room["capacity"]) + "," + str(room["permission"]) + ","
                         + str(room["floor"]) + "\n")


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
            id, capacity, permission, floor = line.split(",")  # get the parameters we need from the line
            room = {"id": id, "capacity": int(capacity), "permission": int(permission), "floor": int(floor),
                    "schedule": {}}
            Rooms.insert_one(room)  # add employee's details to the DB


#######################################################################################


def assign_employees_to_room_one_hour(date_time, room, num_employees, employee, anouncments_list):
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
    capacity = room["capacity"]
    schedule = room["schedule"]
    schedule_employee = employee["schedule"]
    if check_legal_permission(employee, room) == False:
        anouncments_list.append("Dear {}! There is no free room the {} ! Sorry.".format(employee['name'], date_time))
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
        anouncments_list.append(
            "Dear {}! The room that was chosen for you is: {}. For the time: {}. ".format(employee['name'], room['id'],
                                                                                          date_time))
    else:
        if schedule[date_time][0] + num_employees > capacity | (date_time in schedule_employee):
            return False
        schedule[date_time] = (schedule[date_time][0] + num_employees, None)
        schedule_employee[date_time] = (num_employees, room["id"])
        anouncments_list.append(
            "Dear {}! The room that was chosen for you is: {}. For the time: {}. ".format(employee['name'], room['id'],
                                                                                          date_time))
    Rooms.replace_one({'_id': room['_id']}, room)
    return True


def assign_employees_to_room_to_X_hours(date_time, num_employees, num_hours, employee):
    """
    :param employee:
    :param date_time:
    :param num_employees:
    :param num_hours:
    """

    # employee_permission = get_access_permission_of_employee_by_id(id)
    anouncments_list = []
    num_rooms = Rooms.find().count()  # size of the DB of Rooms
    previous_room = Rooms.find()[0]
    for i in range(0, num_hours):
        updated_time_temp = (datetime.strptime(date_time, "%d/%m/%y %H") + timedelta(hours=i))
        updated_time = datetime.strftime(updated_time_temp, "%d/%m/%y %H")
        if check_employee_already_ordered(employee, updated_time):
            continue

        is_asigned_previous = assign_employees_to_room_one_hour(updated_time, previous_room, num_employees, employee,
                                                                anouncments_list)
        # print anouncments_list
        if not is_asigned_previous:
            for j in range(0, num_rooms):
                room = Rooms.find()[j]
                if room["id"] == previous_room["id"]:
                    continue
                is_asigned = assign_employees_to_room_one_hour(updated_time, room, num_employees, employee,
                                                               anouncments_list)
                if is_asigned:
                    previous_room = room
                    break
                if not is_asigned:
                    anouncments_list.append(
                        "Dear {}! There is no free room the {} ! Sorry.".format(employee['name'], updated_time))
    print anouncments_list
    return anouncments_list


def add_weekly_schedule(employee_id, room_order_items=None):
    if room_order_items is None:
        room_order_items = []
    global Employees
    global Rooms
    employee = find_employee(employee_id)

    for item in room_order_items:
        date_time = item.date_time
        num_employees = item.num_employees
        num_hours = item.num_hours
        assign_employees_to_room_to_X_hours(date_time, num_employees, num_hours, employee)


# the function check if there is a employee which have already ordered room for the same date_time
def check_employee_already_ordered(employee, date_time):
    schedule_employee = employee["schedule"]
    if date_time in schedule_employee:  # there is an order
        name = employee['name']
        print
        "Dear {}! You have already ordered room for this time.".format(name)
        return True
    return False


def delete_assign_employees_from_room(date_time, num_employees, num_hours, employee):
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
        schedule_employee[date_time] = (0, None)


def check_room_ordered_by_employee(employee, updated_time):
    schedule_employee = employee["schedule"]
    if id in schedule_employee:
        return False
    return True


def get_room_ordered_by_employee(employee, updated_time):
    schedule_employee = employee["schedule"]
    if id in schedule_employee:
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
                     "permission": int(employee.access_permission), "friends": employee.friends,
                     "schedule": {}}
    Employees.insert(employee_json)


def remove_employee(id):
    global Employees
    if not Employees.delete_one({"id": id}).deleted_count:
        print 'No such employee'


def update_employee(id, name, role, permission, friends, schedules):
    global Employees
    if not Employees.update_one({'id': id},
                                {'$set': {'name': name, 'role': role, 'permission': permission,
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

#input: id. output: the permission of the employee
def get_access_permission_of_employee_by_id(id):
    global Employees
    employee = Employees.find_one({"id": str(id)})
    if employee is None:
        return -1
    return int(employee["permission"])

#input: id of employee. output: true if the employee exists
def check_id_of_employee(id):
    global Employees
    employee = Employees.find_one({"id": str(id)})
    if employee is None:
        return False
    return True

#input: id of employee. output: the employee with the id
def find_employee(id):
    if check_id_of_employee(id):
        return Employees.find_one({"id": str(id)})


def check_legal_permission(employee, room):
    employee_permission = int(employee["permission"])
    room_permission = room["permission"]
    if employee_permission <= room_permission:
        return True
    return False


def find_room(id):
    return Rooms.find_one({"id": str(id)})


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

    stam = Employees.update_one({'id': employee["id"]},
                         {'$set': {
                             'friends': employee_friends}}).matched_count
    print "stam: " + str(stam)

def get_average_friends_of_employee():
    '''
    A function that calculate the average friends per employee
    :return: the average friends per employee
    '''
    employees = Employees.find()
    num_employees = employees.count()
    num_friends = reduce(lambda x,y: x+y, map(lambda x: x["friends"].count(), employees))
    return int(num_friends/num_employees)




####################################################################################################
