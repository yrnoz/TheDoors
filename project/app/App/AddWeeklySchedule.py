from app.Database.ManageDB import *

import logging

from mongoengine import Q

logging.basicConfig(filename='myapp.log', level=logging.INFO)

def add_
# format of input_file: date, duration_time, max_percent_capacity, num_employees, str_id_employee
# max_percent_capacity is double between 0 to 100. Value of 100 means that you accept maximus capacity in the room
def add_weekly_schedule_for_employee(id, input_file):
    logging.info('Started')
    if not check_id_of_employee(id):
        logging.info('Employee does not exist in the system')
        return False
    employee_permission = find_employee(id).access_permission
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
            valid_rooms = get_valid_rooms(employee_permission, date, int(num_hours), 1 + len(guests_ids))
            if not valid_rooms:
                logging.info('Could not schedule your request')
                return False

            # anouncments_list = assign_employees_to_room_to_X_hours(date, num_employees, int(duration_hours), employee, id_employee_list, max_capacity)
            # anouncments_string = ""
            # for announce in anouncments_list:
            #    anouncments_string += announce
            # print anouncments_string
            # return anouncments_string


def get_valid_rooms(orderer_permission, date, num_hours=1, num_employees=1):
    logging.info("in get_valid_rooms")
    valid_rooms_ids = []
    date_time = parse_string_time_to_datetime(date)
    for room in Rooms.objects(Q(maxCapacity__gte=num_employees) & Q(access_permission__lte=orderer_permission)):
        sched = filter(lambda s: s.date == date_time,
                       room.schedules)  # TODO: will need to take into account num of hours
        if not sched:
            valid_rooms_ids.append(room.room_id)
        elif sched[0].occupancy + num_employees <= room.maxCapacity:
            valid_rooms_ids.append(room.room_id)
    return valid_rooms_ids

    # roomsSchedules = Rooms.objects(Q(access_permission__lte=orderer_permission))
    # Rooms.objects((Q(access_permission__lte=orderer_permission) & Q(maxCapacity__gte=(o)))


# def add_weekly_schedule(employee_id, date_time, num_hours=1, guests_ids=None):
#     if guests_ids is None:
#         guests_ids = []
#     global Rooms
#     global Employees
#     employees_id_list = [employee_id] + guests_ids
#     for id in employees_id_list:
#         employee = find_employee(id)
#         schedule_employee = employee["schedule"]
#         schedule_employee[date_time] = (num_employees, room["id"])
#         Employees.replace_one({'_id': employee['_id']}, employee)


# delete all the scheduled orders that there are in the input_file. Assume that only a director can delete the schedule.
# Notice that if the schedule is deleted, you need to update it to all the employees participating
# Ilana
def delete_weekly_schedule(id, input_file):
    employee = find_employee(id)
    with open(input_file) as schedule:
        for line in schedule.readlines():
            if line.count(',') > 2:
                date, duration_hours, employees, str_id_employee = line.split(',')
                num_employees = int(employees)
                id_employee_list = str_id_employee.split()
                if len(id_employee_list) != num_employees:
                    print "problem in entering data"
            if line.count(',') == 1:
                date, duration_hours = line.split(',')
                num_employees = 1
            delete_assign_employees_from_room(date, num_employees, int(duration_hours), employee, id_employee_list)
