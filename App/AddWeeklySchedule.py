from Database.ManageDB import *


def add_weekly_schedule_for_employee(id, input_file):
    if not check_id_of_employee(id):
        return "Employee doesn't exist in the system"
    employee = find_employee(id)
    employee_permission = get_access_permission_of_employee_by_id(id)
    rooms_assigned = ""
    with open(input_file) as schedule:
        for line in schedule.readlines():
            if line.count(',') == 2:
                date, room_permission, num_employees = line.split(',')
            else:
                date, room_permission = line.split(',')
                num_employees = 1
            if room_permission < employee_permission:
                return "You don't have the right access permission"
            matching_rooms = Rooms.find({"permission": int(room_permission)})
            if matching_rooms.count() == 0:
                return "There is no room matching to the permission - " + str(room_permission)
            for room in matching_rooms:
                if assign_employees_to_room_one_hour(date, room, num_employees, employee):
                    rooms_assigned += " " + room["id"]
                    break
    return rooms_assigned
