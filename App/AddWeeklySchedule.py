from Database.ManageDB import *


def add_weekly_schedule_for_employee(id, input_file):
    """
    :param id: int of employee's id
    :param input_file: file of weekly schedule in the format: dd/mm/yy %H,room permission, num_of_employees(possible)
    :return: two things: list with notes if something went wrong, list of the rooms the employee get so far.
    """
    if not check_id_of_employee(id):
        return ["Employee doesn't exist in the system"], []
    employee = find_employee(id)
    employee_permission = get_access_permission_of_employee_by_id(id)
    rooms_assigned = []
    room_cant_assigned = []
    flag = False
    with open(input_file) as schedule:
        for line in schedule.readlines():
            if line.count(',') == 2:
                date, room_permission, employees = line.split(',')
                num_employees = int(employees)
            else:
                date, room_permission = line.split(',')
                num_employees = 1
            if int(room_permission) < employee_permission:
                room_cant_assigned.append("You don't have the right access permission for rooms with permission: " + room_permission)
            matching_rooms = Rooms.find({"permission": int(room_permission)})
            if matching_rooms.count() == 0:
                room_cant_assigned.append("There is no room matching to the permission - " + str(room_permission) + "in date: " + date)
            for room in matching_rooms:
                if assign_employees_to_room_one_hour(date, room, num_employees, employee):
                    rooms_assigned.append(room["id"])
                    flag = True
                    break
            if flag == False:
                room_cant_assigned.append("There is no place in rooms with permissions: " + str(room_permission))
            flag = False
    return room_cant_assigned, rooms_assigned
