from Database.ManageDB import *
import random
import time


SimRooms = db["SimRooms"]  # create new table that called SimRooms just for the Simulation

# SimEmployees contains: id, permission, schedule, friends
SimEmployees = db["SimEmployees"]  # create new table that called SimEmployees just for the Simulation


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
        id = random.randint(0, employees_number * 1000)
        while check_id_of_employee(id):
            id = random.randint(0, employees_number * 1000)
        permission = random.randint(1, min_permission)
        employee = {"id": int(id), "name" : "John", "role" : "Engineer", "permission": int(permission), "password" : "123", "friends": [], "schedule": {}}
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

def check_id_of_simemployee(id):
    global SimEmployees
    employee = SimEmployees.find_one({"id": str(id)})
    if employee is None:
        return False
    return True


#the function copy all employees from the DB to the simulation DB
def simulation_copy_employees_from_DB():
    global SimEmployees
    global Employees
    if Employees.find().count() == 0:
        return False
    for employee in Employees.find():
        if check_id_of_simemployee(employee["id"]):
            continue
        employee["schedule"] = {}
        SimEmployees.insert_one(employee)
    return True

def check_id_of_simroom(id):
    global SimRooms
    room = SimRooms.find_one({"id": str(id)})
    if room is None:
        return False
    return True

# the function copy all rooms from the DB to the simulation DB
def simulation_copy_rooms_from_DB():
    global SimRooms
    global Rooms
    if Rooms.find().count() == 0:
        return False
    for room in Rooms.find():
        if check_id_of_simroom(room["id"]):
            room["schedule"] = {}
            SimRooms.replace_one({'_id': room['_id']}, room)
            continue
        room["schedule"] = {}
        SimRooms.insert(room)
    return True

#the function assign employees with random people to rooms
def simulation_assign_employees(date_time, percent_employees):
    #now = time.strftime("%d/%m/%Y %H")
    rooms = SimRooms.find()
    employees = SimEmployees.find()
    count = 0
    dbg = list(rooms)
    for employee in employees:
        count += 1
        num_employees = random.randint(1, int(employees.count()/5))
        random.shuffle(dbg)
        for room in dbg:
            if simulation_assign_employees_to_room_one_hour(date_time, room, num_employees, employee):
                break
        if count >= int((percent_employees*(employees.count()))/100):
            break


def simulation_assign_employees_to_room_one_hour(date_time, room, num_employees, employee):
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
    global SimRooms
    capacity = room["capacity"]
    schedule = room["schedule"]
    schedule_employee = employee["schedule"]
    try:
        datetime.strptime(date_time, "%d/%m/%y %H")  # check the date_time format is correct
    except ValueError:
        return False
    if not (date_time in schedule):
        if num_employees > capacity or (date_time in schedule_employee):
            return False
        schedule[date_time] = (num_employees, None)
        schedule_employee[date_time] = (num_employees, room["id"])
        simulation_update_schedule_employees(date_time, room["id"], employee["id"], num_employees)
    else:
        if schedule[date_time][0] + num_employees > capacity or (date_time in schedule_employee):
            return False
        schedule[date_time] = (schedule[date_time][0] + num_employees, None)
        schedule_employee[date_time] = (num_employees, room["id"])
        simulation_update_schedule_employees(date_time, room["id"], employee["id"] ,num_employees)
    SimRooms.replace_one({'_id': room['_id']}, room)
    return True

def simulation_update_schedule_employees(date_time, room_id, employee_id, num_employees):
    schedule_employee = find_employee(employee_id)["schedule"]
    schedule_employee[date_time] = (num_employees, room_id)


#
#THIS IS THE MAIN FUNCTION OF THE SIMULATION
#
def simulation_day_in_factory(start_time, finish_time, percent_employees, new_rooms_details = None):
    if start_time < 0 or start_time > 24 or finish_time < 0 or finish_time > 24:
        raise NameError("start time or finish time is not in the right format")
    if start_time > finish_time:
        raise NameError("start time have to be smaller than finish time")
    if percent_employees < 0 or percent_employees > 100 or percent_employees % 10 != 0:
        raise NameError("percent_employees is not in the right format")
    if simulation_copy_employees_from_DB() is False:
        raise NameError("There are no employees")
    if simulation_copy_rooms_from_DB() is False:
        raise NameError("There are no employees")
    if not (new_rooms_details is None):
        simulation_import_room_details_from_file(new_rooms_details)
    date_now = time.strftime("%d/%m/%y")
    with open('Simulation_Stats.xls', 'w') as output:
        for hour in range(start_time, finish_time):
            if hour < 10:
                date_time = date_now + " 0" + str(hour)
            else:
                date_time = date_now + " " + str(hour)
            simulation_assign_employees(date_time, percent_employees)
        rooms = list(SimRooms.find())
        for hour in range(start_time, finish_time):
            date_time = date_now + " " + str(hour)
            output.write(date_time + "\n")
            for room in rooms:
                if not (date_time in room["schedule"]):
                    output.write(room["id"] + "\t" + "empty\n")
                    continue
                schedule = room["schedule"][date_time]
                output.write(room["id"] + "\t" + str(float(schedule[0])/int(room["capacity"])*100) + "%" + "\n")

def mainTest():
    import_employees_from_file("employees_test.csv")
    import_room_details_from_file("rooms_test.csv")
    try:
        simulation_day_in_factory(26, 12, 30)
    except Exception as e:
        print e
    try:
        simulation_day_in_factory(8, 30, 30)
    except Exception as e:
        print e
    try:
        simulation_day_in_factory(9, 12, 17)
    except Exception as e:
        print e
    try:
        simulation_day_in_factory(16, 12, 20)
    except Exception as e:
        print e
    start_time = random.randint(8,12)
    end_time = random.randint(13, 20)
    percent_employee = random.randint(1,8)
    simulation_day_in_factory(start_time,end_time,percent_employee*10)


if __name__ == "__main__":
    mainTest()








