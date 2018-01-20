from app.Database.ManageDB import *

#format of input_file: date, duration_time, max_percent_capacity, num_employees, str_id_employee
#max_percent_capacity is double between 0 to 100. Value of 100 means that you accept maximus capacity in the room
def add_weekly_schedule_for_employee(id, input_file):
    import logging
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    if not check_id_of_employee(id):
        logging.info('Employee doesn't exist in the system')
        return "Employee doesn't exist in the system"
    employee = find_employee(id)
    employee_permission = get_access_permission_of_employee_by_id(id)
    with open(input_file) as schedule:
        for line in schedule.readlines():
            count = line.count(',')
            if line.count(',') > 3:
                date, duration_hours, max_capacity, employees, str_id_employee = line.split(',')
                num_employees = int(employees)
                id_employee_list = str_id_employee.split()
                if len(id_employee_list)!=num_employees:
                    print "problem in entering data"
            if line.count(',') == 2:
                date, duration_hours, max_capacity = line.split(',')
                num_employees = 1
            anouncments_list = assign_employees_to_room_to_X_hours(date, num_employees, int(duration_hours), employee, id_employee_list, max_capacity)
            anouncments_string = ""
            for announce in anouncments_list:
                anouncments_string += announce
        print anouncments_string
        return anouncments_string


# delete all the scheduled orders that there are in the input_file. Assume that only a director can delete the schedule.
#Notice that if the schedule is deleted, you need to update it to all the employees participating
#Ilana
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
            delete_assign_employees_from_room(date, num_employees, int(duration_hours), employee , id_employee_list)
